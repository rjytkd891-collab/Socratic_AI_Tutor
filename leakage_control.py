import re


LEAKAGE_PATTERNS = [
    r"\bviết\s+(?:hộ|giùm|thay)\b",
    r"\b(?:làm|giải)\s+(?:hộ|giùm|thay)\b",
    r"\b(?:cho|đưa)\s+(?:tôi|mình|em|tớ|cậu)?\s*đáp án\b",
    r"\bđáp án\s+(?:hoàn chỉnh|cuối cùng)\b",
    r"\b(?:bài văn|bài nghị luận)\s+hoàn chỉnh\b",
    r"\bdàn ý\s+(?:chi tiết|hoàn chỉnh|đầy đủ)\b",
    r"\b(?:làm|viết)\s+toàn bộ\s+(?:bài|bài tập)\b",
    r"\bchỉ cần\s+(?:đưa|cho)\s+(?:tôi|mình|em|tớ)?\s*đáp án\b",
]


def is_answer_leakage_request(text: str) -> bool:
    if not isinstance(text, str) or not text.strip():
        return False

    normalized = re.sub(r"\s+", " ", text.lower()).strip()

    return any(
        re.search(pattern, normalized, flags=re.IGNORECASE)
        for pattern in LEAKAGE_PATTERNS
    )


def leakage_redirect() -> str:
    return (
        "Tớ không làm toàn bộ bài thay cậu, "
        "nhưng tớ có thể giúp cậu tự xây dựng câu trả lời từng bước. "
        "Trước tiên, theo cậu, yêu cầu quan trọng nhất của đề bài là gì?"
    )
