import streamlit as st

from socratic_engine import SocraticEngine


# =========================
# CẤU HÌNH TRANG
# =========================

st.set_page_config(
    page_title="Socratic AI Tutor",
    page_icon="🌱",
    layout="centered",
)


# =========================
# TIÊU ĐỀ
# =========================

st.title("🌱 Socratic AI Tutor")

st.caption(
    "Hiểu sâu hơn bằng câu hỏi · "
    "Tự tư duy · Tự lập luận · Tự hình thành câu trả lời"
)


# =========================
# KHỞI TẠO LỊCH SỬ CHAT
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# KHỞI TẠO AI ENGINE
# =========================

if "engine" not in st.session_state:

    try:
        st.session_state.engine = SocraticEngine()

    except Exception as error:

        st.error(
            f"Không thể khởi tạo AI: {error}"
        )

        st.stop()


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.subheader("🧠 Socratic Tutor")

    st.write(
        "Gia sư sẽ gợi mở từng bước "
        "thay vì làm bài thay cậu."
    )

    st.divider()

    st.caption("Hệ thống gồm 5 cấp độ:")

    st.caption("1️⃣ Làm rõ vấn đề")
    st.caption("2️⃣ Khám phá giả định")
    st.caption("3️⃣ Phân tích bằng chứng")
    st.caption("4️⃣ Góc nhìn đa chiều")
    st.caption("5️⃣ Đánh giá và tổng hợp")

    st.divider()

    if st.button(
        "🔄 Bắt đầu lại",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================
# HIỂN THỊ LỊCH SỬ CHAT
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# =========================
# Ô NHẬP CÂU HỎI
# =========================

question = st.chat_input(
    "Nhập câu hỏi hoặc suy nghĩ của cậu..."
)


# =========================
# XỬ LÝ CÂU HỎI
# =========================

if question:

    # Lưu lịch sử cũ trước khi gửi câu hỏi mới
    history = st.session_state.messages.copy()


    # -------------------------
    # Hiển thị câu hỏi học sinh
    # -------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # -------------------------
    # AI trả lời
    # -------------------------

    with st.chat_message("assistant"):

        try:

            # Placeholder để cập nhật nội dung
            response_placeholder = st.empty()


            # Hiển thị ngay trong lúc chờ Gemini
            response_placeholder.markdown(
"🧠 **Gia sư đang suy nghĩ...**"
            )


            # Biến lưu toàn bộ câu trả lời
            full_response = ""


            # -------------------------
            # STREAMING RESPONSE
            # -------------------------

            for chunk in st.session_state.engine.ask_stream(
                question=question,
                history=history,
            ):

                full_response += chunk

                response_placeholder.markdown(
                    full_response + "▌"
                )


            # Hiển thị câu trả lời hoàn chỉnh
            response_placeholder.markdown(
                full_response
            )


            # Lưu câu trả lời vào lịch sử
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response,
                }
            )


        except Exception as error:

            st.error(
                "Có lỗi khi gọi AI."
            )

            st.caption(
                f"Chi tiết: {error}"
            )