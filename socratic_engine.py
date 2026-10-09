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
                "Không tìm thấy GEMINI_API_KEY trong secrets.toml"
            )

        self.client = genai.Client(api_key=api_key)

        self.model = "gemini-3.7-flash"

    def get_level(self, student_answer: str) -> int:
        return evaluate_level(student_answer)

    def ask_stream(self, question, history=None):

        if not question or not question.strip():
            return

        # 1. Chống lộ đáp án trước khi gọi API
        if is_answer_leakage_request(question):
            yield leakage_redirect()
            return

        # 2. Xác định cấp độ ngay trên máy
        level = evaluate_level(question)
        level_name = LEVELS[level]

        # 3. Chỉ lấy một phần lịch sử gần nhất
        recent_history = (history or [])[-6:]

        contents = []

        for message in recent_history:
            role = message.get("role")
            content = message.get("content", "")

            if role not in ("user", "assistant"):
                continue

            if not content.strip():
                continue

            api_role = "user" if role == "user" else "model"

            contents.append(
                types.Content(
                    role=api_role,
                    parts=[
                        types.Part.from_text(text=content)
                    ],
                )
            )

        # 4. Hướng dẫn Gemini tạo câu hỏi phù hợp
        instruction = f"""
CẤP ĐỘ SOCRATIC ĐƯỢC ĐỀ XUẤT:
Cấp {level}/5 — {level_name}

Hãy sử dụng cấp độ này làm định hướng.

Tuy nhiên, hãy đọc toàn bộ câu trả lời và lịch sử gần nhất
để điều chỉnh nếu cần.

NHIỆM VỤ:
- Không làm bài thay học sinh.
- Không đưa đáp án hoàn chỉnh.
- Không viết bài văn hoàn chỉnh.
- Không tạo dàn ý chi tiết để học sinh chép.
- Ưu tiên giúp học sinh tự suy nghĩ.
- Chỉ tập trung vào một vấn đề chính.
- Đặt một câu hỏi gợi mở rõ ràng.
- Nếu học sinh đang bế tắc, đưa một gợi ý rất nhỏ trước câu hỏi.
- Nếu học sinh đã có bằng chứng, hãy yêu cầu phân tích ý nghĩa của bằng chứng.
- Nếu học sinh đã lập luận tốt, hãy mở rộng sang góc nhìn khác hoặc đánh giá.
- Không bịa thông tin hoặc dẫn chứng.

Độ dài:
2–5 câu, ưu tiên ngắn gọn để phản hồi nhanh.
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

        # 5. Gọi Gemini DUY NHẤT 1 lần
        stream = self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT + instruction,

                thinking_config=types.ThinkingConfig(
                    thinking_level="low"
                ),

                max_output_tokens=200,
            ),
        )

        # 6. Streaming: trả từng phần ngay khi Gemini tạo ra
        for chunk in stream:

            if chunk.text:
                yield chunk.text
