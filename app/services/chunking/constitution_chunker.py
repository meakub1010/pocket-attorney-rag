import re
from dataclasses import dataclass, field


@dataclass
class ConstitutionChunk:
    text: str
    metadata: dict = field(default_factory=dict)

    def embed_text(self) -> str:
        """Text to actually embed — breadcrumb + content"""
        crumb = self.metadata.get("breadcrumb", "")
        title = self.metadata.get("article_title", "")
        header = f"{crumb}\n{title}\n\n" if crumb else ""
        return header + self.text


class BangladeshConstitutionChunker:
    # ── Regex patterns matching this exact document ──────────────────────
    PART_RE = re.compile(r"^PART\s+(I{1,3}V?|VI{0,3}|XI?A?)\b", re.MULTILINE)
    CHAPTER_RE = re.compile(r"^CHAPTER\s+(I{1,3}V?|VI{0,3}|IIA?)\b", re.MULTILINE)

    # Matches: "27.", "2A.", "47A.", "141B." etc.
    ARTICLE_RE = re.compile(
        r"^(\d+[A-Z]?)\.\s+(.+?)(?=^\d+[A-Z]?\.\s|\Z)", re.MULTILINE | re.DOTALL
    )

    # Left-column marginal titles like "Equality\nbefore law"
    # In this PDF they appear as lines before or beside article numbers
    # We detect them by looking for short ALL-CAPS or Title Case lines
    MARGINAL_RE = re.compile(r"^([A-Z][a-zA-Z ,\-]+)\n(\d+[A-Z]?)\.", re.MULTILINE)

    # Footnote markers at end of document — strip these
    FOOTNOTE_RE = re.compile(r"^\d+\n.+?(?=^\d+\n|\Z)", re.MULTILINE | re.DOTALL)

    # Amendment notes like "[Substituted by...]" inline
    AMEND_RE = re.compile(r"\[\d+\]|\d+\s*$", re.MULTILINE)

    def __init__(self, max_clause_tokens: int = 400):
        self.max_clause_tokens = max_clause_tokens

    # ── Public entry point ───────────────────────────────────────────────
    def chunk(self, raw_text: str) -> list[ConstitutionChunk]:
        text = self._clean(raw_text)
        chunks = []

        current_part = None
        current_chapter = None
        current_article = None
        current_title = None

        # Build marginal title lookup: article_num -> title
        marginal_map = {}
        for m in self.MARGINAL_RE.finditer(text):
            marginal_map[m.group(2)] = m.group(1).strip()

        # Split into article blocks
        article_blocks = self._split_articles(text)

        for art_num, art_body in article_blocks:
            # Update part / chapter context from text before this article
            part_match = self.PART_RE.search(art_body)
            if part_match:
                current_part = part_match.group(0).strip()

            chap_match = self.CHAPTER_RE.search(art_body)
            if chap_match:
                current_chapter = chap_match.group(0).strip()

            # Article title from marginal map or first line heuristic
            art_title = marginal_map.get(art_num) or self._infer_title(art_body)

            breadcrumb = self._make_breadcrumb(
                current_part, current_chapter, art_num, art_title
            )

            base_meta = {
                "part": current_part,
                "chapter": current_chapter,
                "article": art_num,
                "article_title": art_title,
                "breadcrumb": breadcrumb,
                "source": "Bangladesh Constitution",
            }

            # Split long articles into clause-level chunks
            clause_chunks = self._split_clauses(art_body, base_meta)
            chunks.extend(clause_chunks)

        return chunks

    # ── Splitting helpers ────────────────────────────────────────────────
    def _split_articles(self, text: str) -> list[tuple[str, str]]:
        """Returns [(article_number, article_body), ...]"""
        results = []
        matches = list(self.ARTICLE_RE.finditer(text))
        for i, m in enumerate(matches):
            art_num = m.group(1)
            art_body = m.group(2).strip()
            results.append((art_num, art_body))
        return results

    def _split_clauses(self, art_body: str, base_meta: dict) -> list[ConstitutionChunk]:
        """Split article into clause-level chunks if it's long."""
        # Clause pattern: (1), (2), (2A) ...
        clause_re = re.compile(r"\((\d+[A-Z]?)\)\s+", re.MULTILINE)
        clauses = clause_re.split(art_body)

        # If no clauses or short enough — keep as one chunk
        if len(clauses) <= 1 or self._token_count(art_body) < self.max_clause_tokens:
            return [
                ConstitutionChunk(
                    text=art_body.strip(),
                    metadata={**base_meta, "clause": None, "chunk_type": "article"},
                )
            ]

        chunks = []
        # clauses = [preamble, clause_num, clause_text, clause_num, clause_text, ...]
        preamble = clauses[0].strip()
        it = iter(clauses[1:])
        for clause_num, clause_text in zip(it, it):
            clause_text = clause_text.strip()
            if not clause_text:
                continue

            # Sub-clause splitting: (a), (b), (c)
            sub_chunks = self._split_subclauses(clause_num, clause_text, base_meta)
            chunks.extend(sub_chunks)

        return chunks

    def _split_subclauses(
        self, clause_num: str, clause_text: str, base_meta: dict
    ) -> list[ConstitutionChunk]:
        """Further split into sub-clauses (a), (b), (c) if too long."""
        sub_re = re.compile(r"\(([a-z])\)\s+")
        parts = sub_re.split(clause_text)

        if len(parts) <= 1 or self._token_count(clause_text) < self.max_clause_tokens:
            return [
                ConstitutionChunk(
                    text=clause_text,
                    metadata={
                        **base_meta,
                        "clause": clause_num,
                        "sub_clause": None,
                        "chunk_type": "clause",
                        "breadcrumb": base_meta["breadcrumb"]
                        + f" > Clause ({clause_num})",
                    },
                )
            ]

        chunks = []
        intro = parts[0].strip()
        it = iter(parts[1:])
        for sub_letter, sub_text in zip(it, it):
            full_text = f"({sub_letter}) {sub_text.strip()}"
            if intro:
                full_text = intro + "\n" + full_text  # keep parent clause context

            chunks.append(
                ConstitutionChunk(
                    text=full_text,
                    metadata={
                        **base_meta,
                        "clause": clause_num,
                        "sub_clause": sub_letter,
                        "chunk_type": "sub_clause",
                        "breadcrumb": (
                            base_meta["breadcrumb"]
                            + f" > Clause ({clause_num})(sub-clause {sub_letter})"
                        ),
                    },
                )
            )
        return chunks
