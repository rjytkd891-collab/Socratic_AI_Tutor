
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

if "draft_question" not in st.session_state:
    st.session_state.draft_question = ""

if "draft_version" not in st.session_state:
    st.session_state.draft_version = 0

if "show_project" not in st.session_state:
    st.session_state.show_project = False

if "engine" not in st.session_state:
    try:
        st.session_state.engine = SocraticEngine()
    except Exception as error:
        st.error("Không thể khởi tạo AI. Hãy kiểm tra API Key.")
        st.caption(str(error))
        st.stop()

# ==================================================
# 3. CSS - GIAO DIEN
# ==================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap');

    :root {
        --cream: #F8F5EC;
        --paper: #FFFCF5;
        --sage-light: #E7EEDF;
        --sage: #A6B99A;
        --sage-dark: #708969;
        --forest: #354D38;
        --ink: #29352B;
        --muted: #596653;
        --border: #DADFCF;
    }

    html, body, .stApp,
    [class*="css"],
    p, div, span, label,
    input, textarea, button {
        font-family: 'Be Vietnam Pro', Arial, sans-serif;
    }

    .stApp {
        background: var(--cream);
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(248, 245, 236, 0.96);
    }

    .block-container {
        max-width: 1250px;
        padding: 1.2rem 1.5rem 3rem;
    }

    h1, h2, h3 {
        font-family: 'Lora', Georgia, serif !important;
        color: var(--forest);
        font-weight: 600;
    }

    p {
        line-height: 1.75;
    }

    /* Tieu de */
    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 16px;
    }

    .brand-icon {
        font-size: 32px;
    }

    .brand-name {
        font-family: 'Lora', Georgia, serif;
        font-size: clamp(23px, 3vw, 34px);
        font-weight: 600;
        color: var(--forest);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg, #E5EBDD 0%, #DCE5D5 100%
        );
        border-right: 1px solid #D3DDCC;
    }

    .mascot-card {
        background: var(--paper);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 16px 10px;
        text-align: center;
        margin-bottom: 16px;
    }

    .mascot {
        font-size: 52px;
        line-height: 1.3;
    }

    .mascot-title {
        font-family: 'Lora', Georgia, serif;
        font-size: 19px;
        font-weight: 600;
        color: var(--forest);
    }

    .mascot-subtitle {
        font-size: 12px;
        color: var(--muted);
        margin-top: 4px;
    }

    /* Banner */
    .banner {
        position: relative;
        overflow: hidden;
        background: linear-gradient(
            110deg, #DFE9D8 0%, #F5EFDE 55%, #E8EBDD 100%
        );
        border: 1px solid #DCE2D3;
        border-radius: 22px;
        padding: 25px;
        min-height: 145px;
        margin-bottom: 16px;
    }

    .banner-title {
        font-family: 'Lora', Georgia, serif;
        font-size: clamp(25px, 3vw, 38px);
        font-weight: 600;
        color: var(--forest);
        margin-bottom: 8px;
    }

    .banner-subtitle {
        font-size: 14px;
        color: #435540;
        max-width: 75%;
    }

    .banner-art {
        position: absolute;
        right: 24px;
        bottom: 12px;
        font-size: 58px;
    }

    /* Welcome */
    .welcome-card {
        background: linear-gradient(
            135deg, #F4F3E8, #EAF0E4
        );
        border: 1px solid #E0E5D8;
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0 16px;
    }

    .welcome-title {
        font-family: 'Lora', Georgia, serif;
        font-size: 24px;
        font-weight: 600;
        color: var(--forest);
        margin-bottom: 5px;
    }

    .welcome-text {
        font-size: 14px;
        color: #435540;
    }

    /* Chat bubbles */
    [data-testid="stChatMessage"] {
        background: var(--paper);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }

    [data-testid="stChatMessage"] p {
        color: #29352B;
        font-size: 15px;
        line-height: 1.85;
        overflow-wrap: anywhere;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background: var(--paper);
        border: 1px solid var(--border);
        border-radius: 15px;
        margin-bottom: 14px;
    }

    [data-testid="stExpander"] summary {
        color: var(--forest);
        font-weight: 600;
    }

    /* Buttons */
    .stButton > button {
        min-height: 45px;
        white-space: normal;
        border: 1px solid #DEDCCB;
        border-radius: 14px;
        background: var(--paper);
        color: var(--ink);
        transition: background-color 0.15s ease;
    }

    .stButton > button:hover {
        background: #E9F0E3;
        border-color: #B7C9AE;
        color: var(--forest);
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: #FDFBF5;
        border-color: #D2DDCA;
        color: var(--forest);
    }

    /* Form input */
    div[data-testid="stForm"] {
        background: var(--paper);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 12px;
    }

    div[data-testid="stForm"] textarea {
        font-family: 'Be Vietnam Pro', Arial, sans-serif !important;
        font-size: 15px !important;
        line-height: 1.7;
        color: var(--ink);
    }

    .section-label {
        font-family: 'Lora', Georgia, serif;
        font-size: 19px;
        font-weight: 600;
        color: var(--forest);
        margin: 18px 0 10px;
    }

    /* Mobile */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.8rem 0.75rem 2rem;
        }

        .brand {
            gap: 8px;
            margin-bottom: 12px;
        }

        .brand-icon {
            font-size: 27px;
        }

        .brand-name {
            font-size: 24px;
        }

        .banner {
            padding: 16px;
            min-height: 120px;
            border-radius: 17px;
        }

        .banner-title {
            font-size: 24px;
            max-width: 78%;
        }

        .banner-subtitle {
            font-size: 12px;
            max-width: 78%;
        }

        .banner-art {
            right: 10px;
            bottom: 10px;
            font-size: 37px;
        }

        .welcome-card {
            padding: 15px;
            border-radius: 16px;
        }

        .welcome-title {
            font-size: 21px;
        }

        .welcome-text {
            font-size: 13px;
        }

        [data-testid="stChatMessage"] {
            padding: 10px;
            border-radius: 15px;
        }

        [data-testid="stChatMessage"] p {
            font-size: 14px;
            line-height: 1.8;
        }

        .stButton > button {
            font-size: 13px;
            min-height: 44px;
        }

        div[data-testid="stForm"] {
            padding: 8px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# 4. TIEU DE
# ==================================================
st.markdown(
    """
    <div class="brand">
        <div class="brand-icon">🌱</div>
        <div class="brand-name">Socratic AI Tutor</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# 5. SIDEBAR
# ==================================================
with st.sidebar:
    st.markdown(
        """
        <div class="mascot-card">
            <div class="mascot">🐱</div>
            <div class="mascot-title">Socratic AI Tutor</div>
            <div class="mascot-subtitle">Gia sư gợi mở</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("💬  Trò chuyện", use_container_width=True):
        st.session_state.show_project = False
        st.rerun()

    if st.button("📖  Về dự án", use_container_width=True):
        st.session_state.show_project = not st.session_state.show_project

    if st.button("＋  Cuộc trò chuyện mới", use_container_width=True):
        st.session_state.messages = []
        st.session_state.draft_question = ""
        st.session_state.draft_version += 1
        st.session_state.show_project = False
        st.rerun()

    if st.session_state.show_project:
        st.markdown("### Về dự án")
        st.write(
            "Socratic AI Tutor hỗ trợ học sinh tự suy nghĩ, "
            "tự lập luận và tự hình thành câu trả lời."
        )

    st.divider()
    st.markdown("### Lịch sử gần đây")

    previous_questions = [
        message["content"]
        for message in st.session_state.messages
        if message["role"] == "user"
    ]

    if previous_questions:
        for old_question in reversed(previous_questions[-5:]):
            label = old_question[:45]
            if len(old_question) > 45:
                label += "…"
            st.caption("• " + label)
    else:
        st.caption("Chưa có câu hỏi nào.")

# ==================================================
# 6. BANNER
# ==================================================
st.markdown(
    """
    <div class="banner">
        <div class="banner-title">Socratic AI Tutor</div>
        <div class="banner-subtitle">
            Tư duy sâu hơn qua câu hỏi · Tự lập luận · Tự hình thành câu trả lời
        </div>
        <div class="banner-art">📚</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# 7. 5 CAP DO SOCRATIC - THU GON
# ==================================================
with st.expander(
    "🔍 Xem 5 cấp độ câu hỏi Socratic của Trợ lý",
    expanded=False,
):
    level_col1, level_col2 = st.columns(2)

    with level_col1:
        st.markdown("**1. Làm rõ vấn đề**")
        st.caption("Xác định điều đang được hỏi.")

        st.markdown("**2. Khám phá giả định**")
        st.caption("Nhận diện những điều đang được xem là hiển nhiên.")

        st.markdown("**3. Phân tích bằng chứng**")
        st.caption("Kiểm tra căn cứ, dẫn chứng và lí lẽ.")

    with level_col2:
        st.markdown("**4. Góc nhìn đa chiều**")
        st.caption("Xem xét các quan điểm khác nhau.")

        st.markdown("**5. Đánh giá hệ quả**")
        st.caption("Cân nhắc hệ quả và rút ra kết luận.")

# ==================================================
# 8. LOI CHAO
# ==================================================
if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-title">Chào cậu! 🌿</div>
            <div class="welcome-text">
                Cậu muốn tìm hiểu điều gì hôm nay?
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==================================================
# 9. HIEN THI LICH SU CHAT
# ==================================================
for message in st.session_state.messages:
    avatar = "🌱" if message["role"] == "assistant" else "🐾"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ==================================================
# 10. GOI Y NHANH - CHI LA PHAN MO DAU
# ==================================================
if not st.session_state.messages:
    st.markdown(
        '<div class="section-label">Gợi ý bắt đầu</div>',
        unsafe_allow_html=True,
    )

    prompt_col1, prompt_col2 = st.columns(2)

    with prompt_col1:
        if st.button(
            "💡 Tớ đang muốn phân tích...",
            use_container_width=True,
        ):
            st.session_state.draft_question = "Tớ đang muốn phân tích "
            st.session_state.draft_version += 1
            st.rerun()

        if st.button(
            "✍️ Tớ đang tìm dẫn chứng về...",
            use_container_width=True,
        ):
            st.session_state.draft_question = "Tớ đang tìm dẫn chứng về "
            st.session_state.draft_version += 1
            st.rerun()

    with prompt_col2:
        if st.button(
            "🤔 Tớ chưa biết bắt đầu từ đâu...",
            use_container_width=True,
        ):
            st.session_state.draft_question = (
                "Tớ chưa biết bắt đầu từ đâu khi "
            )
            st.session_state.draft_version += 1
            st.rerun()

        if st.button(
            "💬 Tớ muốn tìm hiểu thêm về...",
            use_container_width=True,
        ):
            st.session_state.draft_question = (
                "Tớ muốn tìm hiểu thêm về "
            )
            st.session_state.draft_version += 1
            st.rerun()

# ==================================================
# 11. O NHAP TUY CHINH
# Dung form de hoc sinh sua va bo sung cau goi y
# ==================================================
st.markdown('<div class="section-label">Trò chuyện</div>', unsafe_allow_html=True)

with st.form(
    key=f"question_form_{st.session_state.draft_version}",
    clear_on_submit=True,
):
    question_input = st.text_area(
        "Câu hỏi của cậu",
        value=st.session_state.draft_question,
        placeholder="Nhập câu hỏi hoặc chia sẻ suy nghĩ của cậu...",
        height=90,
        label_visibility="collapsed",
    )

    send_clicked = st.form_submit_button(
        "Gửi câu hỏi  ➤",
        use_container_width=True,
    )

if send_clicked and question_input.strip():
    question = question_input.strip()
    history = st.session_state.messages.copy()
    st.session_state.draft_question = ""

    with st.chat_message("user", avatar="🐾"):
        st.markdown(question)

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

            if full_response.strip():
                response_placeholder.markdown(full_response)

                st.session_state.messages.append(
                    {"role": "user", "content": question}
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
            else:
                response_placeholder.warning(
                    "AI chưa tạo được câu trả lời. Cậu thử lại nhé."
                )

        except Exception as error:
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
            elif "503" in error_text or "unavailable" in error_text:
                response_placeholder.warning(
                    "Dịch vụ AI đang bận. Cậu thử lại sau nhé."
                )
            elif "timeout" in error_text or "deadline_exceeded" in error_text:
                response_placeholder.warning(
                    "AI phản hồi quá thời gian chờ. Cậu thử lại nhé."
                )
            else:
                response_placeholder.error(
                    "Có lỗi khi tạo câu trả lời."
                )
                st.caption(str(error))

elif send_clicked:
    st.warning("Cậu nhập thêm nội dung rồi hãy gửi nhé.")

