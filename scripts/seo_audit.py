#!/usr/bin/env python3
"""SEO content depth audit.

For each content HTML page:
- Computes Flesch Reading Ease (target > 60)
- Counts words, sentences, paragraphs
- Counts engagement elements: tables, charts (canvas/svg), interactive inputs,
  FAQ items, scenario examples (dollar amounts), percentages, year references
- Detects "what this means for you" empathy sections
- Flags AI-generic boilerplate phrases
- Estimates repetition via type-token ratio

Outputs a ranked Markdown report at seo-audit.md.

No external deps; uses html.parser + re from stdlib.
"""
from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Tags whose inner text is invisible (or chrome we don't want in the body text).
BLOCK_TAGS = {"script", "style", "head", "noscript", "template"}
CHROME_TAGS = {"nav", "header", "footer"}

# Phrases that signal AI-generic or thin "filler" content.
AI_GENERIC_PHRASES = [
    "in conclusion",
    "in summary",
    "it is important to note",
    "it should be noted",
    "various factors",
    "a wide variety of",
    "navigate the complexities",
    "in today's world",
    "in this article we will",
    "delve into",
    "tapestry of",
    "ever-evolving",
    "fast-paced world",
    "first and foremost",
    "as previously mentioned",
    "needless to say",
    "the bottom line is",
]

# Empathetic "what this means for you" markers.
EMPATHY_MARKERS_RE = re.compile(
    r"\b(what this means|for you|in your case|if you|your take[- ]home|your situation|"
    r"your monthly|your salary|your numbers|so what|here['']?s what)\b",
    re.IGNORECASE,
)

SENTENCE_END_RE = re.compile(r"[.!?](?:\s|$)")
DOLLAR_RE = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?")
PERCENT_RE = re.compile(r"\b\d+(?:\.\d+)?\s?%")
YEAR_RE = re.compile(r"\b(?:2024|2025|2026)\b")


class BodyTextExtractor(HTMLParser):
    """Walks the HTML, collecting visible body text and counts of elements."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0           # Inside script/style/etc.
        self.chrome_depth = 0         # Inside nav/header/footer
        self.text_chunks: list[str] = []
        self.tag_counts: dict[str, int] = {}
        self.input_types: dict[str, int] = {}
        self.headings_h1: list[str] = []
        self.headings_h2: list[str] = []
        self.headings_h3: list[str] = []
        self._current_heading: str | None = None
        self._heading_buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr_dict = {k.lower(): (v or "") for k, v in attrs}

        if tag in BLOCK_TAGS:
            self.skip_depth += 1
            return
        if tag in CHROME_TAGS:
            self.chrome_depth += 1
            return

        # Count all tags (only outside skip/chrome regions for fairness)
        if self.skip_depth == 0 and self.chrome_depth == 0:
            self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1
            if tag == "input":
                t = attr_dict.get("type", "text").lower()
                self.input_types[t] = self.input_types.get(t, 0) + 1
            if tag in ("h1", "h2", "h3"):
                self._current_heading = tag
                self._heading_buf = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in BLOCK_TAGS:
            if self.skip_depth > 0:
                self.skip_depth -= 1
            return
        if tag in CHROME_TAGS:
            if self.chrome_depth > 0:
                self.chrome_depth -= 1
            return
        if tag == self._current_heading:
            text = " ".join(self._heading_buf).strip()
            if tag == "h1" and text:
                self.headings_h1.append(text)
            elif tag == "h2" and text:
                self.headings_h2.append(text)
            elif tag == "h3" and text:
                self.headings_h3.append(text)
            self._current_heading = None
            self._heading_buf = []

    def handle_data(self, data: str) -> None:
        if self.skip_depth > 0 or self.chrome_depth > 0:
            return
        self.text_chunks.append(data)
        if self._current_heading is not None:
            self._heading_buf.append(data)


WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")


def count_syllables(word: str) -> int:
    """Simple heuristic syllable counter (good enough for Flesch)."""
    w = word.lower()
    if not w:
        return 0
    # Common exceptions
    if w.endswith("e") and not w.endswith("le") and len(w) > 2:
        w = w[:-1]
    groups = re.findall(r"[aeiouy]+", w)
    return max(1, len(groups))


@dataclass
class PageStats:
    path: str
    is_stub: bool = False
    body_words: int = 0
    sentences: int = 0
    syllables: int = 0
    flesch_reading_ease: float = 0.0
    flesch_kincaid_grade: float = 0.0
    type_token_ratio: float = 0.0
    paragraphs: int = 0
    h2_count: int = 0
    h3_count: int = 0
    tables: int = 0
    list_items: int = 0
    inputs_numeric: int = 0
    inputs_range: int = 0
    selects: int = 0
    buttons: int = 0
    canvas: int = 0
    svg: int = 0
    details: int = 0          # <details> = collapsible FAQ-ish
    faq_jsonld: int = 0       # FAQ entries in JSON-LD
    dollar_examples: int = 0
    percent_examples: int = 0
    year_refs: int = 0
    empathy_hits: int = 0
    generic_hits: int = 0
    flags: list[str] = field(default_factory=list)


def compute_flesch(words: int, sentences: int, syllables: int) -> tuple[float, float]:
    if words == 0 or sentences == 0:
        return 0.0, 0.0
    wps = words / sentences
    spw = syllables / words
    fre = 206.835 - 1.015 * wps - 84.6 * spw
    fk = 0.39 * wps + 11.8 * spw - 15.59
    return round(fre, 1), round(fk, 1)


def count_faq_jsonld(html_text: str) -> int:
    count = 0
    for block in re.findall(
        r"<script type=\"application/ld\+json\">(.*?)</script>",
        html_text,
        re.DOTALL,
    ):
        if "\"FAQPage\"" in block:
            count += block.count("\"@type\": \"Question\"")
    return count


def analyze(path: Path) -> PageStats:
    s = PageStats(path=str(path.relative_to(ROOT)))
    raw = path.read_text(encoding="utf-8", errors="ignore")

    # Detect stub redirect pages (very small, redirect-only)
    raw_no_ws = re.sub(r"\s+", " ", raw)
    if len(raw_no_ws) < 1200 and (
        "window.location" in raw or "http-equiv=\"refresh\"" in raw.lower()
    ):
        s.is_stub = True
        return s

    parser = BodyTextExtractor()
    parser.feed(raw)
    text = " ".join("".join(parser.text_chunks).split())

    # Word/sentence/syllable
    words = WORD_RE.findall(text)
    word_count = len(words)
    sentence_count = max(1, len(SENTENCE_END_RE.findall(text)))
    syllable_count = sum(count_syllables(w) for w in words)

    s.body_words = word_count
    s.sentences = sentence_count
    s.syllables = syllable_count
    s.flesch_reading_ease, s.flesch_kincaid_grade = compute_flesch(
        word_count, sentence_count, syllable_count
    )

    if word_count > 0:
        unique = len({w.lower() for w in words})
        s.type_token_ratio = round(unique / word_count, 3)

    # Structural element counts
    s.paragraphs = parser.tag_counts.get("p", 0)
    s.h2_count = len(parser.headings_h2)
    s.h3_count = len(parser.headings_h3)
    s.tables = parser.tag_counts.get("table", 0)
    s.list_items = parser.tag_counts.get("li", 0)
    s.canvas = parser.tag_counts.get("canvas", 0)
    s.svg = parser.tag_counts.get("svg", 0)
    s.details = parser.tag_counts.get("details", 0)
    s.selects = parser.tag_counts.get("select", 0)
    s.buttons = parser.tag_counts.get("button", 0)
    s.inputs_numeric = parser.input_types.get("number", 0)
    s.inputs_range = parser.input_types.get("range", 0)

    # FAQ JSON-LD entries
    s.faq_jsonld = count_faq_jsonld(raw)

    # Example density
    s.dollar_examples = len(DOLLAR_RE.findall(text))
    s.percent_examples = len(PERCENT_RE.findall(text))
    s.year_refs = len(YEAR_RE.findall(text))

    # Empathy + generic phrase hits
    s.empathy_hits = len(EMPATHY_MARKERS_RE.findall(text))
    low = text.lower()
    s.generic_hits = sum(low.count(p) for p in AI_GENERIC_PHRASES)

    # Flag conditions
    if word_count < 600:
        s.flags.append("THIN (<600 words)")
    if s.flesch_reading_ease < 60:
        s.flags.append(f"HARD-TO-READ (FRE {s.flesch_reading_ease})")
    if s.tables == 0 and (s.canvas + s.svg) == 0:
        s.flags.append("NO-VISUAL (no table/chart/svg)")
    if s.empathy_hits == 0:
        s.flags.append("NO-EMPATHY")
    interactive = s.inputs_numeric + s.inputs_range + s.selects + s.buttons
    if interactive == 0:
        s.flags.append("NO-INTERACTIVE")
    if s.dollar_examples < 5 and s.percent_examples < 3:
        s.flags.append("LOW-EXAMPLES (<5 $ and <3 %)")
    if s.generic_hits >= 3:
        s.flags.append(f"GENERIC-PHRASES ({s.generic_hits})")
    if s.type_token_ratio and s.type_token_ratio < 0.35:
        s.flags.append(f"REPETITIVE (TTR {s.type_token_ratio})")
    if s.h2_count + s.h3_count < 4:
        s.flags.append("THIN-STRUCTURE (<4 H2/H3)")

    return s


def severity(s: PageStats) -> int:
    """Higher = needs more remediation work."""
    score = 0
    score += max(0, (700 - s.body_words)) // 50       # thin → +1 per 50 words below 700
    score += max(0, int(60 - s.flesch_reading_ease))  # hard → +1 per FRE point below 60
    score += 5 if s.tables == 0 and (s.canvas + s.svg) == 0 else 0
    score += 5 if (s.inputs_numeric + s.inputs_range + s.selects + s.buttons) == 0 else 0
    score += 4 if s.empathy_hits == 0 else 0
    score += 3 if s.generic_hits >= 3 else 0
    score += 3 if s.dollar_examples < 5 else 0
    score += 2 if s.h2_count + s.h3_count < 4 else 0
    return score


def fmt_row(s: PageStats) -> str:
    interactive = s.inputs_numeric + s.inputs_range + s.selects + s.buttons
    visuals = s.tables + s.canvas + s.svg
    return (
        f"| {severity(s):>3} | {s.body_words:>5} | {s.flesch_reading_ease:>5} | "
        f"{s.flesch_kincaid_grade:>4} | {s.h2_count}/{s.h3_count} | "
        f"{visuals:>2} | {interactive:>3} | {s.faq_jsonld:>2} | "
        f"{s.dollar_examples:>3} | {s.percent_examples:>3} | "
        f"{s.empathy_hits:>3} | {s.generic_hits:>2} | "
        f"`{s.path}` | {', '.join(s.flags) or '—'} |"
    )


def main() -> int:
    pages = sorted(p for p in ROOT.rglob("*.html") if "__pycache__" not in p.parts)
    all_stats: list[PageStats] = []
    for p in pages:
        try:
            stats = analyze(p)
        except Exception as e:
            print(f"ERROR analyzing {p}: {e}", file=sys.stderr)
            continue
        all_stats.append(stats)

    content_stats = [s for s in all_stats if not s.is_stub]
    stubs = [s for s in all_stats if s.is_stub]

    content_stats.sort(key=lambda s: (-severity(s), s.body_words))

    lines: list[str] = []
    lines.append("# SEO Content-Depth Audit\n")
    lines.append(
        f"_Audited {len(content_stats)} content pages "
        f"(+ {len(stubs)} redirect stubs skipped)._\n"
    )
    lines.append(
        "Sort order: highest **severity score** first "
        "(thinner + harder-to-read + fewer visuals/examples = higher score)."
    )
    lines.append("")
    lines.append("**Column legend**")
    lines.append("- **Sev**: severity score (higher = more work needed)")
    lines.append("- **Words**: body word count (excludes nav/footer/scripts)")
    lines.append("- **FRE**: Flesch Reading Ease (target > 60)")
    lines.append("- **FK**: Flesch-Kincaid Grade Level (lower = easier; ~8 is ideal)")
    lines.append("- **H2/H3**: heading counts")
    lines.append("- **Vis**: visual elements (tables + canvas + svg)")
    lines.append("- **Int**: interactive elements (numeric/range inputs + selects + buttons)")
    lines.append("- **FAQ**: FAQ JSON-LD entries")
    lines.append("- **$ / %**: dollar amounts and percentages mentioned in copy")
    lines.append("- **Emp**: empathy markers (\"what this means\", \"your\", \"if you\")")
    lines.append("- **Gen**: AI-generic boilerplate phrase hits")
    lines.append("")
    lines.append(
        "| Sev | Words |   FRE |   FK | H2/H3 | Vis | Int | FAQ |   $ |   % | Emp | Gen | Page | Flags |"
    )
    lines.append(
        "|----:|------:|------:|-----:|:-----:|----:|----:|----:|----:|----:|----:|----:|------|-------|"
    )
    for s in content_stats:
        lines.append(fmt_row(s))

    if stubs:
        lines.append("")
        lines.append("## Skipped (redirect stubs)\n")
        for s in stubs:
            lines.append(f"- `{s.path}`")

    # Summary stats
    if content_stats:
        avg_words = sum(s.body_words for s in content_stats) / len(content_stats)
        avg_fre = sum(s.flesch_reading_ease for s in content_stats) / len(content_stats)
        thin = sum(1 for s in content_stats if "THIN (<600 words)" in s.flags)
        hard = sum(1 for s in content_stats if any(f.startswith("HARD-TO-READ") for f in s.flags))
        no_visual = sum(1 for s in content_stats if "NO-VISUAL (no table/chart/svg)" in s.flags)
        no_inter = sum(1 for s in content_stats if "NO-INTERACTIVE" in s.flags)
        low_ex = sum(1 for s in content_stats if "LOW-EXAMPLES (<5 $ and <3 %)" in s.flags)
        generic = sum(1 for s in content_stats if any(f.startswith("GENERIC-PHRASES") for f in s.flags))
        lines.append("")
        lines.append("## Summary\n")
        lines.append(f"- Avg body words: **{avg_words:.0f}**")
        lines.append(f"- Avg Flesch Reading Ease: **{avg_fre:.1f}** (target > 60)")
        lines.append(f"- Pages flagged THIN (<600 words): **{thin}**")
        lines.append(f"- Pages flagged HARD-TO-READ (FRE < 60): **{hard}**")
        lines.append(f"- Pages without a table/chart/svg visual: **{no_visual}**")
        lines.append(f"- Pages without any interactive element: **{no_inter}**")
        lines.append(f"- Pages with LOW-EXAMPLES (<5 $ and <3 %): **{low_ex}**")
        lines.append(f"- Pages with 3+ AI-generic phrases: **{generic}**")

    report = "\n".join(lines) + "\n"
    out = ROOT / "seo-audit.md"
    out.write_text(report, encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)} ({len(content_stats)} pages, {len(stubs)} stubs skipped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
