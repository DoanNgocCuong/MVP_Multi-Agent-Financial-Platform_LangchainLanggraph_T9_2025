

Em gặp vấn đề là:

- .env em để LANGFUSE KEY, ko để LANGSMITH KEY
- nhưng khi bật langgraph dev lên nó tự nhảy vào LANGSMITH thay vì LANGFUSE

- Dù ko có LANGSMITH KEY mà UI trên LANGSMITH vẫn chạy được luồng thế mới ảo ạ.



Hình như là:

- Code của em khi chạy `langgraph dev` nó tự mở cửa sổ LangSmith lên.
  Vì LangSmith là mặc định của LangGraph Studio (em code đoạn này trong code)
- Còn vào cloud.langfuse thì vẫn có log lại sếp ạ
  (em vừa vào check thử thì thấy có log)
