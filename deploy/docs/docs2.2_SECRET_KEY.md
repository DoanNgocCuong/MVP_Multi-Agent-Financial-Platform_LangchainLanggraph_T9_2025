Let me explain what the `SECRET_KEY` is and why it's important for the AI Financial Multi-Agent System.

[1 tool called]

## 🔐 SECRET_KEY là gì?

**SECRET_KEY** là một **khóa bí mật** được sử dụng để bảo mật hệ thống AI Financial Multi-Agent. Đây là một chuỗi ký tự dài ít nhất 32 ký tự.

### **Mục đích sử dụng:**

1. **🔑 JWT Token Signing**: Dùng để ký và xác thực JWT tokens cho API authentication
2. **�� Data Encryption**: Mã hóa dữ liệu nhạy cảm trong hệ thống
3. **��️ Session Security**: Bảo mật phiên làm việc của người dùng
4. **�� API Security**: Bảo vệ các API endpoints

### **Tại sao cần ít nhất 32 ký tự?**

```python
@validator("secret_key")
def validate_secret_key(cls, v: str) -> str:
    if not v:
        raise ValueError("SECRET_KEY must be set")
    if len(v) < 32:
        raise ValueError("SECRET_KEY must be at least 32 characters long")
    return v
```

- **32 ký tự** đảm bảo độ bảo mật cao (256-bit security)
- Khó bị **brute force attack**
- Tuân thủ các tiêu chuẩn bảo mật hiện đại

### **Cách tạo SECRET_KEY:**

#### **Option 1: Sử dụng Python**

```python
import secrets
import string

# Tạo SECRET_KEY ngẫu nhiên 64 ký tự
secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(64))
print(secret_key)
```

#### **Option 2: Sử dụng OpenSSL**

```bash
# Tạo SECRET_KEY 64 ký tự
openssl rand -base64 48
```

#### **Option 3: Sử dụng online generator**

- Truy cập: https://generate-secret.vercel.app/64
- Chọn độ dài 64 ký tự

### **Ví dụ SECRET_KEY hợp lệ:**

```env
# Ví dụ SECRET_KEY (KHÔNG sử dụng trong production!)
SECRET_KEY=Kj8#mN2$pL9@vR4&wX7!qE1%tY6*uI3^oP5+sA8-dF0=gH2~zC4`bV7|nM1

# Hoặc
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6A7B8C9D0E1F2G3H4I5J6K7L8M9N0O1P2Q3R4S5T6U7V8W9X0Y1Z2
```

### **⚠️ Lưu ý quan trọng:**

1. **KHÔNG BAO GIỜ** chia sẻ SECRET_KEY này
2. **KHÔNG** commit vào Git repository
3. **Sử dụng khác nhau** cho môi trường development, staging, production
4. **Thay đổi định kỳ** trong production
5. **Lưu trữ an toàn** (environment variables, secret management systems)

### **Trong hệ thống AI Financial:**

```python
# SECRET_KEY được sử dụng cho:
- JWT token signing (API authentication)
- Data encryption (financial data protection)
- Session management (user sessions)
- API security (request signing)
```

**Tóm lại:** SECRET_KEY là "chìa khóa" bảo mật quan trọng nhất của hệ thống, giúp bảo vệ dữ liệu tài chính nhạy cảm và xác thực người dùng.
