# 🔄 LangFuse vs LangSmith - Configuration Guide

## **Tình Trạng Hiện Tại:**

### ✅ **Bạn đang sử dụng LangFuse** (không phải LangSmith)

**Bằng chứng:**
- Code có comment: `### LangFuse (Recommended - Free)`
- Import statements: `from langfuse import Langfuse`
- Không có file `.env` để cấu hình

### 🚨 **Vấn Đề:**

**LangGraph Studio** đang cố gắng kết nối với **LangSmith** để tracing, nhưng bạn muốn dùng **LangFuse**.

## **Giải Pháp:**

### **1. Tạo File `.env` với LangFuse Config**

Tạo file `deploy/src/.env` với nội dung:

```bash
# LangFuse Configuration (Free Alternative to LangSmith)
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
LANGFUSE_HOST=https://cloud.langfuse.com

# Disable LangSmith (since we're using LangFuse)
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=
LANGSMITH_ENDPOINT=

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Other configurations
LOG_LEVEL=INFO
DEBUG=false
```

### **2. Cấu Hình LangFuse**

#### **Option A: Sử dụng LangFuse Cloud (Free)**
1. Đăng ký tại: https://cloud.langfuse.com
2. Lấy `LANGFUSE_PUBLIC_KEY` và `LANGFUSE_SECRET_KEY`
3. Cập nhật file `.env`

#### **Option B: Self-hosted LangFuse**
1. Chạy LangFuse locally: `docker run -p 3000:3000 langfuse/langfuse`
2. Set `LANGFUSE_HOST=http://localhost:3000`

### **3. Disable LangSmith trong LangGraph Studio**

Thêm vào file `.env`:
```bash
# Disable LangSmith completely
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=
LANGSMITH_ENDPOINT=
```

### **4. Restart LangGraph Studio**

```bash
# Stop current LangGraph Studio
Ctrl+C

# Restart with new config
langgraph dev
```

## **So Sánh LangFuse vs LangSmith:**

| Feature | LangFuse | LangSmith |
|---------|----------|-----------|
| **Cost** | ✅ Free (self-hosted) | ❌ Paid |
| **Graph Visualization** | ✅ Yes | ✅ Yes |
| **Trace Monitoring** | ✅ Yes | ✅ Yes |
| **Performance Metrics** | ✅ Yes | ✅ Yes |
| **Error Tracking** | ✅ Yes | ✅ Yes |
| **Open Source** | ✅ Yes | ❌ No |
| **Self-hosting** | ✅ Yes | ❌ No |

## **Tại Sao Chọn LangFuse:**

1. **✅ Miễn phí** - Không có giới hạn usage
2. **✅ Open source** - Có thể customize
3. **✅ Self-hosted** - Kiểm soát dữ liệu
4. **✅ Tương thích** - Hỗ trợ LangChain/LangGraph
5. **✅ Feature-rich** - Đầy đủ tính năng tracing

## **Test Configuration:**

### **1. Test LangFuse Connection**
```python
from langfuse import Langfuse

langfuse = Langfuse()
print("LangFuse connected successfully!")
```

### **2. Test LangGraph Studio**
1. Truy cập: http://localhost:8123
2. Kiểm tra không còn LangSmith errors
3. Test graph visualization

## **Troubleshooting:**

### **Issue 1: Still seeing LangSmith errors**
**Solution**: Đảm bảo `LANGSMITH_API_KEY=` (empty) trong `.env`

### **Issue 2: LangFuse connection failed**
**Solution**: Kiểm tra `LANGFUSE_PUBLIC_KEY` và `LANGFUSE_SECRET_KEY`

### **Issue 3: Graph not loading**
**Solution**: Restart LangGraph Studio sau khi cập nhật `.env`

## **Next Steps:**

1. **Tạo file `.env`** với LangFuse config
2. **Restart LangGraph Studio**
3. **Test graph visualization**
4. **Enjoy free tracing!** 🎉

---

## 🎯 **Kết Luận**

Bạn đang sử dụng **LangFuse** (đúng choice!), nhưng cần cấu hình để LangGraph Studio không tìm LangSmith. Sau khi setup `.env` file, bạn sẽ có:

- ✅ **Free tracing** với LangFuse
- ✅ **Graph visualization** trong LangGraph Studio  
- ✅ **No LangSmith errors**
- ✅ **Full observability** cho AI CFO Agent

---
*LangFuse vs LangSmith Configuration Guide - 2025-09-20 UTC*
