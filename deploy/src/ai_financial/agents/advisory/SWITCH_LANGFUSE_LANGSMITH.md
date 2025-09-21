# 🔄 Cách Chuyển Đổi LangFuse ↔ LangSmith

## **Tạo File .env để Cấu Hình**

Tạo file `deploy/src/.env` với một trong hai cấu hình sau:

---

## **Option 1: Sử Dụng LangFuse (Free)**

```bash
# ===== LANGFUSE CONFIGURATION (FREE) =====
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
LANGFUSE_HOST=https://cloud.langfuse.com

# Disable LangSmith
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=
LANGSMITH_ENDPOINT=

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Other settings
LOG_LEVEL=INFO
DEBUG=false
```

---

## **Option 2: Sử Dụng LangSmith (Paid)**

```bash
# ===== LANGSMITH CONFIGURATION (PAID) =====
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=your_project_name
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

# Disable LangFuse
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_HOST=

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Other settings
LOG_LEVEL=INFO
DEBUG=false
```

---

## **Cách Lấy API Keys:**

### **LangFuse (Free):**
1. Đăng ký tại: https://cloud.langfuse.com
2. Tạo project mới
3. Vào Settings → API Keys
4. Copy `Public Key` và `Secret Key`

### **LangSmith (Paid):**
1. Đăng ký tại: https://smith.langchain.com
2. Tạo project mới
3. Vào Settings → API Keys
4. Copy `API Key`

---

## **Cách Chuyển Đổi:**

### **Từ LangFuse → LangSmith:**
1. Comment LangFuse config:
```bash
# LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
# LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
# LANGFUSE_HOST=https://cloud.langfuse.com
```

2. Uncomment LangSmith config:
```bash
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=your_project_name
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

### **Từ LangSmith → LangFuse:**
1. Comment LangSmith config:
```bash
# LANGSMITH_API_KEY=your_langsmith_api_key_here
# LANGSMITH_PROJECT=your_project_name
# LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

2. Uncomment LangFuse config:
```bash
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

## **Restart LangGraph Studio:**

Sau khi thay đổi config:

```bash
# Stop current server
Ctrl+C

# Restart with new config
langgraph dev
```

---

## **So Sánh Chi Tiết:**

| Feature | LangFuse | LangSmith |
|---------|----------|-----------|
| **Cost** | ✅ Free | ❌ $5/month+ |
| **Setup** | ✅ Easy | ✅ Easy |
| **Graph Visualization** | ✅ Yes | ✅ Yes |
| **Trace Monitoring** | ✅ Yes | ✅ Yes |
| **Performance Metrics** | ✅ Yes | ✅ Yes |
| **Error Tracking** | ✅ Yes | ✅ Yes |
| **Open Source** | ✅ Yes | ❌ No |
| **Self-hosting** | ✅ Yes | ❌ No |
| **Community** | ✅ Growing | ✅ Mature |
| **Documentation** | ✅ Good | ✅ Excellent |

---

## **Recommendation:**

### **Chọn LangFuse nếu:**
- ✅ Muốn miễn phí
- ✅ Cần self-hosting
- ✅ Muốn open source
- ✅ Dự án nhỏ/medium

### **Chọn LangSmith nếu:**
- ✅ Có budget
- ✅ Cần enterprise features
- ✅ Muốn support tốt
- ✅ Dự án lớn/production

---

## **Test Configuration:**

### **Test LangFuse:**
```python
from langfuse import Langfuse

try:
    langfuse = Langfuse()
    print("✅ LangFuse connected successfully!")
except Exception as e:
    print(f"❌ LangFuse error: {e}")
```

### **Test LangSmith:**
```python
from langsmith import Client

try:
    client = Client()
    print("✅ LangSmith connected successfully!")
except Exception as e:
    print(f"❌ LangSmith error: {e}")
```

---

## **Troubleshooting:**

### **Issue 1: Still seeing old provider errors**
**Solution**: Restart LangGraph Studio sau khi thay đổi `.env`

### **Issue 2: API key invalid**
**Solution**: Kiểm tra API key trong dashboard của provider

### **Issue 3: Connection timeout**
**Solution**: Kiểm tra network và endpoint URL

---

## **Quick Switch Commands:**

### **Enable LangFuse:**
```bash
# Edit .env file
LANGFUSE_PUBLIC_KEY=your_key
LANGSMITH_API_KEY=
```

### **Enable LangSmith:**
```bash
# Edit .env file
LANGSMITH_API_KEY=your_key
LANGFUSE_PUBLIC_KEY=
```

---

## 🎯 **Kết Luận**

Bạn có thể dễ dàng chuyển đổi giữa LangFuse và LangSmith bằng cách:

1. **Tạo file `.env`** với config tương ứng
2. **Comment/uncomment** các dòng config
3. **Restart LangGraph Studio**
4. **Test connection**

**Recommendation**: Bắt đầu với **LangFuse** (free) để test, sau đó chuyển sang **LangSmith** nếu cần enterprise features! 🚀

---
*Switch LangFuse ↔ LangSmith Guide - 2025-09-20 UTC*
