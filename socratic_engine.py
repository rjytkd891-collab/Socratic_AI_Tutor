import os
import random
import time
import streamlit as st
from google import genai
from google.genai import types


# ==========================================
# SOCRATIC SYSTEM PROMPT
# ==========================================

SOCRATIC_SYSTEM_PROMPT = """
Bạn là Socratic AI Tutor, một gia sư Ngữ văn THPT
tâm huyết, kiên nhẫn và gần gũi.

MỤC TIÊU:
Dẫn dắt học sinh tự tư duy, tự lập luận và tự hình thành
câu trả lời thay vì làm bài thay học sinh.

I. NGUYÊN TẮC SƯ PHẠM
- Không viết sẵn toàn bộ bài văn để học sinh chép.
- Được giải thích kiến thức, gợi ý dàn ý và phân tích từng phần.
- Ưu tiên câu hỏi gợi mở phù hợp với câu trả lời của học sinh.
- Không phán xét khi học sinh chưa biết.
- Giao tiếp tự nhiên, thân thiện, phù hợp học sinh THPT.

II. CHỐNG LẶP CÂU TRẢ LỜI
- Khi cần từ chối yêu cầu làm bài thay, chỉ từ chối một lần
  bằng tối đa một câu ngắn gọn.
- Không diễn đạt lại cùng một lời từ chối nhiều lần.
- Sau lời từ chối, chuyển ngay sang một gợi ý cụ thể
  hoặc một câu hỏi Socratic liên quan.
- Không lặp nguyên văn câu hỏi hoặc luận điểm vừa nêu.
- Mỗi lượt ưu tiên một câu hỏi trọng tâm.
- Nếu học sinh nói không biết, hãy chia nhỏ vấn đề,
  đưa ra một gợi ý dễ hiểu hoặc hai phương án lựa chọn.
- Không hỏi lại điều học sinh đã trả lời rõ ràng.

III. XỬ LÝ YÊU CẦU XIN ĐÁP ÁN
Nếu học sinh yêu cầu viết toàn bộ bài văn hoặc làm bài thay:
- Không tạo bài hoàn chỉnh để học sinh chép nguyên văn.
- Chỉ từ chối ngắn gọn một lần.
- Có thể hướng dẫn lập dàn ý, tìm luận điểm,
  phân tích dẫn chứng hoặc xây dựng từng đoạn.
- Kết thúc bằng một câu hỏi cụ thể giúp học sinh bắt đầu.

IV. NĂM CẤP ĐỘ SOCRATIC
1. Làm rõ vấn đề: xác định yêu cầu, đối tượng và chi tiết.
2. Khám phá giả định: nhận diện giả định và động cơ.
3. Phân tích bằng chứng: tìm dẫn chứng và giải thích.
4. Góc nhìn đa chiều: xem xét cách diễn giải khác.
5. Đánh giá và tổng hợp: kết nối luận điểm, rút ra kết luận.

Chọn cấp độ phù hợp, không bắt buộc đi tuần tự
qua cả năm cấp độ trong mọi cuộc hội thoại.

V. ĐỘ CHÍNH XÁC
- Không bịa dẫn chứng, câu thơ hoặc chi tiết tác phẩm.
- Nếu không chắc chắn, hãy nói rõ và đề nghị học sinh
  cung cấp đoạn trích cần phân tích.
- Phân biệt thông tin trong văn bản với cách diễn giải.

VI. CÁCH PHẢN HỒI
- Ghi nhận ý kiến của học sinh khi phù hợp.
- Đưa ra gợi ý vừa đủ để học sinh tiến thêm một bước.
- Ưu tiên một câu hỏi gợi mở cụ thể.
- Nếu học sinh chỉ chào hỏi, hãy đáp lại tự nhiên.
- Nếu học sinh hỏi kiến thức cụ thể, có thể giải thích
  ngắn gọn trước khi đặt câu hỏi tiếp theo.

MỤC TIÊU CUỐI CÙNG:
Giúp học sinh tự hiểu, tự lập luận và tự hình thành
câu trả lời, không biến cuộc trò chuyện thành chuỗi
từ chối lặp lại hoặc câu hỏi máy móc.
"""


# ==========================================
# SOCRATIC ENGINE
# ==========================================

class SocraticEngine:

    def __init__(self):

        # Lấy danh sách API Keys từ Streamlit Secrets
        self.api_keys = st.secrets.get("API_KEYS", [])

        if isinstance(self.api_keys, str):
            self.api_keys = [self.api_keys]

        # Dự phòng một API Key riêng lẻ
        if not self.api_keys:
            single_key = (
                st.secrets.get("GEMINI_API_KEY")
                or os.environ.get("GEMINI_API_KEY")
            )

            if single_key:
                self.api_keys = [single_key]
            else:
                raise ValueError(
                    "Chưa cấu hình API Key trong Streamlit Secrets!"
                )

        # Loại bỏ key rỗng và key trùng
        self.api_keys = list(dict.fromkeys(
            key.strip()
            for key in self.api_keys
            if isinstance(key, str) and key.strip()
        ))

        if not self.api_keys:
            raise ValueError("Danh sách API Key không hợp lệ.")

    def get_client(self, api_key):
        return genai.Client(api_key=api_key)

    def ask_stream(self, question: str, history: list):

        # Chỉ giữ 8 tin nhắn lịch sử gần nhất
        recent_history = history[-8:]

        contents = []

        for msg in recent_history:
            role = (
                "user"
                if msg["role"] == "user"
                else "model"
            )

            contents.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(
                            text=msg["content"]
                        )
                    ],
                )
            )

        # Thêm câu hỏi hiện tại
        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=question)
                ],
            )
        )

        # Thử các key theo thứ tự ngẫu nhiên
        keys_to_try = self.api_keys.copy()
        random.shuffle(keys_to_try)

        last_error = None

        for index, api_key in enumerate(keys_to_try):

            try:
                client = self.get_client(api_key)

                response_stream = client.models.generate_content_stream(
                    model="gemini-3.8-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SOCRATIC_SYSTEM_PROMPT,
                        temperature=0.7,
                    ),
                )

                stream_iterator = iter(response_stream)

                # Chỉ chuyển key khác nếu lỗi xảy ra
                # trước khi nhận được nội dung đầu tiên
                try:
                    first_chunk = next(stream_iterator)
                except StopIteration:
                    return

                if first_chunk.text:
                    yield first_chunk.text

                # Đã bắt đầu trả lời thì không đổi key giữa chừng
                for chunk in stream_iterator:
                    if chunk.text:
                        yield chunk.text

                return

            except Exception as error:

                last_error = error
                error_text = str(error).lower()

                # Các lỗi có thể thử lại bằng key khác
                retryable = any(
                    marker in error_text
                    for marker in (
                        "429",
                        "resource_exhausted",
                        "quota",
                        "500",
                        "internal",
                        "502",
                        "503",
                        "unavailable",
                        "504",
                        "deadline_exceeded",
                        "timeout",
                    )
                )

                # Lỗi cấu hình hoặc lỗi không thuộc nhóm trên:
                # không thử key khác một cách vô ích
                if not retryable:
                    raise

                # Chờ ngắn giữa các lần thử
                if index < len(keys_to_try) - 1:
                    time.sleep(0.5)
                    continue

        # Tất cả key đều không thành công
        if last_error:
            raise last_error
