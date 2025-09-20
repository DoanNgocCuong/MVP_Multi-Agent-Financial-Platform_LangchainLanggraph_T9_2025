# AI Financial Multi-Agent System - Testing Guide với CURL

## Tổng quan
Tài liệu này cung cấp hướng dẫn test toàn diện hệ thống AI Financial Multi-Agent bằng các lệnh CURL. Bao gồm test từng agent, tools, workflows và luồng tổng thể.

## Mục lục
1. [Chuẩn bị](#chuẩn-bị)
2. [Test System Status](#test-system-status)
3. [Test Agents](#test-agents)
4. [Test Workflows](#test-workflows)
5. [Test Tools](#test-tools)
6. [Test Luồng Tổng Thể](#test-luồng-tổng-thể)
7. [Test Performance](#test-performance)
8. [Troubleshooting](#troubleshooting)

---

## Chuẩn bị

### 1. Khởi động hệ thống
```bash
# Di chuyển vào thư mục deploy/src
cd deploy/src

# Kích hoạt virtual environment
.venv\Scripts\activate

# Khởi động server
python -m ai_financial.main
```

### 2. Kiểm tra server đang chạy
```bash
curl -X GET "http://localhost:8000/health" \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-20T09:00:00Z",
  "version": "0.1.0"
}
```

---

## Test System Status

### 1. Kiểm tra trạng thái tổng thể
```bash
curl -X GET "http://localhost:8000/api/v1/status" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

**Expected Response:**
```json
{
  "system": {
    "version": "0.1.0",
    "environment": "development",
    "debug": false
  },
  "orchestrator": {
    "running": true,
    "registered_agents": 1,
    "active_workflows": 0,
    "active_agent_count": 0,
    "max_concurrent_agents": 10,
    "agent_list": ["ai_cfo_agent"],
    "workflow_types": ["advisory", "transactional"]
  },
  "tool_hub": {
    "servers_count": 1,
    "total_tools": 3,
    "tool_registry_size": 3
  }
}
```

### 2. Kiểm tra health check
```bash
curl -X GET "http://localhost:8000/health" \
  -H "Content-Type: application/json"
```

---

## Test Agents

### Các loại Input khác nhau

#### **1. Input đơn giản (chỉ message) - ✅ Hoạt động:**
```json
{
  "message": "Phân tích tài chính"
}
```

**CURL Command:**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{"message": "Phân tích tài chính"}'
```

#### **2. Input với context cơ bản - ⚠️ Cần test:**
```json
{
  "message": "Phân tích tài chính",
  "context": {
    "company_name": "ABC Corp",
    "industry": "manufacturing"
  }
}
```

**CURL Command:**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Phân tích tài chính",
    "context": {
      "company_name": "ABC Corp",
      "industry": "manufacturing"
    }
  }'
```

#### **3. Input với dữ liệu tài chính - ⚠️ Cần test:**
```json
{
  "message": "Phân tích tài chính",
  "context": {
    "company_name": "ABC Corp",
    "industry": "manufacturing",
    "financial_data": {
      "revenue": 1000000,
      "expenses": 800000,
      "assets": 2000000,
      "liabilities": 500000
    }
  }
}
```

#### **4. Input với dữ liệu chi tiết - ⚠️ Cần test:**
```json
{
  "message": "Phân tích tài chính toàn diện",
  "context": {
    "company_name": "ABC Corp",
    "industry": "manufacturing",
    "period": "Q3 2025",
    "financial_data": {
      "revenue": 1000000,
      "expenses": 800000,
      "assets": 2000000,
      "liabilities": 500000,
      "cash_flow": 200000,
      "debt": 300000,
      "equity": 1200000
    },
    "additional_info": {
      "goals": "Tối ưu hóa hiệu suất tài chính",
      "concerns": "Tỷ lệ nợ cao",
      "benchmarks": "So sánh với ngành"
    }
  }
}
```

### Lưu ý quan trọng:
- **Input đơn giản**: Chỉ cần `message` - ✅ Đã test thành công
- **Input với context**: Cần thêm trường `context` - ⚠️ Đang phát triển
- **Hệ thống hiện tại**: Sử dụng mock data nên input context chưa được xử lý đầy đủ
- **Demo mode**: Tất cả phân tích đều dựa trên dữ liệu mẫu

### Input/Output Structure

#### **Input Format:**
```json
{
  "message": "Yêu cầu phân tích tài chính",
  "context": {
    "company_name": "Tên công ty",
    "industry": "Ngành nghề",
    "period": "Kỳ báo cáo",
    "financial_data": {
      "revenue": 1000000,
      "expenses": 800000,
      "assets": 2000000,
      "liabilities": 500000,
      "cash_flow": 200000
    },
    "additional_info": {
      "goals": "Mục tiêu phân tích",
      "concerns": "Vấn đề cần quan tâm",
      "benchmarks": "So sánh với đối thủ"
    }
  }
}
```

#### **Output Format:**
```json
{
  "agent_id": "ai_cfo_agent",
  "session_id": "uuid-string",
  "response": "# AI CFO Financial Analysis Report\n\n## Executive Summary\n...",
  "metadata": {
    "analysis_plan": {...},
    "financial_data": {...},
    "analysis_results": {...},
    "insights": "...",
    "risk_assessment": {...},
    "recommendations": "..."
  },
  "completed_steps": ["analyze_request", "gather_data", "perform_analysis", "generate_insights", "assess_risks", "provide_recommendations", "format_response"],
  "error": null
}
```

### 1. Test AI CFO Agent - Phân tích tài chính cơ bản
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Phân tích tình hình tài chính của công ty chúng tôi trong quý 3",
    "context": {
      "company_name": "ABC Corp",
      "industry": "manufacturing",
      "period": "Q3 2025",
      "financial_data": {
        "revenue": 1000000,
        "expenses": 800000,
        "assets": 2000000,
        "liabilities": 500000
      }
    }
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 2. Test AI CFO Agent - Dự báo tài chính
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Dự báo tài chính cho quý 4 và năm sau",
    "context": {
      "company_name": "TechStart Inc",
      "industry": "technology",
      "period": "Q4 2025 - 2026",
      "historical_data": {
        "q1_2025": {"revenue": 500000, "growth": 0.15},
        "q2_2025": {"revenue": 600000, "growth": 0.20},
        "q3_2025": {"revenue": 750000, "growth": 0.25}
      },
      "market_conditions": {
        "economic_outlook": "positive",
        "industry_trends": "AI adoption increasing",
        "competition_level": "high"
      }
    }
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 3. Test AI CFO Agent - Đánh giá rủi ro
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Đánh giá rủi ro tài chính và đưa ra khuyến nghị"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 4. Test AI CFO Agent - Báo cáo tổng hợp
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tạo báo cáo tài chính tổng hợp cho ban lãnh đạo"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 5. Test AI CFO Agent - Phân tích ngành
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "So sánh hiệu suất tài chính với các công ty cùng ngành"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

**Expected Response Structure:**
```json
{
  "agent_id": "ai_cfo_agent",
  "session_id": "uuid-string",
  "response": "# AI CFO Financial Analysis Report\n\n## Executive Summary\n...",
  "metadata": {
    "analysis_plan": {...},
    "financial_data": {...},
    "analysis_results": {...},
    "insights": "...",
    "risk_assessment": {...},
    "recommendations": "..."
  },
  "completed_steps": ["analyze_request", "gather_data", "perform_analysis", "generate_insights", "assess_risks", "provide_recommendations", "format_response"],
  "error": null
}
```

### Giải thích Output:

#### **1. Response chính:**
- **`agent_id`**: ID của agent xử lý request
- **`session_id`**: ID phiên làm việc (UUID)
- **`response`**: Báo cáo tài chính đầy đủ dạng Markdown
- **`error`**: Thông báo lỗi (null nếu thành công)

#### **2. Metadata chi tiết:**
- **`analysis_plan`**: Kế hoạch phân tích
- **`financial_data`**: Dữ liệu tài chính được sử dụng
- **`analysis_results`**: Kết quả phân tích chi tiết
- **`insights`**: Các insight chính
- **`risk_assessment`**: Đánh giá rủi ro
- **`recommendations`**: Khuyến nghị chiến lược

#### **3. Completed Steps:**
- **`analyze_request`**: Phân tích yêu cầu
- **`gather_data`**: Thu thập dữ liệu
- **`perform_analysis`**: Thực hiện phân tích
- **`generate_insights`**: Tạo insights
- **`assess_risks`**: Đánh giá rủi ro
- **`provide_recommendations`**: Đưa ra khuyến nghị
- **`format_response`**: Định dạng response

### Demo Mode Output:
Hiện tại hệ thống đang chạy ở **Demo Mode** nên:
- Tất cả dữ liệu tài chính đều là **mock data**
- Phân tích dựa trên **dữ liệu mẫu** cố định
- Response luôn có format **"# AI CFO Financial Analysis Report"**
- Bao gồm: **Executive Summary**, **Risk Assessment**, **Strategic Recommendations**

---

## Test Workflows

### 1. Test Advisory Workflow - Hỗ trợ CEO
```bash
curl -X POST "http://localhost:8000/api/v1/workflows/advisory/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Cần tư vấn tài chính chiến lược cho quyết định đầu tư mới"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 2. Test Advisory Workflow - Phân tích đầu tư
```bash
curl -X POST "http://localhost:8000/api/v1/workflows/advisory/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Phân tích tính khả thi của dự án đầu tư 10 triệu USD"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 3. Test Transactional Workflow - Xử lý giao dịch
```bash
curl -X POST "http://localhost:8000/api/v1/workflows/transactional/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Xử lý và phân loại các giao dịch tài chính trong tháng"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 4. Test Transactional Workflow - Đối soát
```bash
curl -X POST "http://localhost:8000/api/v1/workflows/transactional/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Đối soát và kiểm tra các giao dịch ngân hàng"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 5. Test Workflow Streaming
```bash
curl -X GET "http://localhost:8000/api/v1/workflows/advisory/stream?message=Test streaming workflow" \
  -H "Accept: text/plain" \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

**Expected Response Structure:**
```json
{
  "success": true,
  "workflow_type": "advisory",
  "workflow_id": "uuid-string",
  "results": {
    "analysis": {
      "agent_id": "ai_cfo_agent",
      "session_id": "uuid-string",
      "response": "...",
      "metadata": {...},
      "completed_steps": [...],
      "error": null
    }
  },
  "completed_steps": ["analysis"]
}
```

---

## Test Tools

### 1. Liệt kê tất cả tools
```bash
curl -X GET "http://localhost:8000/api/v1/tools" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 2. Test Financial Ratio Calculator
```bash
curl -X POST "http://localhost:8000/api/v1/tools/financial_ratio_calculator/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "ratio_type": "current_ratio",
    "financial_data": {
      "current_assets": 100000,
      "current_liabilities": 50000
    }
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 3. Test Cash Flow Analyzer
```bash
curl -X POST "http://localhost:8000/api/v1/tools/cash_flow_analyzer/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "cash_flows": [
      {
        "period": "2025-Q1",
        "operating_cash_flow": 50000,
        "investing_cash_flow": -10000,
        "financing_cash_flow": -5000,
        "net_cash_flow": 35000
      },
      {
        "period": "2025-Q2",
        "operating_cash_flow": 60000,
        "investing_cash_flow": -15000,
        "financing_cash_flow": -8000,
        "net_cash_flow": 37000
      }
    ],
    "analysis_type": "trend"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 4. Test Profitability Analyzer
```bash
curl -X POST "http://localhost:8000/api/v1/tools/profitability_analyzer/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "financial_data": {
      "revenue": 1000000,
      "cost_of_goods_sold": 600000,
      "operating_expenses": 200000,
      "net_income": 150000,
      "total_assets": 2000000,
      "total_equity": 1200000
    },
    "analysis_type": "comprehensive"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

**Expected Response Structure:**
```json
{
  "success": true,
  "data": {
    "ratio_value": 2.0,
    "interpretation": "Strong liquidity position",
    "benchmark": "Industry average: 1.5"
  },
  "error": null,
  "metadata": {
    "calculation_method": "current_assets / current_liabilities",
    "timestamp": "2025-09-20T09:00:00Z"
  },
  "execution_time": 0.05,
  "timestamp": "2025-09-20T09:00:00Z"
}
```

---

## Test Luồng Tổng Thể

### 1. Test Intelligent Routing - Forecast Request
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tôi cần dự báo tài chính cho quý tới"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 2. Test Intelligent Routing - Report Request
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tạo báo cáo tài chính tổng hợp"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 3. Test Intelligent Routing - Risk Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Đánh giá rủi ro và cảnh báo"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 4. Test End-to-End Workflow
```bash
# Bước 1: Khởi tạo phân tích
curl -X POST "http://localhost:8000/api/v1/workflows/advisory/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Phân tích tài chính toàn diện cho công ty"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"

# Bước 2: Sử dụng kết quả để tạo báo cáo
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Dựa trên phân tích trước, tạo báo cáo chi tiết cho CEO"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

---

## Test Performance

### 1. Test Response Time
```bash
# Test với timing
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Test performance"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\nSize: %{size_download} bytes\n"
```

### 2. Test Concurrent Requests
```bash
# Chạy đồng thời 3 requests
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{"message": "Request 1"}' &
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{"message": "Request 2"}' &
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{"message": "Request 3"}' &
wait
```

### 3. Test Memory Usage
```bash
# Test với request lớn
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Phân tích tài chính chi tiết với dữ liệu lớn: '$(printf 'A%.0s' {1..1000})'"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

---

## Test Script Tự Động

### 1. Tạo script test tổng hợp
```bash
#!/bin/bash
# test_comprehensive.sh

BASE_URL="http://localhost:8000"
echo "🔍 COMPREHENSIVE SYSTEM TEST"
echo "=============================="

# Test 1: System Status
echo -e "\n1. 📊 SYSTEM STATUS"
curl -s -X GET "$BASE_URL/api/v1/status" | jq '.system.version, .orchestrator.registered_agents, .tool_hub.total_tools'

# Test 2: Agent Tests
echo -e "\n2. 🤖 AGENT TESTS"
curl -s -X POST "$BASE_URL/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test agent functionality"}' | jq '.agent_id, .error'

# Test 3: Workflow Tests
echo -e "\n3. 🔄 WORKFLOW TESTS"
curl -s -X POST "$BASE_URL/api/v1/workflows/advisory/execute" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test advisory workflow"}' | jq '.success, .workflow_type'

# Test 4: Tool Tests
echo -e "\n4. 🛠️ TOOL TESTS"
curl -s -X GET "$BASE_URL/api/v1/tools" | jq '.count'

echo -e "\n✅ ALL TESTS COMPLETED"
```

### 2. Chạy script test
```bash
chmod +x test_comprehensive.sh
./test_comprehensive.sh
```

---

## Troubleshooting

### 1. Lỗi 500 Internal Server Error
```bash
# Kiểm tra logs server
tail -f logs/ai_financial.log

# Test với verbose output
curl -v -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test"}'
```

### 2. Lỗi Connection Refused
```bash
# Kiểm tra server có chạy không
netstat -an | grep 8000

# Khởi động lại server
cd deploy/src
python -m ai_financial.main
```

### 3. Lỗi Timeout
```bash
# Test với timeout dài hơn
curl --max-time 30 -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test"}'
```

### 4. Lỗi JSON Parsing
```bash
# Validate JSON trước khi gửi
echo '{"message": "Test"}' | jq .

# Test với JSON đơn giản
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

---

## Kết quả mong đợi

### ✅ Test thành công khi:
- HTTP Status: 200
- Response Time: < 10s
- Có đầy đủ các trường: `agent_id`, `session_id`, `response`, `metadata`, `completed_steps`
- `error`: null
- Response có nội dung tài chính hợp lệ

### ❌ Test thất bại khi:
- HTTP Status: 500, 404, 400
- Response Time: > 30s
- `error`: có giá trị
- Response rỗng hoặc không đúng format
- Timeout hoặc connection refused

---

## Lưu ý quan trọng

1. **Demo Mode**: Hệ thống đang chạy ở chế độ demo với mock LLM
2. **Response Time**: Có thể chậm do sử dụng mock data
3. **Session ID**: Mỗi request tạo session ID mới
4. **Metadata**: Chứa thông tin chi tiết về quá trình phân tích
5. **Error Handling**: Luôn kiểm tra trường `error` trong response

---

## Tài liệu tham khảo

- [API Documentation](DOCS_API.md)
- [Deployment Guide](docs2.12_Deployment_Checklist.md)
- [Technical Stack](docs2.9_understand_Tech_Stack.md)
- [Bug Reports](docs2.4_BugReport.md)
