## 1. Trí nhớ của Chatbot:
- Bản chất LLM là **Stateless**(không có trạng thái), nó không dành riêng 1 **ngăn nhớ** nào trên sever để lưu lại cuộc trò chuyện của chúng ta. 
- Dòng đời của history qua từng lượt chat:
 + Bạn gõ: "Tôi là Trung"
 + history có 1 phần tử: [{"role": "user", "content": "Tôi là Trung"}]
 + Gửi lên Gemini: 1 câu → Trả về: "Chào Trung"
 + History được nạp thêm câu trả lời:
    [
        {"role": "user", "content": "Tôi là Trung"},
        {"role": "model", "content": "Chào Trung"}
    ]
- Vì openAI thiết kế API dạng văn bản thuần: {"role": "user", "content": "hello"}, mà mỗi tin nhắn không phải chỉ có mỗi chữ, mà có thể gồm cả hình ảnh, âm thanh, file,... Nên phải có **part** 
                    {
                    "role": "user",
                    "parts": [
                        {"text": "Hãy phân tích hình này:"},
                        {"inline_data": {"mime_type": "image/jpeg", "data": "..."}}
                              ]
                    }
