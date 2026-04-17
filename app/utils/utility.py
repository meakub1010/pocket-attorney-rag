import re
from pypdf import PdfReader
from io import BytesIO

def extract_pdf_text(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)


def clean_text(text: str) -> str:
    # ─────────────────────────────────────────────
    # 1. Remove headers (dates + title repetition)
    # ─────────────────────────────────────────────
    text = re.sub(
        r'\d{2}/\d{2}/\d{4}.*?Bangladesh\n',
        '',
        text
    )

    # ─────────────────────────────────────────────
    # 2. Remove URLs and page markers
    # ─────────────────────────────────────────────
    text = re.sub(r'bdlaws\.minlaw\.gov\.bd[^\n]*', '', text)
    text = re.sub(r'\b\d+/\d+\b', '', text)

    # ─────────────────────────────────────────────
    # 3. Remove standalone numbers (footnotes/pages)
    # ─────────────────────────────────────────────
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

    # ─────────────────────────────────────────────
    # 4. Fix weird apostrophes and spacing
    # ─────────────────────────────────────────────
    text = text.replace("   ’", "’")
    text = re.sub(r'\s{2,}', ' ', text)

    # ─────────────────────────────────────────────
    # 5. Fix broken lines inside sentences
    # (join lines that shouldn't be split)
    # ─────────────────────────────────────────────
    text = re.sub(r'\n(?=[a-z,\)])', ' ', text)

    # ─────────────────────────────────────────────
    # 6. Fix broken titles (e.g., "Equality\nbefore law")
    # Join Capitalized lines split across newline
    # ─────────────────────────────────────────────
    text = re.sub(r'([A-Za-z])\n([a-z])', r'\1 \2', text)

    # ─────────────────────────────────────────────
    # 7. Normalize clause formatting
    # Ensure clauses start on new line
    # ─────────────────────────────────────────────
    text = re.sub(r'\s*\((\d+[A-Z]?)\)', r'\n(\1)', text)

    # ─────────────────────────────────────────────
    # 8. Normalize article formatting
    # Ensure "1. ..." starts on new line
    # ─────────────────────────────────────────────
    text = re.sub(r'\n?(\d+[A-Z]?\.)\s+', r'\n\1 ', text)

    # ─────────────────────────────────────────────
    # 9. Clean excessive newlines
    # ─────────────────────────────────────────────
    text = re.sub(r'\n{3,}', '\n\n', text)

    # ─────────────────────────────────────────────
    # 10. Trim
    # ─────────────────────────────────────────────
    return text.strip()

# ── Utility ──────────────────────────────────────────────────────────
def _clean(self, text: str) -> str:
    # Remove page headers (repeated site URL lines)
    text = re.sub(r'bdlaws\.minlaw\.gov\.bd.*\n', '', text)
    text = re.sub(r'\d+/\d+/\d+.*Constitution.*\n', '', text)
    # Remove footnote blocks at page bottoms
    text = re.sub(r'bdlaws\.minlaw\.gov\.bd/act-print-367\.html\s+\d+/\d+', '', text)
    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def _make_breadcrumb(self, part, chapter, article, title) -> str:
    parts = [p for p in [part, chapter, f"Article {article}"] if p]
    crumb = " > ".join(parts)
    if title:
        crumb += f" ({title})"
    return crumb

def _infer_title(self, body: str) -> str:
    """Use first short line as title if no marginal map entry."""
    first = body.strip().split('\n')[0]
    return first[:60] if len(first) < 80 else ""

def _token_count(self, text: str) -> int:
    return len(text.split())   # rough estimate; swap for tiktoken if needed