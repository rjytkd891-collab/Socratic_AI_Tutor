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
        st.error("Không thể khởi tạo AI.")

        with st.expander("🔧 Chi tiết lỗi kỹ thuật"):
            st.code(str(error))

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
        st.markdown(message["content"])


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

    # Lưu lịch sử trước lượt hỏi mới
    history = st.session_state.messages.copy()

    # Hiển thị câu hỏi của học sinh
    with st.chat_message("user"):
        st.markdown(question)

    # AI trả lời
    with st.chat_message("assistant"):

        response_placeholder = st.empty()
        full_response = ""

        try:

            # Hiển thị trạng thái chờ
            response_placeholder.markdown(
                "🧠 **Gia sư đang suy nghĩ...**"
            )

            # =========================
            # STREAMING RESPONSE
            # =========================

            for chunk in st.session_state.engine.ask_stream(
                question=question,
                history=history,
            ):

                if chunk:
                    full_response += chunk

                    response_placeholder.markdown(
                        full_response + "▌"
                    )

            # =========================
            # HOÀN TẤT PHẢN HỒI
            # =========================

            if full_response.strip():

                response_placeholder.markdown(
                    full_response
                )

                # Chỉ lưu lịch sử sau khi AI hoàn tất
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

                response_placeholder.empty()

                st.warning(
                    "AI chưa tạo được câu trả lời. "
                    "Cậu thử gửi lại sau nhé."
                )

        # =========================
        # XỬ LÝ LỖI
        # =========================

        except Exception as error:

            error_text = str(error)
            error_lower = error_text.lower()

            # Lỗi hết quota hoặc giới hạn API
            if (
                "429" in error_text
                or "resource_exhausted" in error_lower
                or "quota" in error_lower
            ):

                st.warning(
                    "⚠️ Gemini đã chạm giới hạn quota "
                    "hoặc số lượt sử dụng API. "
                    "Cậu hãy kiểm tra Google AI Studio "
                    "hoặc chờ quota được cấp lại nhé."
                )

            # Lỗi máy chủ quá tải
            elif (
                "503" in error_text
                or "unavailable" in error_lower
            ):

                st.warning(
                    "⏳ Dịch vụ AI đang quá tải tạm thời. "
                    "Cậu đợi một chút rồi thử lại nhé."
                )

            # Lỗi thời gian chờ
            elif (
                "timeout" in error_lower
                or "timed out" in error_lower
            ):

                st.warning(
                    "⌛ Yêu cầu mất quá nhiều thời gian. "
                    "Cậu thử gửi lại sau nhé."
                )

            # Những lỗi khác
            else:

                st.error(
                    "❌ Có lỗi khi gọi AI. "
                    "Cậu có thể mở phần bên dưới "
                    "để kiểm tra chi tiết."
                )

            # Chi tiết lỗi dành cho người phát triển
            with st.expander("🔧 Chi tiết lỗi kỹ thuật"):
                st.code(error_text)
