from dataclasses import dataclass
from typing import Optional

class ParseError(Exception):
    pass

@dataclass
class ParsedContent:
    title: str
    content: str
    image: Optional[str] = None