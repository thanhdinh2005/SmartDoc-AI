import streamlit as st
import sys
import os

# Thêm thư mục backend vào đường dẫn để import được code
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
from conversational_rag import ConversationalRAG

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="SmartDoc AI", page_icon="🧠", layout="centered")
st.title("🧠 SmartDoc AI - Hệ thống Q&A Tài liệu")

# --- 2. KHỞI TẠO STATE (BỘ NHỚ TRÌNH DUYỆT) ---
# Tránh việc tải lại mô hình AI mỗi khi người dùng click vào trang
if "qa_system" not in st.session_state:
    with st.spinner("Đang khởi động AI Engine (Qwen 3B)..."):
        st.session_state.qa_system = ConversationalRAG(model_name="qwen2.5:3b")

# Khởi tạo mảng lưu lịch sử chat (Yêu cầu 2)
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. THANH BÊN (SIDEBAR) & NÚT XÓA LỊCH SỬ ---
with st.sidebar:
    st.header("⚙️ Cài đặt")
    # Yêu cầu 3: Nút xóa lịch sử hội thoại
    if st.button("🗑️ Xóa lịch sử Chat"):
        st.session_state.messages = []
        st.success("Đã xóa lịch sử!")

# --- 4. HIỂN THỊ LỊCH SỬ HỘI THOẠI ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. XỬ LÝ NHẬP LIỆU & HIỂN THỊ KẾT QUẢ ---
# Khung nhập chat ở cuối màn hình
if prompt := st.chat_input("Hỏi bất cứ điều gì về tài liệu của bạn..."):
    # 5.1. In câu hỏi của người dùng ra màn hình
    st.chat_message("user").markdown(prompt)
    
    # 5.2. Lưu vào lịch sử
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 5.3. Gọi AI xử lý và in câu trả lời (Có hiệu ứng Streaming)
    with st.chat_message("assistant"):
        # Nhận luồng dữ liệu stream từ Backend
        stream_response, sources = st.session_state.qa_system.ask(prompt)
        
        # Streamlit có sẵn hàm write_stream cực mạnh để hứng từng chữ từ LangChain!
        full_response = st.write_stream(stream_response)
        
    # 5.4. Lưu câu trả lời của AI vào lịch sử
    st.session_state.messages.append({"role": "assistant", "content": full_response})