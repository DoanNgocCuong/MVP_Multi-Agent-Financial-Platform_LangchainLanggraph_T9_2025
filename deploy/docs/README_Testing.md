# AI Financial Multi-Agent System - Testing Guide

## Quick Start

### 1. Khởi động hệ thống
```bash
cd deploy/src
.venv\Scripts\activate
python -m ai_financial.main
```

### 2. Test nhanh với CURL
```bash
# Test system status
curl -X GET "http://localhost:8000/api/v1/status"

# Test agent
curl -X POST "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{"message": "Phân tích tài chính"}'

# Test workflow
curl -X POST "http://localhost:8000/api/v1/workflows/advisory/execute" \
  -H "Content-Type: application/json" \
  -d '{"message": "Tư vấn tài chính"}'
```

### 3. Test tự động

#### Linux/Mac:
```bash
chmod +x test_automation.sh
./test_automation.sh all
```

#### Windows PowerShell:
```powershell
.\test_automation.ps1 all
```

## Tài liệu chi tiết

- **[docs3.2_Testing_Guide_CURL.md](docs3.2_Testing_Guide_CURL.md)** - Hướng dẫn test chi tiết với CURL
- **[test_automation.sh](test_automation.sh)** - Script test tự động (Linux/Mac)
- **[test_automation.ps1](test_automation.ps1)** - Script test tự động (Windows)

## Các loại test

1. **System Status** - Kiểm tra trạng thái hệ thống
2. **Agents** - Test từng agent riêng biệt
3. **Workflows** - Test luồng workflow
4. **Tools** - Test các công cụ tài chính
5. **Performance** - Test hiệu suất
6. **Intelligent Routing** - Test định tuyến thông minh

## Kết quả mong đợi

- ✅ HTTP Status: 200
- ✅ Response Time: < 10s
- ✅ Có đầy đủ các trường: `agent_id`, `session_id`, `response`, `metadata`
- ✅ `error`: null

## Troubleshooting

- **Lỗi 500**: Kiểm tra logs server
- **Connection Refused**: Đảm bảo server đang chạy
- **Timeout**: Tăng timeout hoặc kiểm tra hiệu suất
- **JSON Error**: Validate JSON trước khi gửi
