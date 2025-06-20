# Hướng Dẫn Chi Tiết về MCP và ADK

Chào bạn, để hướng dẫn lại toàn bộ tutorial này một cách chi tiết và giúp bạn tránh "tutorial hell", chúng ta sẽ tập trung vào việc hiểu rõ lý do tại sao MCP tồn tại và cách nó giải quyết các vấn đề, thay vì chỉ đơn thuần sao chép code. Dưới đây là hướng dẫn từng bước, nhấn mạnh vào các khái niệm chính và lý do đằng sau chúng.

## Tổng quan về MCP và ADK
**Model Context Protocol (MCP)** đã nhanh chóng trở thành tiêu chuẩn để kết nối các công cụ với các tác nhân AI của bạn. Trong video, nó được mô tả là một công nghệ nền tảng cốt lõi trong việc xây dựng các tác nhân AI thực tế. Mục tiêu chính là siêu nạp các tác nhân **ADK (Agent Development Kit)** với các công cụ thực tế có thể hoạt động.

Người hướng dẫn ban đầu cũng cảm thấy MCP rất phức tạp và khó hiểu, thậm chí nghĩ rằng nó "vô nghĩa" và "quá nhiều công việc phụ". Tuy nhiên, sau khi làm việc liên tục với nó, anh ấy đã trở thành một người tin tưởng vững chắc vào MCP và hiểu lý do tại sao nó là một công cụ mạnh mẽ. Điều này cho thấy sự kiên trì và việc hiểu rõ các vấn đề mà MCP giải quyết là chìa khóa để vượt qua "tutorial hell".

## Giai đoạn 1: Hiểu về MCP – Tại sao chúng ta cần nó? (The "Why")
Giai đoạn này tập trung vào việc đặt nền tảng vững chắc để bạn hiểu tại sao MCP lại mạnh mẽ và tại sao bạn nên sử dụng nó.

### 1. Vấn đề với việc gọi công cụ truyền thống (Traditional Tool Calling):
- **Thiếu chuẩn hóa và lặp lại công việc**: Khi xây dựng một tác nhân ADK để làm việc với một công cụ như Notion, bạn sẽ phải tự tay viết code cho mọi lệnh gọi API (ví dụ: truy vấn cơ sở dữ liệu, tạo trang, thêm bình luận).
- **Thừa thãi và vi phạm nguyên tắc DRY (Don't Repeat Yourself)**: Nếu bạn có nhiều tác nhân hoặc nhiều dự án cần sử dụng cùng một công cụ (ví dụ: Notion), bạn sẽ phải sao chép và dán cùng một đoạn mã công cụ giữa các dự án hoặc tạo thư viện công cụ dùng chung. Ở cấp độ vĩ mô, mọi nhà phát triển AI muốn sử dụng Notion đều phải tự mình tạo lại hàng trăm dòng code chỉ để gói gọn các lệnh của Notion API. Điều này dẫn đến sự lãng phí công sức và không hiệu quả.

### 2. Giải pháp của MCP (Model Context Protocol):
- **Chuẩn hóa việc kết nối công cụ**: MCP là một cách chuẩn hóa để các tác nhân AI kết nối với các công cụ bên ngoài. Về cơ bản, MCP là một máy chủ (server) cung cấp một cách chuẩn hóa để truy cập các công cụ AI phổ biến, thực tế mà bạn muốn cung cấp cho các tác nhân của mình.
- **Chức năng của MCP Server**:
  - Kết nối với tác nhân của bạn.
  - Cho phép tác nhân của bạn gọi một công cụ, liệt kê tất cả các công cụ mà tác nhân có quyền truy cập, hoặc mô tả một công cụ để bạn biết các đối số cần truyền và giá trị trả về.
  - Gói gọn tất cả các điểm cuối API mà bạn thường phải tạo công cụ cho chúng, và MCP tự động làm điều đó cho bạn.
- **Giảm sự dư thừa**: Ví dụ, Notion có một máy chủ MCP mà mọi nhà phát triển AI ở bất cứ đâu đều có thể sử dụng để giao tiếp với Notion. Điều này loại bỏ sự cần thiết phải tạo lại các công cụ cho cùng một API.

### 3. Lợi ích chính của việc sử dụng MCP:
- **Dễ dàng truy cập các công cụ phổ biến**: Với các công cụ phổ biến như Slack, Notion, các cơ sở dữ liệu thông thường, hoặc các công cụ trình duyệt, bạn chỉ cần kết nối tác nhân của mình với máy chủ MCP tương ứng và ngay lập tức có quyền truy cập vào tất cả các công cụ đó. Thay vì phải tạo lại tất cả các lệnh API, MCP giúp tác nhân của bạn được "siêu nạp" để thực hiện rất nhiều công việc.
- **Tiêu chuẩn hóa và tái sử dụng**: MCP cho phép truy cập công cụ theo cách tiêu chuẩn hóa, giúp việc chia sẻ và sử dụng lại công cụ trên nhiều dự án trở nên dễ dàng hơn rất nhiều.
- **Tiết kiệm thời gian và công sức**: Đối với các API phổ biến, MCP là một "ân huệ từ chúa" vì nó giúp cuộc sống của bạn dễ dàng hơn rất nhiều khi làm việc với các tác nhân. Chỉ với vài cú nhấp chuột, bạn có thể kết nối với Notion và truy cập ngay lập tức hàng chục công cụ khác nhau.

### 4. Nhược điểm và khi nào không nên dùng MCP:
- **Thiết lập ban đầu phức tạp hơn**: Có một số thiết lập bổ sung mà bạn phải thực hiện khi tạo các máy chủ MCP, đặc biệt là với các công cụ tùy chỉnh (custom tools). Bạn cần phải thiết lập một máy chủ tùy chỉnh trên máy tính cục bộ của mình.
- **Không phù hợp cho thử nghiệm nhanh**: Nếu bạn đang thử nghiệm nhanh với một số công cụ tùy chỉnh cục bộ cho mục đích thử nghiệm khái niệm (proof of concept), bạn nên tránh MCP vì nó sẽ tốn nhiều công sức thiết lập máy chủ hơn mà không mang lại nhiều giá trị.
- **Khi nào nên dùng**: Chỉ nên dùng MCP khi bạn tạo ra thứ gì đó mà bạn sẽ sử dụng trong nhiều dự án khác nhau hoặc bạn muốn người khác sử dụng.

## Giai đoạn 2: Kết nối tác nhân ADK với máy chủ MCP từ xa (Remote MCP)
Giai đoạn này giúp bạn hiểu cách kết nối tác nhân của mình với một máy chủ MCP đã có sẵn, chẳng hạn như máy chủ Notion MCP.

### 1. Tìm kiếm các máy chủ MCP:
- **Kho lưu trữ GitHub của Model Context Protocol**: Đây là nơi phổ biến nhất để tìm các máy chủ MCP công khai, bao gồm các công cụ cho GitHub, Google Drive, Google Maps, cơ sở dữ liệu, trình duyệt web, v.v.
- **Smithery**: Một nguồn khác để tìm các máy chủ MCP.
- **Cấu trúc của một máy chủ MCP**: Mỗi máy chủ MCP sẽ liệt kê các công cụ mà nó cung cấp, mục đích dự kiến của công cụ, các đầu vào (inputs) và giá trị trả về (returns). Nó cũng cung cấp hướng dẫn chi tiết về cách sử dụng công cụ đó.

### 2. Cách chạy một máy chủ MCP:
- Một máy chủ MCP chỉ đơn thuần là một máy chủ chạy cục bộ trên máy tính của bạn và chờ tác nhân của bạn gửi yêu cầu.
- Có nhiều cách để chạy một máy chủ, phổ biến nhất là:
  - **Docker**: Tස: Tạo một Docker container và chạy máy chủ MCP bên trong nó.
  - **npx (Node Package Executables)**: Chạy một gói Node.js để khởi động máy chủ.
  - **Python**: Chạy một máy chủ được viết bằng Python (bạn sẽ thấy ví dụ này trong Giai đoạn 3).
- Các lệnh chạy máy chủ thường bao gồm: lệnh (command), các đối số (arguments) cần thiết để khởi động máy chủ (ví dụ: biến môi trường cho khóa API), và đôi khi là liên kết đến thư viện hoặc container.

### 3. Ví dụ với Notion MCP Server:
- Để làm việc với Notion, bạn sẽ cần làm theo hướng dẫn thiết lập của họ để có khóa API Notion và kết nối máy chủ MCP của họ với các trang và cơ sở dữ liệu Notion của bạn.

### 4. Kết nối tác nhân ADK với MCP:
- Trong code của tác nhân ADK, bạn sử dụng lệnh MCP tool set để kết nối tác nhân của mình với các máy chủ MCP khác nhau.
- Bạn sẽ truyền vào các tham số kết nối (connection parameters) và các biến môi trường cần thiết (ví dụ: khóa API Notion).
- **Ví dụ code** để kết nối với Notion MCP server:  
  ```python
  agent.add_model_context_protocol_tool_set(connection_parameters, environment_variables)
  ```
  Điều này cho phép tác nhân của bạn truy cập ngay lập tức hàng chục công cụ khác nhau chỉ với một lệnh.

### 5. Cách tác nhân tương tác với MCP (Demo thực tế):
- Khi tác nhân được kết nối, nó có thể:
  - **What tools do you have access to?**: Yêu cầu máy chủ MCP liệt kê tất cả các công cụ mà nó có quyền truy cập. Máy chủ MCP sẽ trả về danh sách các công cụ cơ bản như truy cập trang, tìm kiếm cơ sở dữ liệu, quản lý người dùng, tạo bình luận, v.v.
  - **Describe the [tool name] tool**: Yêu cầu máy chủ MCP mô tả một công cụ cụ thể, bao gồm mục đích, các đầu vào cần thiết (query, filter, sorting, pagination), và giới hạn. Thông tin này đã được máy chủ MCP cung cấp sẵn, bạn không cần phải tự thêm vào.
  - **Gọi công cụ (Call tool)**: Tác nhân có thể dịch các yêu cầu ngôn ngữ tự nhiên thành các lệnh gọi công cụ phù hợp. Ví dụ:
    - **What databases have I used recently?** sẽ khiến tác nhân gọi công cụ tìm kiếm cơ sở dữ liệu Notion.
    - **What are the most recent pages I've worked on in the content engine, give me the five most recent?** sẽ tạo một truy vấn tùy chỉnh để tìm kiếm các trang gần đây nhất trong cơ sở dữ liệu cụ thể.
    - **Add a comment to the MCP ADK crash course that says 'Please like and subscribe.'** sẽ khiến tác nhân gọi công cụ thêm bình luận.
- **Minh họa về luồng làm việc**: Tác nhân gọi máy chủ MCP, máy chủ MCP sau đó gọi API Notion, và Notion thực hiện hành động và trả về kết quả.
- **Khả năng gỡ lỗi**: Bạn có thể dễ dàng kiểm tra các hoạt động của tác nhân bằng cách nhấp vào các nút trong giao diện để xem tác nhân đã chọn công cụ nào và các tham số được truyền vào cho lệnh gọi hàm.

## Giai đoạn 3: Tạo một máy chủ MCP cục bộ (Local MCP) – Dành cho công cụ tùy chỉnh
Giai đoạn này sẽ phức tạp hơn về mặt code, nhưng nó rất quan trọng để bạn hiểu cách tạo các công cụ tùy chỉnh của riêng mình và cung cấp chúng cho các tác nhân một cách chuẩn hóa bằng MCP.

### 1. Mục đích:
Học cách tạo một máy chủ MCP chạy cục bộ trên máy tính của bạn và kết nối tác nhân ADK với nó. Điều này hữu ích khi bạn muốn tạo các công cụ tùy chỉnh của riêng mình và cung cấp chúng một cách chuẩn hóa.

### 2. Các bước tạo máy chủ MCP cục bộ (server.py):
- **Cấu trúc dự án**: Thường có một thư mục `local_MCP` chứa `server.py` (tạo máy chủ), `agent.py` (gọi đến máy chủ MCP), và cơ sở dữ liệu của bạn (ví dụ: SQLite).
- **Kết nối cơ sở dữ liệu**: Tạo một hàm tiện ích (ví dụ: `get_database_connection`) mà tất cả các công cụ của bạn sẽ sử dụng để kết nối với cơ sở dữ liệu.
- **Tạo các công cụ (Tools)**:
  - Các công cụ là các hàm Python thông thường (ví dụ: `list_database_tables`, `get_table_schema`, `query_database_table`, `insert_data`, `delete_data`).
  - **Quy tắc quan trọng**: Trong ADK, bạn cần đảm bảo rằng các công cụ trả về một dictionary.
  - **Bug cần lưu ý**: Tại thời điểm video được tạo, công cụ MCP không thể có tham số rỗng (empty parameter) hoặc tham số có giá trị mặc định/tùy chọn; bạn phải truyền một tham số giả (dummy parameter) để nó hoạt động. Điều này nhấn mạnh tầm quan trọng của việc kiểm tra tài liệu ADK mới nhất hoặc cộng đồng để biết các bản sửa lỗi.
- **Khởi tạo MCP Server**: Tạo một thể hiện của máy chủ MCP bằng cách cung cấp tên cho nó (ví dụ: `server = MCPServer(name="My Database Server")`).
- **Thêm công cụ vào Server**:
  - ADK cung cấp một hàm giúp chuyển đổi các công cụ ADK thô (raw ADK tools) thành định dạng công cụ mà MCP có thể sử dụng.
  - Bạn sẽ tạo một danh sách hoặc từ điển các công cụ ADK mà bạn muốn thêm vào máy chủ của mình.
- **Hai hàm chính mà mọi máy chủ MCP cần**:
  - **list_tools**: Hàm này có nhiệm vụ liệt kê tất cả các công cụ mà máy chủ MCP có quyền truy cập. Nó sẽ lặp qua danh sách các công cụ ADK của bạn, chuyển đổi chúng sang định dạng MCP và trả về một danh sách các schema công cụ. Khi tác nhân hỏi "what tools do you have access to?", hàm này sẽ được gọi.
  - **call_tool**: Hàm này nhận tên của một công cụ và các đối số cụ thể. Nó kiểm tra xem công cụ đó có tồn tại không, sau đó gọi hàm công cụ tương ứng (ví dụ: `run_async`) và trả về phản hồi cho tác nhân.
- **Chạy MCP Server**: Sử dụng `run_mcp_stdio_server` để khởi động máy chủ cục bộ. Máy chủ này sẽ chạy và chờ tác nhân gửi yêu cầu thông qua input/output tiêu chuẩn (standard input/output). Bạn có thể chạy máy chủ này độc lập để kiểm tra bằng lệnh `python server.py`.

### 3. Kết nối tác nhân ADK với máy chủ MCP cục bộ (agent.py):
- Cũng giống như kết nối với máy chủ từ xa, bạn sử dụng MCP tool set. Tuy nhiên, thay vì chạy một lệnh `npx` hoặc `docker` từ xa, bạn cần chỉ định đường dẫn tuyệt đối (absolute path) đến tệp `server.py` của bạn.
- **Ví dụ**:
  ```python
  agent.add_model_context_protocol_tool_set(command=["python3", os.path.abspath(os.path.join(os.path.dirname(__file__), "server.py"))])
  ```
  Điều này đảm bảo tác nhân biết cách khởi động và giao tiếp với máy chủ cục bộ của bạn.

### 4. Minh họa về tác nhân ADK và Local MCP (Demo thực tế với Database):
- Khi chạy tác nhân, bạn có thể thực hiện các lệnh tương tự:
  - **What tools do you have access to?**: Sẽ trả về danh sách các công cụ cơ sở dữ liệu tùy chỉnh mà bạn đã thiết lập (`insert_data`, `delete_data`, `query_data`, v.v.).
  - **What tables do I have access to?**: Sẽ kích hoạt công cụ `list_all_tables` và trả về các bảng trong cơ sở dữ liệu cục bộ của bạn (ví dụ: `users`, `to-dos`).
  - **What users do I have in the users table?**: Sẽ kích hoạt công cụ `query_database_table` để lấy tất cả thông tin từ bảng `users`.
  - **What to-dos does Bob have?**: Tác nhân sẽ tạo một truy vấn tùy chỉnh để tìm các to-dos trong bảng `to-do` với điều kiện `user_ID` khớp với `user_ID` của Bob.
  - **Add a to-do for Bob to go grocery shopping**: Sẽ kích hoạt công cụ `insert_data` để thêm một mục mới vào cơ sở dữ liệu.
- Điều này cho thấy tác nhân ADK có thể chuyển đổi ngôn ngữ tiếng Anh của bạn thành các lệnh gọi công cụ phù hợp được MCP host, bao gồm cả các công cụ tùy chỉnh của bạn.

## Cách tránh "Tutorial Hell" với hướng dẫn này
Để thực sự nắm vững MCP và tránh rơi vào "tutorial hell" (tức là chỉ làm theo mà không hiểu), hãy tập trung vào những điều sau:

1. **Hiểu rõ "Tại sao"**: Đừng chỉ sao chép code. Hãy luôn tự hỏi tại sao chúng ta cần MCP? Nó giải quyết vấn đề gì của việc gọi công cụ truyền thống?. Sự lặp lại code và thiếu chuẩn hóa là những vấn đề cốt lõi mà MCP giải quyết.
2. **Khái niệm hơn là Cú pháp**: Tập trung vào việc hiểu các khái niệm như "cách chuẩn hóa", "MCP server là một wrapper", và cách nó cung cấp các hàm `list_tools`, `describe_tools`, và `call_tool`.
3. **Thực hành Tích cực**:
   - Tải xuống mã nguồn: Video cung cấp tất cả mã nguồn miễn phí. Hãy tải xuống và chạy thử các ví dụ.
   - Thay đổi và thử nghiệm: Thay đổi một phần nhỏ của mã và xem điều gì xảy ra. Thử thêm một công cụ mới vào máy chủ MCP cục bộ của bạn hoặc thay đổi logic của một công cụ hiện có.
   - Sử dụng tính năng gỡ lỗi của ADK: Luôn kiểm tra các nút gỡ lỗi trong giao diện tác nhân ADK để xem tác nhân đang nghĩ gì, công cụ nào được chọn và các tham số được truyền vào. Đây là cách tuyệt vời để hiểu luồng hoạt động.
4. **Biết khi nào nên sử dụng MCP**: Dựa trên nhược điểm, hãy nhớ rằng MCP là tuyệt vời cho các API phổ biến hoặc khi bạn muốn chuẩn hóa việc sử dụng công cụ trên nhiều dự án. Nhưng đối với các thử nghiệm nhanh hoặc PoC với công cụ tùy chỉnh, việc thiết lập có thể quá phức tạp so với lợi ích.
5. **Từng bước một**: Người hướng dẫn nhấn mạnh rằng MCP có nhiều phần chuyển động và phải mất thời gian để hiểu. Đừng lo lắng nếu nó không "nhấp" ngay lập tức. Cứ làm theo từng giai đoạn và mọi thứ sẽ rõ ràng hơn khi bạn thấy nó hoạt động trong thực tế.
6. **Sử dụng tài nguyên bổ sung**: Nếu có bất kỳ câu hỏi nào, bạn có thể bình luận hoặc tham gia cộng đồng miễn phí mà người hướng dẫn đã tạo (với hơn 7000 thành viên và các buổi huấn luyện hàng tuần miễn phí).

Bằng cách tập trung vào lý do tại sao và cách thức MCP hoạt động ở cấp độ khái niệm, kết hợp với thực hành chủ động, bạn sẽ có thể nắm vững công nghệ này và áp dụng nó một cách hiệu quả vào các dự án AI của mình.