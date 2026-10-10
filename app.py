
import streamlit as st
from socratic_engine import SocraticEngine


# ==================================================
# 1. CAU HINH TRANG
# ==================================================

st.set_page_config(
    page_title="Socratic AI Tutor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# 2. KHOI TAO SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "engine" not in st.session_state:
    try:
        st.session_state.engine = SocraticEngine()
    except Exception as error:
        st.error(
            "Không thể khởi tạo AI. "
            "Hãy kiểm tra API Key trong Streamlit Secrets."
        )
        st.caption(str(error))
        st.stop()


# ==================================================
# 3. GIAO DIEN VA FONT CHU
# ==================================================

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap'
    );

    /* Mau sac chung */
    :root {
        --sage: #718873;
        --sage-dark: #405845;
        --sage-light: #E8EEE7;
        --cream: #F8F7F2;
        --white: #FFFFFF;
        --text: #26352E;
        --muted: #68766A;
        --border: #DDE5DC;
    }

    /* Font va nen */
    html, body, .stApp,
    [class*="css"],
    p, div, span, label,
    input, textarea, button {
        font-family: 'Be Vietnam Pro', Arial, sans-serif;
    }

    .stApp {
        background-color: var(--cream);
        color: var(--text);
    }

    /* An nen header mac dinh */
    header[data-testid="stHeader"] {
        background-color: transparent;
    }

    /* Khung noi dung */
    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* Tieu de mang phong cach van hoc */
    h1, h2, h3 {
        font-family: 'Lora', Georgia, serif !important;
        color: var(--sage-dark);
        font-weight: 600;
    }

    h1 {
        font-size: 2.25rem;
        line-height: 1.35;
    }

    h2 {
        font-size: 1.65rem;
    }

    h3 {
        font-size: 1.3rem;
    }

    p, li {
        line-height: 1.8;
    }

    /* Thanh ben */
    section[data-testid="stSidebar"] {
        background-color: var(--sage-light);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li {
        color: var(--text);
    }

    /* Tin nhan */
    [data-testid="stChatMessage"] {
        background-color: var(--white);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.8rem;
    }

    [data-testid="stChatMessage"] p {
        font-size: 1rem;
        line-height: 1.85;
        overflow-wrap: anywhere;
    }

    /* O nhap tin nhan */
    [data-testid="stChatInput"] {
        border-color: var(--border);
        border-radius: 16px;
    }

    [data-testid="stChatInput"] textarea {
        font-family: 'Be Vietnam Pro', Arial, sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.6;
    }

    /* Nut bam */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid #B7C7B8;
        color: var(--sage-dark);
        background-color: var(--white);
        min-height: 2.7rem;
        font-family: 'Be Vietnam Pro', Arial, sans-serif;
    }

    .stButton > button:hover {
        border-color: var(--sage);
        color: var(--sage-dark);
    }

    /* Khung chao mung */
    .welcome-note {
        background-color: #EEF2EA;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.4rem;
        margin-top: 1rem;
        margin-bottom: 1.4rem;
    }

    .welcome-note h3 {
        margin-top: 0;
        margin-bottom: 0.6rem;
    }

    .welcome-note p {
        color: #536357;
        margin-bottom: 0;
    }

    /* Hien thi tren dien thoai */
    @media (max-width: 768px) {
        .block-container {
            padding: 1.2rem 1rem 5rem 1rem;
        }

        h1 {
            font-size: 1.8rem !important;
        }

        h2 {
            font-size: 1.4rem !important;
        }

        h3 {
            font-size: 1.15rem !important;
        }

        [data-testid="stChatMessage"] {
            padding: 0.8rem;
            border-radius: 13px;
        }

        [data-testid="stChatMessage"] p {
            font-size: 0.95rem;
        }

        .welcome-note {
            padding: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# 4. THANH BEN - THONG TIN DU AN
# ==================================================

with st.sidebar:
    st.markdown("## 🌱 Socratic AI Tutor")
    st.caption("Không đưa đáp án ngay — cùng người học tìm ra câu trả lời.")

    st.divider()

    st.subheader("Về dự án")

    st.write(
        "Socratic AI Tutor là gia sư AI gợi mở, "
        "hướng dẫn học sinh tự suy nghĩ, tự lập luận "
        "và hình thành câu trả lời."
    )

    st.subheader("5 cấp độ câu hỏi")

    st.markdown(
        """
        **1. Làm rõ vấn đề**

        Xác định điều đang cần tìm hiểu.

        **2. Khám phá giả định**

        Nhận diện những điều đang được xem là hiển nhiên.

        **3. Phân tích bằng chứng**

        Kiểm tra lí lẽ và căn cứ.

        **4. Góc nhìn đa chiều**

        Xem xét những cách giải thích khác.

        **5. Đánh giá và tổng hợp**

        Rút ra kết luận có cơ sở.
        """
    )

    st.divider()

    st.caption(
        "AI là người đồng hành trong quá trình học tập. "
        "Người học vẫn là người suy nghĩ và đưa ra kết luận."
    )

    if st.button("↻ Bắt đầu cuộc trò chuyện mới", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ==================================================
# 5. TIEU DE CHINH
# ==================================================

st.title("Socratic AI Tutor")

st.caption(
    "Tư duy sâu hơn qua câu hỏi · "
    "Tự lập luận · Tự hình thành câu trả lời"
)

st.divider()

st.subheader("Không gian trò chuyện")

st.write(
    "Hãy chia sẻ câu hỏi hoặc suy nghĩ của cậu. "
    "Mình sẽ đồng hành bằng những câu hỏi gợi mở."
)


# ==================================================
# 6. MAN CHAO MUNG KHI CHUA CO TIN NHAN
# ==================================================

if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-note">
            <h3>Chào cậu, mình cùng bắt đầu nhé.</h3>
            <p>
            Cậu không cần có sẵn câu trả lời hoàn chỉnh.
            Hãy bắt đầu từ điều cậu đang băn khoăn,
            một ý kiến chưa chắc chắn hoặc một đoạn văn
            muốn hiểu sâu hơn.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# 7. HIEN THI LICH SU TRO CHUYEN
# ==================================================

for message in st.session_state.messages:
    if message["role"] == "user":
        avatar = "👤"
    else:
        avatar = "🌱"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# ==================================================
# 8. NHAN CAU HOI VA GOI SOCRATIC ENGINE
# ==================================================

question = st.chat_input(
    "Nhập câu hỏi hoặc chia sẻ suy nghĩ của cậu..."
)

if question:
    # Lich su cu duoc gui cho AI de duy tri mach hoi thoai.
    history = st.session_state.messages.copy()

    # Hien thi cau hoi cua nguoi dung.
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    # Goi AI va hien thi cau tra loi dang streaming.
    with st.chat_message("assistant", avatar="🌱"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            for chunk in st.session_state.engine.ask_stream(
                question=question,
                history=history,
            ):
                if chunk:
                    full_response += chunk
                    response_placeholder.markdown(
                        full_response + " ▌"
                    )

            # Hoan tat phan hien thi.
            if full_response.strip():
                response_placeholder.markdown(full_response)

                # Chi luu hoi thoai sau khi AI tra loi thanh cong.
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
            else:
                response_placeholder.warning(
                    "AI chưa tạo được nội dung trả lời. "
                    "Cậu thử gửi lại nhé."
                )

        except Exception as error:
            # Xu ly mot so loi API pho bien.
            error_text = str(error).lower()

            if (
                "429" in error_text
                or "resource_exhausted" in error_text
                or "quota" in error_text
            ):
                response_placeholder.warning(
                    "AI đã chạm giới hạn lượt gọi. "
                    "Cậu chờ một lúc rồi thử lại nhé."
                )

            elif (
                "503" in error_text
                or "unavailable" in error_text
            ):
                response_placeholder.warning(
                    "Dịch vụ AI đang bận. "
                    "Cậu thử lại sau một chút nhé."
                )

            elif (
                "timeout" in error_text
                or "deadline_exceeded" in error_text
            ):
                response_placeholder.warning(
                    "AI phản hồi quá thời gian chờ. "
                    "Cậu thử lại nhé."
                )

            else:
                response_placeholder.error(
                    "Có lỗi khi tạo câu trả lời."
                )
                st.caption(str(error))

