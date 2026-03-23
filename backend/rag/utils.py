import re

MAIN_SECTION_PATTERN = re.compile(r"^\s*(\d+)-\s+(.+)$", re.MULTILINE)
SUBSECTION_PATTERN   = re.compile(r"^\s*(\d+\.\d+)\s+(.+)$", re.MULTILINE)
PAGE_MARKER_PATTERN  = re.compile(r"\[\[PAGE_(\d+)\]\]")

def clean_page_text(text: str) -> str:
    text = re.sub(r"Politique RH\s*-\s*Version\s*1", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def strip_page_markers(text: str) -> str:
    text = PAGE_MARKER_PATTERN.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()