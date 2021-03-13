from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    preamble: str
    content: str