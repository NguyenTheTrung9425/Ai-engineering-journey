import requests
import streamlit as st

st.set_page_config(page_title = "AI Chatbot", page_icon = "🤖", layout="centered")

st.markdown(
    """
<style>
    /* Ẩn bớt khoảng trắng thừa trên đầu trang */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }
    
    /* Bong bóng chat của USER: Căn lệch sang bên PHẢI */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse;
        text-align: right;
        background-color: #1e3a8a20; /* Nền xanh nhẹ */
        border-radius: 15px 15px 2px 15px;
        margin-left: auto;
        width: fit-content;
        max-width: 80%;
    }
    /* Bong bóng chat của BOT: Căn lệch sang bên TRÁI */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
        background-color: #37415120; /* Nền xám nhẹ */
        border-radius: 15px 15px 15px 2px;
        margin-right: auto;
        width: fit-content;
        max-width: 80%;
    }
</style>
""",
    unsafe_allow_html=True,
)


st.title("🤖 My AI Chatbot")
st.caption("Project week 01 - FastAPI + Gemini + Groq Fallback + Streamlit")

# 1. Tạo thanh bên (Sidebar) để nhập tên / Session ID
with st.sidebar:
    st.header("Settings ⚙️")
    session_id = st.text_input("Tên của bạn (Session ID):", value = "Trung")
    if st.button("Reset Session"):
        st.session_state.session_history = []
        st.rerun()

# 2. Quản lý trạng thái tin nhắn trên giao diện của Streamlit

if "session_history" not in st.session_state:
    st.session_state.session_history = []   

# 3. Hiển thị lại các tin nhắn cũ ra màn hình dưới dạng bong bóng chat
for chat in st.session_state.session_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# 4. Ô nhập tin nhắn ở dưới đáy màn hình (giống hệt ChatGPT)
if prompt := st.chat_input("Hỏi tôi bất cứ điều gì..."):
    # Hiển thị ngay câu hỏi của bạn lên màn hình
    st.session_state.session_history.append({"role": "user", "content": prompt})   
    with st.chat_message("user"):
        st.markdown(prompt) 

    # 5. Gửi request tới Backend FastAPI (cổng 8000)
    backend_url = "http://127.0.0.1:8000/chat"
    payload = {"session_id": session_id, "message": prompt}

    with st.chat_message("assistant"):
        with st.spinner("AI đang suy nghĩ..."):
            try:
                response = requests.post(backend_url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    bot_reply = data["reply"]
                    model_used = data["model_used"]

                    # In câu trả lời và nhãn mô hình ra màn hình
                    st.markdown(bot_reply)
                    st.caption(f"Model used: {model_used}")

                    # Lưu vào danh sách hiển thị
                    st.session_state.session_history.append({"role": "model", "content": bot_reply})
                else:
                    st.error(f"Error: Mã {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Không thể kết nối tới backend: {e}")