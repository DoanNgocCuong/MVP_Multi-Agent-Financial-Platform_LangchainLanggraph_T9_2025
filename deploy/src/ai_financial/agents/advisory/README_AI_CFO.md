# AI CFO Agent - Hướng Dẫn Sử Dụng

## Tổng Quan

AI CFO Agent là một agent chuyên biệt trong hệ thống Multi-Agent Financial Platform, được thiết kế để cung cấp phân tích tài chính toàn diện, đánh giá rủi ro và đưa ra khuyến nghị chiến lược.

## Luồng Nội Bộ (Internal Workflow)

AI CFO Agent sử dụng LangGraph workflow với 7 bước xử lý tuần tự:

### 1. analyze_request
- **Mục đích**: Phân tích và hiểu yêu cầu từ user
- **Input**: Message từ user (text)
- **Xử lý**: 
  - Phân loại loại phân tích cần thiết
  - Xác định industry context
  - Tạo analysis plan
- **Output**: Analysis plan trong metadata

### 2. gather_data  
- **Mục đích**: Thu thập dữ liệu tài chính cần thiết
- **Input**: Analysis plan từ bước 1
- **Xử lý**:
  - Lấy dữ liệu transactions, accounts, invoices
  - Tạo mock financial data (demo mode)
  - Chuẩn bị data cho phân tích
- **Output**: Financial data trong metadata

### 3. perform_analysis
- **Mục đích**: Thực hiện phân tích tài chính chi tiết
- **Input**: Financial data từ bước 2
- **Xử lý**:
  - Phân tích liquidity, profitability, efficiency
  - Tính toán các financial ratios
  - So sánh với industry benchmarks
- **Output**: Analysis results trong metadata

### 4. generate_insights
- **Mục đích**: Tạo insights và nhận định từ kết quả phân tích
- **Input**: Analysis results từ bước 3
- **Xử lý**:
  - Sử dụng LLM để tạo insights
  - Xác định strengths và weaknesses
  - Đưa ra nhận định về trends
- **Output**: Insights trong metadata

### 5. assess_risks
- **Mục đích**: Đánh giá rủi ro tài chính
- **Input**: Insights từ bước 4
- **Xử lý**:
  - Phân tích các loại rủi ro (liquidity, credit, operational, market, compliance)
  - Đánh giá mức độ rủi ro
  - Đề xuất mitigation actions
- **Output**: Risk assessment trong metadata

### 6. provide_recommendations
- **Mục đích**: Đưa ra khuyến nghị chiến lược
- **Input**: Insights và risk assessment từ bước 4,5
- **Xử lý**:
  - Tạo strategic recommendations
  - Phân loại theo timeline (immediate, short-term, long-term)
  - Đề xuất specific actions
- **Output**: Recommendations trong metadata

### 7. format_response
- **Mục đích**: Định dạng response cuối cùng
- **Input**: Tất cả metadata từ các bước trước
- **Xử lý**:
  - Tạo comprehensive financial report
  - Format theo Markdown structure
  - Bao gồm Executive Summary, Risk Assessment, Recommendations
- **Output**: Final formatted response

## Luồng Dữ Liệu (Data Flow)

```
User Input (text) 
    ↓
analyze_request → analysis_plan
    ↓
gather_data → financial_data  
    ↓
perform_analysis → analysis_results
    ↓
generate_insights → insights
    ↓
assess_risks → risk_assessment
    ↓
provide_recommendations → recommendations
    ↓
format_response → final_report (Markdown)
```

## Các Loại Phân Tích Hỗ Trợ

### 1. Financial Health Assessment
- Phân tích tình hình tài chính tổng thể
- Đánh giá khả năng thanh toán
- Kiểm tra cấu trúc tài chính

### 2. Cash Flow Analysis
- Phân tích dòng tiền hoạt động
- Dự báo dòng tiền tương lai
- Tối ưu hóa quản lý tiền mặt

### 3. Profitability Analysis
- Phân tích khả năng sinh lời
- So sánh với ngành
- Xác định drivers của lợi nhuận

### 4. Risk Assessment
- Đánh giá rủi ro thanh khoản
- Rủi ro tín dụng
- Rủi ro hoạt động
- Rủi ro thị trường
- Rủi ro tuân thủ

### 5. Investment Analysis
- Phân tích cơ hội đầu tư
- Đánh giá ROI
- Phân tích rủi ro đầu tư

### 6. Compliance Review
- Kiểm tra tuân thủ quy định
- Báo cáo tài chính
- Audit preparation

### 7. Strategic Planning
- Lập kế hoạch tài chính dài hạn
- Scenario planning
- Capital allocation

### 8. Industry Benchmarking
- So sánh với competitors
- Industry best practices
- Market positioning

## Cách Sử Dụng

### 1. API Endpoint
```
POST /api/v1/agents/ai_cfo_agent/invoke
```

### 2. Request Format
```json
{
  "message": "Phân tích tài chính tổng thể của công ty",
  "context": {
    "company_id": "company_001",
    "user_id": "user_001",
    "analysis_type": "comprehensive",
    "industry": "technology"
  }
}
```

### 3. Response Format
```json
{
  "agent_id": "ai_cfo_agent",
  "session_id": "session_001",
  "response": "# AI CFO Financial Analysis Report\n\n## Executive Summary\n...",
  "metadata": {
    "analysis_plan": {...},
    "financial_data": {...},
    "analysis_results": {...},
    "insights": "...",
    "risk_assessment": {...},
    "recommendations": "..."
  },
  "completed_steps": ["analyze_request", "gather_data", ...],
  "error": null
}
```

## Testing

### 1. Chạy Test Script
```bash
# Linux/Mac
./curl_test_ai_cfo.sh

# Windows PowerShell
.\curl_test_ai_cfo.ps1
```

### 2. Test Individual Steps
```bash
# Chạy test từng bước
python test_ai_cfo.py
```

### 3. Test với curl
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Phân tích tài chính tổng thể",
    "context": {
      "company_id": "test_company",
      "user_id": "test_user"
    }
  }'
```

## Visualization

### 1. Mermaid Diagram
Xem file `ai_cfo_workflow.md` để xem diagram chi tiết của workflow.

### 2. LangFuse Integration
```python
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

langfuse = Langfuse()
handler = CallbackHandler()

# Thêm vào graph execution
result = await agent.compiled_graph.ainvoke(
    initial_state, 
    config={"callbacks": [handler]}
)
```

## Demo Mode vs Production Mode

### Demo Mode (hiện tại)
- Sử dụng mock data cố định
- LLM responses được simulate
- Tất cả analysis dựa trên sample data

### Production Mode (khi có OpenAI API key)
- Sử dụng real LLM (GPT-4)
- Phân tích dữ liệu thực tế
- Dynamic insights và recommendations

## Tối Ưu Hóa

### 1. Performance
- Tất cả 7 bước hoàn thành trong < 0.02s
- Không có bước nào bị lỗi
- Workflow chạy mượt mà

### 2. Recommendations
- ✅ Add caching for frequently accessed data
- ✅ Implement parallel processing where possible
- ✅ Use database connections for real data instead of mock data
- ✅ Add input validation and error handling
- ✅ Implement performance monitoring and metrics

## Troubleshooting

### 1. Common Issues
- **Agent not initialized**: Kiểm tra OpenAI API key
- **Workflow fails**: Check logs for specific error messages
- **Slow performance**: Consider caching and optimization

### 2. Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 3. Error Handling
Agent có built-in error handling và sẽ trả về error message chi tiết nếu có lỗi xảy ra.

## Kết Luận

AI CFO Agent là một component mạnh mẽ trong hệ thống Multi-Agent Financial Platform, cung cấp:

- ✅ **Comprehensive Analysis**: Phân tích tài chính toàn diện
- ✅ **Risk Assessment**: Đánh giá rủi ro chi tiết
- ✅ **Strategic Recommendations**: Khuyến nghị chiến lược
- ✅ **Industry Context**: Tích hợp ngữ cảnh ngành
- ✅ **High Performance**: Hiệu suất cao và ổn định
- ✅ **Easy Integration**: Dễ dàng tích hợp với hệ thống

---
*Generated on 2025-09-20 UTC*
*AI CFO Agent v1.0 - Multi-Agent Financial Platform*
