import streamlit as st
from socratic_engine import SocraticEngine

st.set_page_config(
    page_title="Socratic AI Tutor",
    page_icon="🌱",
    layout="centered",
)

# GIAO DIEN: LORA + BE VIETNAM PRO
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap');

    html, body, .stApp,
    [class*="css"], p, div, span,
    label, input, textarea, button {
        font-family: 'Be Vietnam Pro', Arial, sans-serif !important;
    }

    h1, h2, h3 {
        font-family: 'Lora', Georgia, serif !important;
        font-weight: 600;
    }

    .stApp {
        background-color: #F8F7F2;
        color: #26352E;
    }

    [data-testid="stSidebar"] {
        background-color: #E8EEE7;
    }

    [data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border: 1px solid #E1E7DF;
        border-radius: 14px;
        padding: 1rem;
        line-height: 1.8;
    }

    textarea, input {
        font-family: 'Be Vietnam Pro', Arial, sans-serif !important;
    }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #B7C7B8;
        color: #26352E;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# TIEU DE
st.title("Socratic AI Tutor")

st.caption(
    "Tư duy sâu hơn qua câu hỏi · "
    "Tự lập luận · Tự hình thành câu trả lời"
)

# THANH BEN: GIOI THIEU DU AN
with st.sidebar:
    st.header("Về dự án")

    st.write(
        "Socratic AI Tutor là gia sư gợi mở, "
        "giúp người học tự suy nghĩ thay vì nhận "
        "ngay đáp án hoàn chỉnh."
    )

    st.subheader("5 cấp độ câu hỏi")

    st.markdown(
        """
        1. **Làm rõ vấn đề**
        2. **Khám phá giả định**
        3. **Phân tích bằng chứng**
        4. **Góc nhìn đa chiều**
        5. **Đánh giá và tổng hợp**
        """
    )

    st.caption(
        "AI hỗ trợ tư duy; người học vẫn là "
        "người đưa ra kết luận."
    )

    if st.button("↻ Bắt đầu mới", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# KHOI TAO TRO CHUYEN
if "messages" not in st.session_state:
    st.session_state.messages = []

if "engine" not in st.session_state:
    st.session_state.engine = SocraticEngine()

# KHUNG CHAT
st.subheader("Không gian trò chuyện")

st.write(
    "Hãy chia sẻ câu hỏi hoặc suy nghĩ của cậu. "
    "Mình sẽ đồng hành bằng những câu hỏi gợi mở."
)

# HIEN THI LICH SU CHAT
for message in st.session_state.messages:
    avatar = "🌱" if message["role"] == "assistant" else "👤"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# NHAN CAU HOI
question = st.chat_input(
    "Nhập câu hỏi hoặc chia sẻ suy nghĩ của cậu..."
)

if question:
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    history = st.session_state.messages.copy()

    with st.chat_message("assistant", avatar="🌱"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            for chunk in st.session_state.engine.ask_stream(
                question=question,
                history=history,
            ):
                full_response += chunk

                response_placeholder.markdown(
                    full_response + "▌"
                )

            response_placeholder.markdown(full_response)

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response,
                }
            )

        except Exception as error:
            error_text = str(error).lower()

            if (
                "429" in error_text
                or "resource_exhausted" in error_text
                or "quota" in error_text
            ):
                st.warning(
                    "AI đã chạm giới hạn lượt gọi. "
                    "Cậu chờ một lúc rồi thử lại nhé."
                )

            elif (
                "503" in error_text
                or "unavailable" in error_text
            ):
                st.warning(
                    "Dịch vụ AI đang bận. "
                    "Cậu thử lại sau một chút nhé."
                )

            elif (
                "timeout" in error_text
                or "deadline_exceeded" in error_text
            ):
                st.warning(
                    "AI phản hồi quá thời gian chờ. "
                    "Cậu thử lại nhé."
                )

            else:
                st.error(
                    "Có lỗi khi tạo câu trả lời: "
                    + str(error)
                )