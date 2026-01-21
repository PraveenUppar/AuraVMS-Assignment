import re
from typing import List
from .base import ParsedContent, ParseError

def _strip_leading_empty_lines(lines: List[str]) -> List[str]:
    while lines and not lines[0].strip():
        lines.pop(0)
    return lines

def _is_image_reference(line: str) -> bool:
    markdown_image_pattern = r"!\[.*?\]\(.*?\)"
    return (
        re.match(markdown_image_pattern, line.strip()) is not None
        or line.strip().startswith("http://")
        or line.strip().startswith("https://")
    )

def parse_txt_md(text: str) -> ParsedContent:
    
    if not text.strip():
        raise ParseError("File is empty")

    lines = text.splitlines()
    lines = _strip_leading_empty_lines(lines)

    if not lines:
        raise ParseError("No content found")
    
    image = None

    if _is_image_reference(lines[0]):
        image = lines.pop(0).strip()
        lines = _strip_leading_empty_lines(lines)

    if not lines:
        raise ParseError("Missing title")

    title = lines.pop(0).strip()

    if not title:
        raise ParseError("Title cannot be empty")

    content = "\n".join(lines).strip()

    return ParsedContent(
        title=title,
        content=content,
        image=image
    )