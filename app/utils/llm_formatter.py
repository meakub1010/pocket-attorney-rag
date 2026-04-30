import re
from typing import Dict


class LLMFormatter:
    @staticmethod
    def format_to_markdown(text: str) -> Dict:
        """
        Converts raw LLM text into structured Markdown-friendly format.
        """

        # Normalize line breaks
        text = text.replace("\\n", "\n").strip()

        # Split paragraphs
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        # Try to detect bullet points
        bullets = []
        cleaned_paragraphs = []

        for p in paragraphs:
            if p.startswith("*") or p.startswith("-"):
                bullets.append(p)
            else:
                cleaned_paragraphs.append(p)

        # Build markdown answer
        markdown = ""

        for p in cleaned_paragraphs:
            markdown += p + "\n\n"

        if bullets:
            markdown += "### Key Points\n\n"
            for b in bullets:
                markdown += f"- {b.lstrip('*- ').strip()}\n"

        return {
            "answer_markdown": markdown.strip(),
            "answer_text": text,
            "has_bullets": len(bullets) > 0,
        }
