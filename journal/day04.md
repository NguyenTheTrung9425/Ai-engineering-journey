## Tạo thêm cửa DELETE /session/{session_id} ở main.py, để khi bấm Reset thì app.py gọi sang ra lệnh cho main.py xóa luôn trí nhớ ở phía server.
- Lúc còn lưu trong RAM (session = {}), ta dùng session.pop(session_id, None) để xóa an toàn (có thì xóa, chưa có thì bỏ qua không báo lỗi KeyError). Tối nay nâng cấp lên SQLite thì thay bằng delete_history(session_id).

## Ghi nhớ SQL Injection
- Giả sử viết code SAI (dùng f-string):
**conn.execute(f"DELETE FROM chat_history WHERE session_id = '{session_id}'")**

- Nếu có 1 hacker vào ô nhập Session ID, thay vì gõ "Trung", hắn gõ: ' OR '1'='1
- Khi ghép vào f-string, câu lệnh SQL bị biến thành:
**DELETE FROM chat_history WHERE session_id = '' OR '1'='1'**

- Vì '1'='1' luôn luôn ĐÚNG, Database hiểu nhầm thành lệnh xóa mọi dòng → XÓA SẠCH DỮ LIỆU CỦA TOÀN BỘ KHÁCH HÀNG TRONG CÔNG TY! 😱 (Chiêu lén nhét lệnh SQL vào ô nhập chữ này gọi là SQL Injection).
  
- Còn khi viết ĐÚNG (dùng dấu ?): 
**conn.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))**
- SQLite khóa cứng khung lệnh SQL lại, và coi bất cứ thứ gì nhét vào dấu ? chỉ là chữ bình thường (dữ liệu), KHÔNG BAO GIỜ chạy nó như lệnh. Nên hacker có gõ ' OR '1'='1 thì SQLite chỉ đi tìm xem có ai đặt tên kỳ quặc là "' OR '1'='1" không → không có ai → an toàn tuyệt đối!
  

## Ghi nhớ các bug ẩn "assistant" vs "model" khi đọc từ DB ra cho Gemini & Groq.