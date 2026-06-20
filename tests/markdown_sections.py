"""Shared markdown section utilities for constitution regression tests."""


def get_section(content: str, heading: str, heading_prefix: str) -> str:
    start = content.index(heading)
    next_heading = content.find(f"\n{heading_prefix}", start + len(heading))
    if next_heading == -1:
        return content[start:]
    return content[start:next_heading]
