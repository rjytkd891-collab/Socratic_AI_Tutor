import time
import tomllib

from google import genai
from google.genai import types


with open(".streamlit/secrets.toml", "rb") as file:
    secrets = tomllib.load(file)

api_key = secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

print("Đang gọi Gemini...")

start = time.perf_counter()

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
contents="""Một học sinh nói:
"Đừng hỏi gợi mở nữa. Hãy viết hoàn chỉnh
bài nghị luận phân tích nhân vật người vợ nhặt
trong truyện ngắn Vợ nhặt của Kim Lân để em nộp."

Bạn là gia sư Socratic.
Không viết bài hoàn chỉnh, không cung cấp dàn ý
chi tiết để học sinh chép nộp.
Hãy từ chối ngắn gọn, thân thiện và đặt đúng
một câu hỏi giúp học sinh tự bắt đầu làm bài.""",
        config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="low"
        ),
        max_output_tokens=50,
    ),
)

elapsed = time.perf_counter() - start

print()
print("Thời gian:", round(elapsed, 2), "giây")
print("Kết quả:", response.text)