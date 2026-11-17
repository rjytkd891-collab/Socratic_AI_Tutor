import streamlit as st
import streamlit.components.v1 as components

def inject_seo():
    # 1. Cấu hình tiêu đề tab trình duyệt chứa từ khóa chính
    st.set_page_config(
        page_title="Socratic AI - Trợ lý AI học văn & Hỗ trợ học văn thông minh",
        page_icon="📚",
        layout="wide"
    )

    # 2. Chèn Meta Tags & Schema JSON-LD vào thẻ <head> của trang
    seo_html = """
    <script>
        // Tự động cập nhật Meta Description và Keywords lên thẻ <head> chính của trang
        const metaTags = [
            { name: "google-site-verification", content: "xM4cOWbX37NbsITsSD" },
            { name: "description", content: "Socratic AI học văn - Trợ lý AI hỗ trợ học văn, phân tích tác phẩm văn học, gợi mở tư duy phản biện và viết bài nghị luận theo phương pháp đặt câu hỏi Socratic." },
            { name: "keywords", content: "Socratic AI, Socratic AI học văn, AI học văn, hỗ trợ học văn, trợ lý AI môn Ngữ văn, phân tích văn học AI" },
            { name: "author", content: "Socratic AI Tutor" },
            { property: "og:title", content: "Socratic AI - Trợ lý AI học văn thông minh" },
            { property: "og:description", content: "Công cụ AI hỗ trợ học văn, luyện viết nghị luận và khám phá tác phẩm văn học bằng phương pháp đối thoại Socratic." },
            { property: "og:type", content: "website" }
        ];

        metaTags.forEach(tagData => {
            let meta = document.createElement('meta');
            if (tagData.name) meta.name = tagData.name;
            if (tagData.property) meta.setAttribute('property', tagData.property);
            meta.content = tagData.content;
            document.head.appendChild(meta);
        });

        // Thêm dữ liệu có cấu trúc (Schema.org) giúp Google hiển thị đẹp trên kết quả tìm kiếm
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.text = JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "Socratic AI - AI Học Văn",
            "alternateName": ["Socratic AI học văn", "AI học văn", "Hỗ trợ học văn"],
            "applicationCategory": "EducationalApplication",
            "operatingSystem": "Web",
            "description": "Trợ lý AI hỗ trợ học văn và rèn luyện tư duy văn học theo phương pháp Socratic."
        });
        document.head.appendChild(script);
    </script>
    """
    components.html(seo_html, height=0, width=0)