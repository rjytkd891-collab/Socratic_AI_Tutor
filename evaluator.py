import re


LEVELS = {
    1: "Làm rõ vấn đề",
    2: "Khám phá giả định",
    3: "Phân tích bằng chứng",
    4: "Góc nhìn đa chiều",
    5: "Đánh giá và tổng hợp",
}


def evaluate_level(student_answer: str) -> int:
    """
    Ước lượng cấp độ Socratic phù hợp.
    Đây là bộ lọc nhanh chạy ngay trên máy,
    không gọi Gemini nên gần như không tạo thêm độ trễ.
    """

    if not student_answer or not student_answer.strip():
        return 1

    text = re.sub(r"\s+", " ", student_answer.lower()).strip()

    if len(text) < 20:
        return 1

    has_claim = any(
        x in text
        for x in [
            "em nghĩ",
            "mình nghĩ",
            "tớ nghĩ",
            "theo em",
            "theo mình",
            "theo tớ",
            "em cho rằng",
            "mình cho rằng",
            "tớ cho rằng",
            "em thấy",
            "mình thấy",
        ]
    )

    has_evidence = any(
        x in text
        for x in [
            "chi tiết",
            "hình ảnh",
            "câu thơ",
            "từ ngữ",
            "dẫn chứng",
            "câu văn",
            "đoạn thơ",
            "tác giả viết",
            "tác giả sử dụng",
            "cho thấy",
        ]
    )

    has_multiple_views = any(
        x in text
        for x in [
            "tuy nhiên",
            "mặt khác",
            "một cách hiểu khác",
            "góc nhìn khác",
            "ngược lại",
            "không chỉ",
            "đồng thời",
            "có thể hiểu",
        ]
    )

    has_evaluation = any(
        x in text
        for x in [
            "qua đó",
            "từ đó",
            "điều này cho thấy",
            "ý nghĩa",
            "đóng góp",
            "chủ đề",
            "giá trị",
            "thông điệp",
            "nhận xét",
        ]
    )

    if has_evaluation and has_multiple_views and has_evidence:
        return 5

    if has_multiple_views and has_evidence:
        return 4

    if has_evidence:
        return 3

    if has_claim:
        return 2

    return 1
