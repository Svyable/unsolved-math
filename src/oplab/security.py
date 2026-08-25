from collections.abc import Iterable

SUSPICIOUS_MARKERS: tuple[str, ...] = (
    "<script",
    "javascript:",
    "ignore previous instructions",
    "ignore all previous instructions",
    "system prompt",
    "developer message",
    "curl | sh",
    "wget | sh",
    "rm -rf",
)


def contains_instruction_like_content(values: Iterable[object]) -> bool:
    """Flag imported text that deserves review; never interpret it as instructions."""

    text = "\n".join(str(value) for value in values if value is not None).casefold()
    return any(marker in text for marker in SUSPICIOUS_MARKERS)
