# 🎨 LangGraph Studio UI Guide - Xem Nodes của AI CFO Agent

## 🚀 Cách Bật LangGraph Studio UI

### **1. Cài Đặt LangGraph CLI**
```bash
pip install langgraph-cli
```

### **2. Tạo Configuration File**
File `langgraph.json` đã được tạo:
```json
{
  "dependencies": ["."],
  "graphs": {
    "ai_cfo_agent": "./ai_cfo_agent.py:ai_cfo_agent"
  },
  "env": ".env"
}
```

### **3. Chạy LangGraph Studio**
```bash
cd deploy/src/ai_financial/agents/advisory/
langgraph dev
```

### **4. Truy Cập UI**
- **URL**: http://localhost:8123
- **Graph Mode**: Xem workflow dạng graph
- **Chat Mode**: Test agent trực tiếp

## 🎯 **Features của LangGraph Studio**

### **Graph Mode:**
- ✅ **Visualize Workflow**: Xem 7 nodes của AI CFO Agent
- ✅ **Node Details**: Click vào từng node để xem chi tiết
- ✅ **Edge Connections**: Xem luồng dữ liệu giữa các nodes
- ✅ **State Inspection**: Xem state changes
- ✅ **Execution Flow**: Trace execution path

### **Chat Mode:**
- ✅ **Interactive Testing**: Chat trực tiếp với agent
- ✅ **Real-time Execution**: Xem agent hoạt động
- ✅ **Response Preview**: Xem kết quả ngay lập tức
- ✅ **Error Debugging**: Debug lỗi trong workflow

## 📊 **7 Nodes của AI CFO Agent**

### **1. analyze_request**
- **Mục đích**: Phân tích yêu cầu từ user
- **Input**: User message (text)
- **Output**: Analysis plan
- **Xử lý**: Phân loại loại phân tích cần thiết

### **2. gather_data**
- **Mục đích**: Thu thập dữ liệu tài chính
- **Input**: Analysis plan
- **Output**: Financial data
- **Xử lý**: Load transactions, accounts, invoices

### **3. perform_analysis**
- **Mục đích**: Thực hiện phân tích tài chính
- **Input**: Financial data
- **Output**: Analysis results
- **Xử lý**: Liquidity, profitability, efficiency analysis

### **4. generate_insights**
- **Mục đích**: Tạo insights từ kết quả phân tích
- **Input**: Analysis results
- **Output**: Insights
- **Xử lý**: Sử dụng LLM để generate insights

### **5. assess_risks**
- **Mục đích**: Đánh giá rủi ro tài chính
- **Input**: Insights
- **Output**: Risk assessment
- **Xử lý**: Liquidity, credit, operational risk analysis

### **6. provide_recommendations**
- **Mục đích**: Đưa ra khuyến nghị chiến lược
- **Input**: Risk assessment
- **Output**: Recommendations
- **Xử lý**: Immediate, short-term, long-term strategies

### **7. format_response**
- **Mục đích**: Format kết quả cuối cùng
- **Input**: Recommendations
- **Output**: Final report (Markdown)
- **Xử lý**: Tạo executive summary và final report

## 🔍 **Cách Sử Dụng LangGraph Studio**

### **Graph Mode:**
1. **Mở Graph View**: Click vào "Graph" tab
2. **Explore Nodes**: Click vào từng node để xem details
3. **View Connections**: Xem edges giữa các nodes
4. **Inspect State**: Xem state changes trong từng step
5. **Trace Execution**: Follow execution path

### **Chat Mode:**
1. **Mở Chat View**: Click vào "Chat" tab
2. **Type Message**: Nhập câu hỏi tài chính
3. **Send Request**: Click "Send" để chạy agent
4. **View Response**: Xem kết quả phân tích
5. **Debug Issues**: Xem logs nếu có lỗi

## 🧪 **Test Cases để Thử**

### **Basic Financial Analysis:**
```
"Phân tích tài chính tổng thể"
```

### **Risk Assessment:**
```
"Đánh giá rủi ro tài chính của công ty"
```

### **Cash Flow Analysis:**
```
"Phân tích dòng tiền và khuyến nghị cải thiện"
```

### **Strategic Planning:**
```
"Đưa ra chiến lược tài chính dài hạn"
```

## 🎨 **Visualization Features**

### **Graph View:**
- **Node Colors**: Mỗi node có màu khác nhau
- **Edge Arrows**: Hiển thị luồng dữ liệu
- **State Info**: Hiển thị state trong từng node
- **Execution Path**: Highlight path đã chạy

### **Interactive Features:**
- **Zoom**: Zoom in/out graph
- **Pan**: Di chuyển graph
- **Node Details**: Click để xem chi tiết
- **State Inspection**: Xem state changes

## 🚀 **Advanced Features**

### **Debugging:**
- **Step-by-step Execution**: Chạy từng node riêng lẻ
- **State Inspection**: Xem state tại mỗi step
- **Error Tracking**: Debug lỗi trong workflow
- **Performance Metrics**: Đo thời gian từng node

### **Testing:**
- **Interactive Chat**: Test agent trực tiếp
- **Custom Inputs**: Test với input khác nhau
- **Response Validation**: Kiểm tra output format
- **Error Handling**: Test error scenarios

## 🔧 **Troubleshooting**

### **Common Issues:**
1. **Port 8123 in use**: Thay đổi port trong config
2. **Graph not loading**: Check langgraph.json format
3. **Nodes not visible**: Verify export function
4. **State errors**: Check state structure

### **Solutions:**
1. **Kill process**: `Ctrl+C` để stop server
2. **Check logs**: Xem error messages
3. **Restart**: Restart LangGraph Studio
4. **Verify config**: Check langgraph.json

## 📚 **Resources**

### **Documentation:**
- **LangGraph Studio**: https://langchain-ai.github.io/langgraph/studio/
- **LangGraph CLI**: https://langchain-ai.github.io/langgraph/cli/
- **Graph Visualization**: https://langchain-ai.github.io/langgraph/concepts/graphs/

### **Examples:**
- **Official Examples**: langchain-ai/langgraph
- **Community Projects**: jkmaina/LangGraphProjects
- **Tutorials**: FreeCodeCamp LangGraph Course

## 🎉 **Kết Luận**

Với LangGraph Studio, bạn có thể:

- ✅ **Visualize** workflow của AI CFO Agent
- ✅ **Debug** từng node riêng lẻ
- ✅ **Test** agent với interactive chat
- ✅ **Monitor** execution flow
- ✅ **Inspect** state changes
- ✅ **Optimize** performance

**LangGraph Studio** là công cụ mạnh mẽ để develop và debug LangGraph workflows! 🚀

---
*Generated for AI CFO Agent - 2025-09-20 UTC*
*LangGraph Studio UI Guide*
