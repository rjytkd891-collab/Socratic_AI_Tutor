import time
import random

import streamlit as st
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT
from leakage_control import (
    is_answer_leakage_request,
    leakage_redirect,
)
from evaluator import evaluate_level, LEVELS


class SocraticEngine:

    def __init__(self):
        api_key = st.secrets.get("GEMINI_API_KEY", "")

        if not api_key:
            raise ValueError(
                "Không tìm thấy GEMINI_API_KEY trong Secrets."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.8-flash"

        # Số lần thử lại tối đa sau lần gọi đầu tiên
        self.max_retries = 2

    def get_level(self, student_answer: str) -> int:
        return evaluate_level(student_answer)

    def _is_temporary_error(self, error):
        """Nhận diện các lỗi có thể thử lại."""
        message = str(error).lower()

        temporary_markers = [
            "503",
            "429",
            "500",
            "502",
            "504",
            "unavailable",
            "resource_exhausted",
            "too many requests",
            "deadline exceeded",
            "timed out",
            "timeout",
            "connection reset",
            "connection error",
            "temporarily",
        ]

        return any(
            marker in message
            for marker in temporary_markers
        )

    def ask_stream(self, question, history=None):

        if not question or not question.strip():
            return

        # 1. Chặn yêu cầu đòi đáp án hoàn chỉnh
        if is_answer_leakage_request(question):
            yield leakage_redirect()
            return

        # 2. Ước lượng cấp độ Socratic trên máy
        level = evaluate_level(question)
        level_name = LEVELS[level]

        # 3. Lấy lịch sử gần nhất
        recent_history = (history or [])[-6:]

        contents = []

        for message in recent_history:
            role = message.get("role")
            content = message.get("content", "")

            if role not in ("user", "assistant"):
                continue

            if not isinstance(content, str) or not content.strip():
                continue

            api_role = (
                "user" if role == "user" else "model"
            )

            contents.append(
                types.Content(
                    role=api_role,
                    parts=[
                        types.Part.from_text(text=content)
                    ],
                )
            )

        # 4. Hướng dẫn phản hồi
        instruction = f"""
CẤP ĐỘ SOCRATIC ĐƯỢC ĐỀ XUẤT:
Cấp {level}/5 — {level_name}

Dựa vào câu trả lời và lịch sử để điều chỉnh cấp độ
nếu cần. Không tăng cấp chỉ vì học sinh trả lời thêm một lượt.

NGUYÊN TẮC:
- Không làm bài thay học sinh.
- Không đưa đáp án hoàn chỉnh hoặc bài văn để chép.
- Ưu tiên giúp học sinh tự suy nghĩ và lập luận.
- Mỗi lượt tập trung vào một vấn đề chính.
- Đặt một câu hỏi gợi mở rõ ràng.
- Nếu học sinh bế tắc, đưa một gợi ý nhỏ rồi hỏi tiếp.
- Nếu có bằng chứng, yêu cầu học sinh phân tích ý nghĩa.
- Nếu lập luận tốt, mở rộng sang góc nhìn khác hoặc đánh giá.
- Không bịa chi tiết tác phẩm hay dẫn chứng.
- Không xem mọi yêu cầu giải thích kiến thức là gian lận.

PHONG CÁCH:
Tiếng Việt tự nhiên, gần gũi, ngắn gọn.
Thường trả lời trong 2–5 câu.
"""

        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=question.strip()
                    )
                ],
            )
        )

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT + instruction,
            thinking_config=types.ThinkingConfig(
                thinking_level="low"
            ),
            max_output_tokens=200,
        )

        # 5. Thử lại có giới hạn khi gặp lỗi tạm thời
        for attempt in range(self.max_retries + 1):

            try:
                stream = self.client.models.generate_content_stream(
                    model=self.model,
                    contents=contents,
                    config=config,
                )

                received_text = False

                for chunk in stream:
                    if chunk.text:
                        received_text = True
                        yield chunk.text

                # Nếu đã trả lời được thì kết thúc
                if received_text:
                    return

                # Không nhận được nội dung: thử lại nếu còn lượt
                if attempt < self.max_retries:
                    time.sleep(
                        (2 ** attempt) + random.uniform(0, 0.5)
                    )
                    continue

                yield (
                    "Gemini chưa trả về nội dung. "
                    "Cậu thử gửi lại câu hỏi sau nhé."
                )
                return

            except Exception as error:

                # Không thử lại các lỗi không có tính tạm thời
                if not self._is_temporary_error(error):
                    raise

                # Đã hết số lần thử
                if attempt >= self.max_retries:
                    yield (
                        "Gemini đang quá tải hoặc đã chạm hạn mức. "
                        "Cậu đợi một chút rồi gửi lại nhé."
                    )
                    return

                # Chờ tăng dần: khoảng 1–1,5 giây, rồi 2–2,5 giây
                wait_seconds = (
                    2 ** attempt
                ) + random.uniform(0, 0.5)

                time.sleep(wait_seconds)
