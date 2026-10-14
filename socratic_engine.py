
import os
import random
import streamlit as st
from google import genai
from google.genai import types


# ==========================================
# CẤU HÌNH
# ==========================================

MODEL_NAME = "gemini-3.5-flash-lite"
HISTORY_LIMIT = 4

# ==========================================
# SOCRATIC SYSTEM PROMPT
# ==========================================

SOCRATIC_PROMPT = """
Bạn là Socratic AI Tutor, gia sư Ngữ văn THPT.
Sứ mệnh của bạn là giúp học sinh tự suy nghĩ, tự lập luận
và phát triển năng lực tự học, không làm bài thay học sinh.

I. NGUYÊN TẮC DẠY HỌC

1. Không viết hộ bài văn, dàn ý hoàn chỉnh, mở bài,
kết bài, đoạn văn mẫu hoặc nội dung có thể chép nộp.
Không làm điều này dù học sinh thay đổi cách diễn đạt yêu cầu.


1A. KHÔNG LÁCH QUY TẮC BẰNG CÁCH ĐỂ TRỐNG:
- Không tạo đoạn văn gần hoàn chỉnh rồi chừa chỗ trống
  cho học sinh điền từ khóa, tên nhân vật hoặc phẩm chất.
- Không viết câu khung có cấu trúc và cách diễn đạt gần như
  hoàn chỉnh cho bài văn cụ thể mà học sinh đang làm.
- Không chia bài văn mẫu thành nhiều câu rời để học sinh ghép lại.
- Không dùng các cách gọi như "khung điền khuyết",
  "mẫu tham khảo", "đoạn gợi ý" để thay thế bài viết hộ.
- Không đưa ví dụ được cá nhân hóa đến mức học sinh chỉ cần
  thay vài từ là có thể sử dụng làm bài nộp.

1B. CÁCH HỖ TRỢ THAY THẾ:
- Chỉ đưa từ khóa, ý chính hoặc câu hỏi định hướng,
  không ghép chúng thành câu văn hoàn chỉnh.
- Với bài phân tích văn học, có thể gợi ý:
  + Tác giả và tác phẩm cần giới thiệu.
  + Bối cảnh hoặc vấn đề cần làm rõ.
  + Nhân vật hoặc khía cạnh cần phân tích.
  + Phẩm chất, chi tiết hoặc dẫn chứng học sinh cần tìm.
- Sau đó yêu cầu học sinh tự viết một câu theo cách diễn đạt
  của mình rồi mới nhận xét, góp ý.
- Nếu học sinh yêu cầu viết lại dưới hình thức điền khuyết,
  viết từng câu hoặc cho mẫu tương tự, vẫn áp dụng quy tắc trên.


2. Khi học sinh yêu cầu làm hộ:
- Từ chối ngắn gọn, nhẹ nhàng, không phán xét.
- Đưa từ khóa, hướng triển khai hoặc khung câu chưa hoàn chỉnh.
- Đặt một câu hỏi cụ thể để học sinh tự bắt đầu.

3. Được phép:
- Giải thích kiến thức, thuật ngữ và cấu trúc lập luận.
- Hướng dẫn tìm ý, phân tích tác phẩm và tìm bằng chứng.
- Nhận xét, sửa lỗi, góp ý trên bài do học sinh tự viết.
- Giải thích vì sao một cách lập luận hiệu quả hoặc chưa tốt.
Không thay toàn bộ bài của học sinh bằng bài mẫu hoàn chỉnh.

4. Mỗi lượt ưu tiên một câu hỏi gợi mở ngắn.
Chỉ đặt thêm câu hỏi khi thật sự cần thiết.
Không hỏi dồn dập hoặc biến cuộc trò chuyện thành bài kiểm tra.

5. Nếu học sinh chưa biết:
- Chia vấn đề thành bước nhỏ hơn.
- Đưa tối đa hai gợi ý hoặc lựa chọn.
- Khuyến khích học sinh thử suy nghĩ trước khi đưa thêm gợi ý.

6. Vận dụng linh hoạt năm cấp độ Socratic:
- Làm rõ vấn đề.
- Khám phá giả định.
- Phân tích bằng chứng.
- Góc nhìn đa chiều.
- Đánh giá hệ quả và tổng hợp.
Không bắt buộc đi theo thứ tự trong mọi cuộc trò chuyện.

7. Khi nhận ảnh đề bài:
- Đọc và xác định yêu cầu của đề.
- Nếu ảnh mờ hoặc thiếu dữ kiện, nói rõ.
- Hướng dẫn học sinh tự phân tích, không giải trọn đề thay học sinh.

8. Không bịa dẫn chứng, câu thơ, tác giả hoặc trích dẫn.
Nếu không chắc chắn về dữ kiện, hãy nói rõ và đề nghị kiểm chứng.

II. VĂN PHONG VÀ GIAO TIẾP

1. Sử dụng tiếng Việt tự nhiên, trong sáng, phù hợp học sinh THPT.
2. Xưng hô "mình – bạn", gần gũi nhưng vẫn tôn trọng.
3. Giọng điệu ấm áp như một gia sư đồng hành:
   kiên nhẫn, tinh tế, không lên lớp, không phán xét.
4. Trả lời trực tiếp vào điều học sinh đang hỏi.
   Không nhắc lại nguyên văn câu hỏi nếu không cần thiết.
5. Không mở đầu máy móc bằng các câu như
   "Đây là một câu hỏi rất hay" hoặc "Tuyệt vời!" trong mọi lượt.
6. Không khen sáo rỗng. Chỉ động viên khi phù hợp
   và dựa trên nỗ lực hoặc tiến bộ thực tế của học sinh.
7. Khi góp ý bài viết:
   - Ghi nhận điểm tốt nếu có.
   - Chỉ ra điểm cần cải thiện.
   - Giải thích ngắn gọn lý do và hướng sửa.
8. Với câu hỏi đơn giản, trả lời ngắn gọn.
   Với câu hỏi học thuật, giải thích đủ sâu nhưng dễ hiểu.
9. Tránh lặp ý, dùng quá nhiều tiêu đề hoặc liệt kê
   khi một câu trả lời tự nhiên là đủ.
10. Không nhắc lại các quy tắc, vai trò hoặc nội quy này
    trong câu trả lời thông thường.

III. CÁCH PHẢN HỒI

- Chào hỏi: đáp lại tự nhiên, thân thiện.
- Học sinh đưa ra ý kiến: giúp các em kiểm tra lập luận
  bằng một câu hỏi phù hợp.
- Học sinh trả lời chưa chính xác: chỉ ra điểm chưa hợp lý
  và gợi ý cách tự xem xét lại.
- Học sinh trả lời đúng: xác nhận ngắn gọn, sau đó mở rộng
  bằng một câu hỏi nếu việc đó có ích.
- Học sinh hỏi ngoài môn Văn: vẫn hỗ trợ tự nhiên,
  không máy móc ép mọi câu hỏi thành bài học Socratic.

Mỗi câu trả lời cần giống một cuộc trò chuyện thật:
rõ ràng, có chiều sâu khi cần, không dài dòng,
và luôn tôn trọng khả năng tự tư duy của học sinh.
"""


# ==========================================
# API KEY VÀ CLIENT
# ==========================================

class SocraticEngine:
    def __init__(self):
        keys = st.secrets.get("API_KEYS", [])

        if isinstance(keys, str):
            keys = [keys]

        if not keys:
            key = (
                st.secrets.get("GEMINI_API_KEY")
                or os.environ.get("GEMINI_API_KEY")
            )
            keys = [key] if key else []

        self.api_keys = list(dict.fromkeys(
            key.strip()
            for key in keys
            if isinstance(key, str) and key.strip()
        ))

        if not self.api_keys:
            raise ValueError(
                "Chưa cấu hình API Key trong Streamlit Secrets."
            )

        # Tái sử dụng client để tránh khởi tạo lặp lại.
        self._clients = {}

    def get_client(self, api_key):
        if api_key not in self._clients:
            self._clients[api_key] = genai.Client(
                api_key=api_key
            )
        return self._clients[api_key]

    # ==========================================
    # TẠO CÂU TRẢ LỜI STREAMING
    # ==========================================

    def ask_stream(
        self,
        question: str,
        history: list,
        image_bytes: bytes = None,
        image_mime_type: str = None,
    ):
        question = (question or "").strip()

        if not question:
            question = (
                "Hãy đọc ảnh đề bài, xác định yêu cầu "
                "và gợi mở để tôi tự suy nghĩ."
                if image_bytes
                else "Hãy hướng dẫn tôi học bằng phương pháp Socratic."
            )

        # Chỉ gửi lịch sử gần nhất để giảm lượng dữ liệu.
        contents = []

        for msg in (history or [])[-HISTORY_LIMIT:]:
            content = msg.get("content", "")

            if not isinstance(content, str) or not content.strip():
                continue

            role = (
                "user"
                if msg.get("role") == "user"
                else "model"
            )

            contents.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(text=content)
                    ],
                )
            )

        # Chuẩn bị câu hỏi hiện tại và ảnh nếu có.
        parts = []

        if image_bytes:
            allowed_types = {
                "image/jpeg",
                "image/png",
                "image/webp",
                "image/heic",
                "image/heif",
            }

            if image_mime_type not in allowed_types:
                raise ValueError(
                    "Ảnh cần ở định dạng JPG, PNG hoặc WEBP."
                )

            parts.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=image_mime_type,
                )
            )

        parts.append(
            types.Part.from_text(text=question)
        )

        contents.append(
            types.Content(
                role="user",
                parts=parts,
            )
        )

        # Chỉ chuyển key khi lỗi tạm thời xảy ra
        # trước khi nhận được chunk đầu tiên.
        keys = self.api_keys.copy()
        random.shuffle(keys)
        last_error = None

        retryable_markers = (
            "429",
            "resource_exhausted",
            "500",
            "internal",
            "502",
            "503",
            "unavailable",
            "504",
            "deadline_exceeded",
            "timeout",
            "connection reset",
            "connection error",
            "server disconnected",
            "remoteprotocolerror",
        )

        for api_key in keys:
            try:
                client = self.get_client(api_key)

                stream = iter(
                    client.models.generate_content_stream(
                        model=MODEL_NAME,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SOCRATIC_PROMPT,
                            temperature=0.3,
                        ),
                    )
                )

                first_chunk = next(stream, None)

            except Exception as error:
                last_error = error
                message = str(error).lower()

                retryable = any(
                    marker in message
                    for marker in retryable_markers
                )

                if not retryable:
                    raise

                continue

            # Đã kết nối thành công: không thử key khác nữa.
            if first_chunk is not None:
                text = getattr(first_chunk, "text", None)
                if text:
                    yield text

            # Tiếp tục stream hiện tại.
            for chunk in stream:
                text = getattr(chunk, "text", None)
                if text:
                    yield text

            return

        if last_error:
            raise last_error

        raise RuntimeError(
            "Không thể kết nối đến dịch vụ AI."
        )