# AI Financial Multi-Agent System - Agent Testing Guide

## Tổng quan Agents

### 🎯 **Agents hiện có (đã implement):**
1. **`ai_cfo_agent`** - AI CFO Agent (Advisory)

### 🔮 **Agents được định nghĩa (chưa implement):**
2. **`forecasting_agent`** - Financial Forecasting Agent
3. **`alert_agent`** - Risk Alert Agent  
4. **`reporting_agent`** - Financial Reporting Agent
5. **`ocr_agent`** - Document Processing Agent
6. **`data_sync_agent`** - Data Synchronization Agent
7. **`reconciliation_agent`** - Financial Reconciliation Agent

---

## Test Agent hiện có

### 1. AI CFO Agent (`ai_cfo_agent`)

#### **Mô tả:**
- **Chức năng**: Phân tích tài chính, tư vấn chiến lược, đánh giá rủi ro
- **Loại**: Advisory Agent
- **Industry**: General (có thể customize)
- **Status**: ✅ **Hoạt động**

#### **Test Cases:**

##### **Test 1: Phân tích tài chính cơ bản**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Phân tích tình hình tài chính của công ty chúng tôi"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

**PowerShell:**
```powershell
$body = '{"message": "Phân tích tình hình tài chính của công ty chúng tôi"}'
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" -Method POST -Body $body -Headers @{"Content-Type"="application/json"}
```

##### **Test 2: Dự báo tài chính**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Dự báo tài chính cho quý tới và năm sau"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

##### **Test 3: Đánh giá rủi ro**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Đánh giá rủi ro tài chính và đưa ra khuyến nghị"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

##### **Test 4: Báo cáo tổng hợp**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tạo báo cáo tài chính tổng hợp cho ban lãnh đạo"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

##### **Test 5: So sánh ngành**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "So sánh hiệu suất tài chính với các công ty cùng ngành"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

##### **Test 6: Tư vấn đầu tư**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tư vấn về quyết định đầu tư 5 triệu USD vào dự án mới"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

##### **Test 7: Phân tích hiệu suất**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Phân tích hiệu suất tài chính và đề xuất cải thiện"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

##### **Test 8: Kế hoạch tài chính**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Lập kế hoạch tài chính cho năm 2026"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

#### **Expected Response:**
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

---

## Test Agents chưa implement (sẽ trả về lỗi)

### 2. Forecasting Agent (`forecasting_agent`)

#### **Mô tả:**
- **Chức năng**: Dự báo tài chính, trend analysis, scenario planning
- **Loại**: Predictive Agent
- **Status**: ❌ **Chưa implement**

#### **Test (sẽ fail):**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/forecasting_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Dự báo doanh thu cho 6 tháng tới"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

**Expected Error:**
```json
{
  "success": false,
  "error": "Agent 'forecasting_agent' not found",
  "session_id": "uuid-string"
}
```

### 3. Alert Agent (`alert_agent`)

#### **Mô tả:**
- **Chức năng**: Cảnh báo rủi ro, monitoring, threshold alerts
- **Loại**: Monitoring Agent
- **Status**: ❌ **Chưa implement**

#### **Test (sẽ fail):**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/alert_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Kiểm tra các cảnh báo rủi ro tài chính"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 4. Reporting Agent (`reporting_agent`)

#### **Mô tả:**
- **Chức năng**: Tạo báo cáo, dashboard, KPI tracking
- **Loại**: Reporting Agent
- **Status**: ❌ **Chưa implement**

#### **Test (sẽ fail):**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/reporting_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tạo báo cáo tài chính hàng tháng"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 5. OCR Agent (`ocr_agent`)

#### **Mô tả:**
- **Chức năng**: Xử lý tài liệu, OCR, data extraction
- **Loại**: Document Processing Agent
- **Status**: ❌ **Chưa implement**

#### **Test (sẽ fail):**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ocr_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Xử lý hóa đơn và trích xuất dữ liệu tài chính"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 6. Data Sync Agent (`data_sync_agent`)

#### **Mô tả:**
- **Chức năng**: Đồng bộ dữ liệu, integration, data standardization
- **Loại**: Data Management Agent
- **Status**: ❌ **Chưa implement**

#### **Test (sẽ fail):**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/data_sync_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Đồng bộ dữ liệu từ hệ thống ERP"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

### 7. Reconciliation Agent (`reconciliation_agent`)

#### **Mô tả:**
- **Chức năng**: Đối soát tài chính, matching, variance analysis
- **Loại**: Reconciliation Agent
- **Status**: ❌ **Chưa implement**

#### **Test (sẽ fail):**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/reconciliation_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Đối soát tài khoản ngân hàng với sổ sách"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

---

## Test Intelligent Routing

### Test routing tự động dựa trên keywords:

#### **1. Forecast Request (sẽ route đến forecasting_agent nhưng fail):**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tôi cần dự báo tài chính cho quý tới"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

#### **2. Alert Request (sẽ route đến alert_agent nhưng fail):**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Cảnh báo rủi ro tài chính cao"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

#### **3. Report Request (sẽ route đến reporting_agent nhưng fail):**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tạo báo cáo tài chính tổng hợp"
  }' \
  -w "\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n"
```

---

## Script Test Tự Động

### PowerShell Script:
```powershell
# Test all agents
$agents = @(
    @{id="ai_cfo_agent"; name="AI CFO Agent"; status="active"},
    @{id="forecasting_agent"; name="Forecasting Agent"; status="inactive"},
    @{id="alert_agent"; name="Alert Agent"; status="inactive"},
    @{id="reporting_agent"; name="Reporting Agent"; status="inactive"},
    @{id="ocr_agent"; name="OCR Agent"; status="inactive"},
    @{id="data_sync_agent"; name="Data Sync Agent"; status="inactive"},
    @{id="reconciliation_agent"; name="Reconciliation Agent"; status="inactive"}
)

foreach ($agent in $agents) {
    Write-Host "Testing $($agent.name) ($($agent.id))..." -ForegroundColor Yellow
    
    $body = '{"message": "Test agent functionality"}'
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/agents/$($agent.id)/invoke" -Method POST -Body $body -Headers @{"Content-Type"="application/json"}
        Write-Host "✅ $($agent.name): SUCCESS" -ForegroundColor Green
        Write-Host "   Agent ID: $($response.agent_id)" -ForegroundColor Cyan
        Write-Host "   Session ID: $($response.session_id)" -ForegroundColor Cyan
    }
    catch {
        Write-Host "❌ $($agent.name): FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    Write-Host ""
}
```

---

## Kết quả mong đợi

### ✅ **Agent hoạt động:**
- **`ai_cfo_agent`**: Trả về báo cáo tài chính đầy đủ

### ❌ **Agents chưa implement:**
- **`forecasting_agent`**: "Agent 'forecasting_agent' not found"
- **`alert_agent`**: "Agent 'alert_agent' not found"
- **`reporting_agent`**: "Agent 'reporting_agent' not found"
- **`ocr_agent`**: "Agent 'ocr_agent' not found"
- **`data_sync_agent`**: "Agent 'data_sync_agent' not found"
- **`reconciliation_agent`**: "Agent 'reconciliation_agent' not found"

---

## Roadmap Implementation

### **Phase 1: Core Agents (Hiện tại)**
- ✅ AI CFO Agent

### **Phase 2: Predictive Agents**
- 🔄 Forecasting Agent
- 🔄 Alert Agent

### **Phase 3: Processing Agents**
- 🔄 OCR Agent
- 🔄 Data Sync Agent

### **Phase 4: Analysis Agents**
- 🔄 Reporting Agent
- 🔄 Reconciliation Agent

---

## Lưu ý quan trọng

1. **Demo Mode**: Tất cả agents đều sử dụng mock data
2. **Intelligent Routing**: Hoạt động nhưng fallback về AI CFO Agent
3. **Error Handling**: Agents chưa implement sẽ trả về lỗi "not found"
4. **Performance**: Response time < 10s cho agent hoạt động
5. **Session Management**: Mỗi request tạo session ID mới
