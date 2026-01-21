from docx import Document
from .txt_md import parse_txt_md
from .base import ParsedContent, ParseError


def parse_docx(file_path: str) -> ParsedContent:
    try:
        document = Document(file_path)
    except Exception as e:
        raise ParseError(f"Failed to read DOCX file: {e}")

    lines = [p.text for p in document.paragraphs]
    text = "\n".join(lines)

    return parse_txt_md(text)