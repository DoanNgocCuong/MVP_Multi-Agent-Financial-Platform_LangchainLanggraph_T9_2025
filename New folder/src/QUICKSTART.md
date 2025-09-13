# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install the package in development mode
pip install -e .
```

### 2. Run the Demo

```bash
# Simple startup script (recommended for first time)
python run_demo.py

# Or run the interactive demo directly
python demo.py

# Or use the CLI
python -m ai_financial.cli chat
```

### 3. Explore the System

The system will work in **demo mode** without any configuration. You can:

- ✅ Test financial calculation tools
- ✅ Interact with the system architecture
- ✅ See workflow orchestration
- ⚠️ AI agents will use mock responses (need OpenAI API key for real AI)

## 🔧 Configuration (Optional)

### For Full AI Capabilities

1. Get an OpenAI API key from https://platform.openai.com/
2. Create a `.env` file (or edit the auto-generated one):

```env
OPENAI_API_KEY=sk-your_openai_api_key_here
```

3. Restart the system

### For Production Use

See the full [README.md](README.md) for complete configuration options including:
- Database setup (PostgreSQL, MongoDB, Redis)
- External integrations (QuickBooks, Plaid, etc.)
- Security configuration
- Monitoring setup

## 🎯 What You Can Try

### 1. Financial Tools Demo
```bash
python -m ai_financial.cli test-tool financial_ratio_calculator --params '{"ratio_type": "current_ratio", "financial_data": {"current_assets": 100000, "current_liabilities": 50000}}'
```

### 2. Interactive Chat
```bash
python -m ai_financial.cli chat
```

### 3. Web Interface
```bash
python -m ai_financial.main
# Then visit http://localhost:8000
```

### 4. System Status
```bash
python -m ai_financial.cli status
```

## 🐛 Troubleshooting

### "SECRET_KEY must be set" Error
- **Solution**: The system now auto-generates a development key
- **For Production**: Set `SECRET_KEY` environment variable

### "OpenAI API key not configured"
- **Solution**: This is normal for demo mode
- **For Full AI**: Add `OPENAI_API_KEY` to `.env` file

### Import Errors
- **Solution**: Install dependencies with `pip install -r requirements.txt`
- **Alternative**: Install with `pip install -e .`

### Permission Errors
- **Solution**: Make sure you're in the `src/` directory
- **Alternative**: Use `python -m ai_financial.main` instead of direct imports

## 📚 Next Steps

1. **Try the Demo**: Run `python run_demo.py` to see all capabilities
2. **Add OpenAI Key**: For real AI agent interactions
3. **Read Documentation**: See [README.md](README.md) for full features
4. **Customize**: Add your own agents and tools
5. **Deploy**: Configure for your production environment

## 🆘 Need Help?

- Check the [README.md](README.md) for detailed documentation
- Run `python run_demo.py` for guided setup
- Look at `demo.py` for usage examples
- Check `tests/` directory for test examples