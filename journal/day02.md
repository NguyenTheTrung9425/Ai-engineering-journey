# Nhật Ký Học Tập – Ngày 2 (24/11/2026)
**Chủ đề:** Dựng Backend AI Đa Người Dùng với FastAPI & Cơ Chế Dự Phòng (Fallback) Groq

---

### 1. Kiến Trúc Web API với FastAPI
- **Tại sao phải viết Web API thay vì chạy Terminal (CLI)?**
  - Terminal chỉ chạy được trên 1 máy cá nhân cục bộ.
  - Ngoài đời thực, ứng dụng Mobile, Website hay phần mềm doanh nghiệp cần kết nối qua Internet bằng giao thức HTTP. Viết API (`/chat`) giúp bất kỳ ứng dụng nào trên thế giới cũng có thể gửi câu hỏi và nhận câu trả lời.
- **Vai trò của Pydantic (`BaseModel`):**
  - Đóng vai trò là "người gác cổng" kiểm tra dữ liệu đầu vào. Nếu client gửi thiếu trường hoặc sai kiểu dữ liệu, Pydantic tự động chặn lại và báo lỗi (422) mà không làm sập server.
  - Tự động sinh ra giao diện tài liệu tương tác Swagger UI (`/docs`) để test API trực quan.

---

### 2. Quản Lý Bộ Nhớ Đa Người Dùng (`session = {}`)
- **Cách phân biệt người dùng:**
  - Dùng `session_id` làm chìa khóa (key) trong dictionary `session`.
  - Mỗi người có một ngăn nhớ riêng (`user_history = session[req.session_id]`), nhờ đó người này không bị lẫn câu chuyện của người kia.
- **Tại sao lưu trong RAM thì bấm Ctrl+S lại "mất trí nhớ"?**
  - Biến `session` nằm trong bộ nhớ tạm (RAM) của tiến trình Python.
  - Khi sửa code và bấm Ctrl+S, cờ `--reload` của uvicorn sẽ tắt tiến trình cũ và khởi động tiến trình mới $\rightarrow$ RAM bị hệ điều hành xóa sạch về rỗng `{}`.
  - *Bài học:* Trong hệ thống thực tế (production), bắt buộc phải lưu session vào CSDL (như Redis, SQLite, PostgreSQL) chứ không được lưu tạm trong RAM.

---

### 3. Cơ Chế Dự Phòng (Fallback System: Gemini $\rightarrow$ Groq)
- **Tính sẵn sàng cao (High Availability):**
  - Không bao giờ phụ thuộc 100% vào một nhà cung cấp duy nhất. Nếu Gemini bị nghẽn mạng/quá tải (503) sau 3 lần retry, hệ thống tự động gọi sang Groq (chạy model Llama 3) để cứu nguy.
  - Người dùng không hề biết Google vừa sập, trải nghiệm vẫn mượt mà.
- **Tại sao cần "bộ phiên dịch" đổi role?**
  - Dữ liệu lưu trong session dùng chuẩn của Google: `"role": "model"`.
  - Nhưng Groq tuân theo chuẩn OpenAI, chỉ hiểu `"role": "assistant"`.
  - Dòng code `role = "assistant" if h["role"] == "model" else "user"` giúp dịch lại nhãn tin nhắn để Groq không quăng lỗi `400 Bad Request`.

---

### 4. Kỹ Thuật Python Tuple Unpacking
- Bản chất khi hàm viết `return reply, "Gemini"`, Python đóng gói 2 giá trị này vào **1 cái hộp duy nhất (`tuple`)**.
- Cú pháp `bot_reply, model_used = get_ai_reply(...)` là cơ chế **mở gói tự động theo thứ tự**:
  - Biến đầu tiên hứng giá trị thứ nhất (`reply`).
  - Biến thứ hai hứng giá trị thứ hai (`model_used`).
- Giúp code ngắn gọn, sạch sẽ, không cần phải truy xuất qua chỉ số `[0]`, `[1]`.

---

### Cam Kết Bản Thân:
- **Game hôm nay:** 0 phút LoL, 0 phút Naraka ✅.
- **Tình trạng:** Nắm chắc kiến thức backend AI, sẵn sàng cho Ngày 3!