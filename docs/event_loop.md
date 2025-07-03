### 1. Event Loop trong ADK Runtime

| Bước | Thành phần                   | Mô tả                  |
| ---- | ---------------------------- | ---------------------- |
| 1    | User → Runner                | Người dùng gửi yêu cầu |
| 2    | Runner → Event Loop          | Khởi động vòng lặp     |
| 3    | Event Loop → Execution Logic | Agent thực thi         |
| 4    | Agent → Runner               | Yield event            |
| 5    | Runner → Services & UI       | Xử lý & phản hồi       |
| 6    | Runner → Agent               | Resume execution       |
