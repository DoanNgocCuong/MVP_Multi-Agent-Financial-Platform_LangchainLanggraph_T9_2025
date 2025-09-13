.venv/Scripts/activate

cd src 


```bash
💡 Tại sao pip install -e . tốt hơn pip install -r requirements.txt?
pip install -e . (Editable install):
✅ Cài package như một editable package
✅ Có thể chạy ai-financial command
✅ Tự động cài đúng dependencies từ pyproject.toml
✅ Development mode - thay đổi code không cần reinstall
✅ Có metadata đầy đủ
pip install -r requirements.txt:
❌ Chỉ cài dependencies
❌ Không có package metadata
❌ Không có entry points
❌ Không có tool configuration
```

```bash
# Simple startup script (recommended for first time)
python run_demo.py

# Or run the interactive demo directly
python demo.py

# Or use the CLI
python -m ai_financial.cli chat

# Start the server
ai-financial start

# Interactive chat
ai-financial chat
```