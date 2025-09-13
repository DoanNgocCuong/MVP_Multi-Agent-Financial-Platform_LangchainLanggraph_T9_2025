# Hướng dẫn chạy với Dữ liệu Thật - AI Financial Multi-Agent System

## 📋 Tổng quan

Tài liệu này hướng dẫn chi tiết cách chạy AI Financial Multi-Agent System với dữ liệu thật thay vì demo data. Hệ thống hiện tại đang chạy ở **demo mode** với mock data, để chuyển sang **production mode** với dữ liệu thật cần thực hiện các bước cấu hình sau.

**Ngày tạo**: 13/09/2025  
**Version**: 0.1.0  
**Environment**: Production Setup

---

## 🔄 So sánh Demo vs Real Data

### **Demo Mode (Hiện tại):**
```python
# Demo sử dụng mock data
demo_data = {
    "current_assets": 150000,      # Hardcoded
    "current_liabilities": 75000,  # Hardcoded
    "cash_flows": [25000, 28000, 32000, 35000, 30000, 33000]  # Mock data
}
```

### **Real Data Mode (Production):**
```python
# Real data từ database/external systems
real_data = {
    "current_assets": fetch_from_quickbooks(),      # Từ QuickBooks API
    "current_liabilities": fetch_from_erp(),        # Từ ERP system
    "cash_flows": fetch_from_banking_api()          # Từ banking APIs
}
```

---

## 🚀 Các bước Setup với Dữ liệu Thật

### **Bước 1: Cấu hình Environment Variables**

#### **1.1 Tạo file `.env` với cấu hình đầy đủ:**
```bash
# Navigate to src directory
cd "New folder/src"

# Tạo file .env
touch .env
```

#### **1.2 Nội dung file `.env`:**
```env
# ===========================================
# AI FINANCIAL MULTI-AGENT SYSTEM - PRODUCTION CONFIG
# ===========================================

# Environment
ENVIRONMENT=production
DEBUG=false

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# ===========================================
# OPENAI CONFIGURATION (REQUIRED for AI)
# ===========================================
OPENAI_API_KEY=sk-your_actual_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=4000

# ===========================================
# DATABASE CONFIGURATION (REQUIRED for data persistence)
# ===========================================
# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=ai_financial
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=ai_financial

# MongoDB (Optional - for document storage)
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=ai_financial

# Redis (Required - for caching)
REDIS_URL=redis://localhost:6379
REDIS_DB=0

# ===========================================
# SECURITY (REQUIRED for production)
# ===========================================
SECRET_KEY=your_very_secure_secret_key_at_least_32_characters_long
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ===========================================
# EXTERNAL INTEGRATIONS (REAL DATA SOURCES)
# ===========================================
# QuickBooks Integration
QUICKBOOKS_CLIENT_ID=your_quickbooks_client_id
QUICKBOOKS_CLIENT_SECRET=your_quickbooks_client_secret
QUICKBOOKS_SANDBOX=false

# Banking APIs (Plaid)
PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_secret
PLAID_ENVIRONMENT=production

# ERP Integration (SAP/Oracle)
SAP_HOST=your_sap_host
SAP_USERNAME=your_sap_username
SAP_PASSWORD=your_sap_password

# ===========================================
# MONITORING & OBSERVABILITY
# ===========================================
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_HOST=https://cloud.langfuse.com

# OpenTelemetry
OTEL_SERVICE_NAME=ai-financial-system
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# ===========================================
# WORKFLOW CONFIGURATION
# ===========================================
MAX_CONCURRENT_AGENTS=10
CASH_FLOW_FORECAST_WEEKS=13
PL_FORECAST_MONTHS=12
AUTO_APPROVAL_THRESHOLD=1000.0
TWO_MAN_RULE_THRESHOLD=5000.0
```

### **Bước 2: Setup Database Infrastructure**

#### **2.1 PostgreSQL Setup (Required):**
```bash
# Option 1: Sử dụng Docker (Khuyến nghị)
docker run --name postgres-ai-financial \
  -e POSTGRES_USER=ai_financial \
  -e POSTGRES_PASSWORD=your_secure_password \
  -e POSTGRES_DB=ai_financial \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  -d postgres:15

# Option 2: Cài đặt PostgreSQL trực tiếp
# Windows: Download từ https://www.postgresql.org/download/windows/
# Ubuntu: sudo apt-get install postgresql postgresql-contrib
# macOS: brew install postgresql
```

#### **2.2 Redis Setup (Required):**
```bash
# Option 1: Docker
docker run --name redis-ai-financial \
  -p 6379:6379 \
  -v redis_data:/data \
  -d redis:7-alpine

# Option 2: Cài đặt trực tiếp
# Windows: Download từ https://github.com/microsoftarchive/redis/releases
# Ubuntu: sudo apt-get install redis-server
# macOS: brew install redis
```

#### **2.3 MongoDB Setup (Optional):**
```bash
# Docker
docker run --name mongodb-ai-financial \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  -d mongo:7
```

### **Bước 3: Cài đặt Dependencies**

```bash
# Navigate to src directory
cd "New folder/src"

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### **Bước 4: Khởi tạo Database Schema**

```bash
# Tạo tables trong database
python -c "
from ai_financial.core.database import create_tables
create_tables()
print('✅ Database tables created successfully')
"
```

---

## 🔌 Cấu hình External Integrations

### **4.1 QuickBooks Integration (Real Financial Data)**

#### **Setup QuickBooks App:**
1. Truy cập: https://developer.intuit.com/
2. Tạo ứng dụng mới
3. Lấy `Client ID` và `Client Secret`
4. Cấu hình redirect URLs

#### **Cấu hình trong .env:**
```env
QUICKBOOKS_CLIENT_ID=your_actual_client_id
QUICKBOOKS_CLIENT_SECRET=your_actual_client_secret
QUICKBOOKS_SANDBOX=false  # true for testing, false for production
```

#### **Code để fetch real data:**
```python
# Example: Fetch real financial data from QuickBooks
from ai_financial.integrations.quickbooks import QuickBooksClient

async def fetch_real_financial_data():
    qb_client = QuickBooksClient()
    
    # Fetch real balance sheet data
    balance_sheet = await qb_client.get_balance_sheet()
    
    # Fetch real income statement
    income_statement = await qb_client.get_income_statement()
    
    # Fetch real cash flow statement
    cash_flow = await qb_client.get_cash_flow_statement()
    
    return {
        "current_assets": balance_sheet["current_assets"],
        "current_liabilities": balance_sheet["current_liabilities"],
        "revenue": income_statement["total_revenue"],
        "expenses": income_statement["total_expenses"],
        "cash_flows": cash_flow["operating_cash_flows"]
    }
```

### **4.2 Banking API Integration (Plaid)**

#### **Setup Plaid Account:**
1. Truy cập: https://plaid.com/
2. Tạo tài khoản developer
3. Lấy `client_id` và `secret`
4. Cấu hình webhook endpoints

#### **Cấu hình trong .env:**
```env
PLAID_CLIENT_ID=your_actual_plaid_client_id
PLAID_SECRET=your_actual_plaid_secret
PLAID_ENVIRONMENT=production  # sandbox, development, production
```

#### **Code để fetch real banking data:**
```python
# Example: Fetch real banking data from Plaid
from ai_financial.integrations.plaid_client import PlaidClient

async def fetch_real_banking_data():
    plaid_client = PlaidClient()
    
    # Fetch real account balances
    accounts = await plaid_client.get_accounts()
    
    # Fetch real transactions
    transactions = await plaid_client.get_transactions()
    
    # Fetch real cash flow data
    cash_flow = await plaid_client.get_cash_flow()
    
    return {
        "account_balances": accounts,
        "transactions": transactions,
        "cash_flow_data": cash_flow
    }
```

### **4.3 ERP Integration (SAP/Oracle)**

#### **Cấu hình ERP Connection:**
```env
SAP_HOST=your_sap_host
SAP_USERNAME=your_sap_username
SAP_PASSWORD=your_sap_password
SAP_CLIENT=100
```

#### **Code để fetch real ERP data:**
```python
# Example: Fetch real ERP data
from ai_financial.integrations.sap_client import SAPClient

async def fetch_real_erp_data():
    sap_client = SAPClient()
    
    # Fetch real inventory data
    inventory = await sap_client.get_inventory_data()
    
    # Fetch real vendor data
    vendors = await sap_client.get_vendor_data()
    
    # Fetch real customer data
    customers = await sap_client.get_customer_data()
    
    return {
        "inventory": inventory,
        "vendors": vendors,
        "customers": customers
    }
```

---

## 🔄 Chuyển đổi từ Demo sang Real Data

### **5.1 Modify Agent để sử dụng Real Data:**

#### **Before (Demo Mode):**
```python
# ai_financial/agents/advisory/ai_cfo_agent.py
async def _gather_financial_data(self, state: AgentState) -> AgentState:
    # Demo data
    demo_data = {
        "current_assets": 150000,
        "current_liabilities": 75000,
        "revenue": 1500000
    }
    state.financial_data = demo_data
    return state
```

#### **After (Real Data Mode):**
```python
# ai_financial/agents/advisory/ai_cfo_agent.py
async def _gather_financial_data(self, state: AgentState) -> AgentState:
    # Real data from integrations
    real_data = await self._fetch_real_financial_data()
    state.financial_data = real_data
    return state

async def _fetch_real_financial_data(self):
    """Fetch real financial data from external systems."""
    from ai_financial.integrations.quickbooks import QuickBooksClient
    from ai_financial.integrations.plaid_client import PlaidClient
    
    # Fetch from QuickBooks
    qb_client = QuickBooksClient()
    balance_sheet = await qb_client.get_balance_sheet()
    
    # Fetch from banking APIs
    plaid_client = PlaidClient()
    cash_flow = await plaid_client.get_cash_flow()
    
    return {
        "current_assets": balance_sheet["current_assets"],
        "current_liabilities": balance_sheet["current_liabilities"],
        "cash_flows": cash_flow["monthly_flows"],
        "revenue": balance_sheet["total_revenue"],
        "expenses": balance_sheet["total_expenses"]
    }
```

### **5.2 Modify Tools để sử dụng Real Data:**

#### **Before (Demo Mode):**
```python
# ai_financial/mcp/tools/financial_tools.py
class FinancialRatioTool(BaseTool):
    async def execute(self, parameters, context=None) -> ToolResult:
        # Demo calculation with hardcoded data
        current_assets = 150000
        current_liabilities = 75000
        current_ratio = current_assets / current_liabilities
        
        return ToolResult(
            success=True,
            data={
                "current_ratio": current_ratio,
                "current_assets": current_assets,
                "current_liabilities": current_liabilities
            }
        )
```

#### **After (Real Data Mode):**
```python
# ai_financial/mcp/tools/financial_tools.py
class FinancialRatioTool(BaseTool):
    async def execute(self, parameters, context=None) -> ToolResult:
        # Real data from database/integrations
        financial_data = await self._fetch_real_financial_data()
        
        current_assets = financial_data["current_assets"]
        current_liabilities = financial_data["current_liabilities"]
        current_ratio = current_assets / current_liabilities
        
        return ToolResult(
            success=True,
            data={
                "current_ratio": current_ratio,
                "current_assets": current_assets,
                "current_liabilities": current_liabilities,
                "data_source": "quickbooks_api",
                "last_updated": financial_data["last_updated"]
            }
        )
    
    async def _fetch_real_financial_data(self):
        """Fetch real financial data from database."""
        from ai_financial.core.database import get_db
        
        db = next(get_db())
        try:
            # Query real data from database
            financial_data = db.query(FinancialData).order_by(
                FinancialData.updated_at.desc()
            ).first()
            
            return {
                "current_assets": financial_data.current_assets,
                "current_liabilities": financial_data.current_liabilities,
                "last_updated": financial_data.updated_at
            }
        finally:
            db.close()
```

---

## 🚀 Chạy hệ thống với Real Data

### **6.1 Khởi động với Real Configuration:**

```bash
# Navigate to src directory
cd "New folder/src"

# Start với production configuration
python run_demo.py
# Chọn option 2: Start web server

# Hoặc start trực tiếp
python -m ai_financial.main
```

### **6.2 Verify Real Data Integration:**

#### **Test API endpoints với real data:**
```bash
# Health check
curl http://localhost:8000/health

# Test financial ratio calculation với real data
curl -X POST http://localhost:8000/api/v1/tools/financial_ratio_calculator/execute \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "ratio_type": "current_ratio",
      "use_real_data": true
    }
  }'

# Test AI CFO agent với real data
curl -X POST http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze our current financial health using real data",
    "use_real_data": true
  }'
```

### **6.3 Monitor Real Data Processing:**

#### **Check logs:**
```bash
# View application logs
tail -f logs/ai_financial.log

# Check database connections
docker logs postgres-ai-financial

# Check Redis connections
docker logs redis-ai-financial
```

#### **Monitor API calls:**
```bash
# Check external API calls
curl http://localhost:8000/api/v1/status

# View integration status
curl http://localhost:8000/api/v1/integrations/status
```

---

## 📊 Data Flow với Real Data

### **7.1 Real Data Flow Diagram:**
```
External Systems → API Integrations → Database → AI Agents → Analysis Results
     ↓                    ↓              ↓           ↓            ↓
QuickBooks API → QuickBooks Client → PostgreSQL → AI CFO Agent → Financial Report
Banking APIs → Plaid Client → PostgreSQL → Forecasting Agent → Cash Flow Forecast
ERP Systems → SAP Client → PostgreSQL → Alert Agent → Risk Assessment
```

### **7.2 Data Processing Pipeline:**
```python
# Real data processing pipeline
async def process_real_financial_data():
    # 1. Fetch data from external systems
    qb_data = await quickbooks_client.fetch_balance_sheet()
    plaid_data = await plaid_client.fetch_transactions()
    erp_data = await sap_client.fetch_inventory()
    
    # 2. Store in database
    await store_financial_data(qb_data, plaid_data, erp_data)
    
    # 3. Process with AI agents
    cfo_analysis = await ai_cfo_agent.analyze_real_data()
    forecast = await forecasting_agent.predict_real_trends()
    
    # 4. Generate reports
    report = await reporting_agent.generate_executive_report()
    
    return report
```

---

## 🔧 Troubleshooting Real Data Issues

### **8.1 Common Issues:**

#### **Database Connection Issues:**
```bash
# Check PostgreSQL connection
docker exec -it postgres-ai-financial psql -U ai_financial -d ai_financial -c "SELECT 1;"

# Check Redis connection
docker exec -it redis-ai-financial redis-cli ping
```

#### **API Integration Issues:**
```bash
# Test QuickBooks API
curl -X POST http://localhost:8000/api/v1/integrations/quickbooks/test

# Test Plaid API
curl -X POST http://localhost:8000/api/v1/integrations/plaid/test
```

#### **Authentication Issues:**
```bash
# Check OpenAI API key
curl -X POST http://localhost:8000/api/v1/test-openai

# Verify JWT tokens
curl -X POST http://localhost:8000/api/v1/auth/verify
```

### **8.2 Performance Optimization:**

#### **Database Optimization:**
```sql
-- Create indexes for better performance
CREATE INDEX idx_financial_data_updated_at ON financial_data(updated_at);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_accounts_type ON accounts(account_type);
```

#### **Caching Strategy:**
```python
# Cache frequently accessed data
@cache(expire=300)  # 5 minutes
async def get_current_balance():
    return await fetch_from_quickbooks()
```

---

## 📈 Monitoring Real Data Performance

### **9.1 Key Metrics to Monitor:**

```python
# Real data performance metrics
real_data_metrics = {
    "data_freshness": "Last updated: 5 minutes ago",
    "api_response_time": "QuickBooks: 1.2s, Plaid: 0.8s",
    "data_accuracy": "99.8% accuracy rate",
    "integration_health": "All systems operational",
    "processing_time": "AI analysis: 2.3s average"
}
```

### **9.2 Dashboard Setup:**
```bash
# Access monitoring dashboard
curl http://localhost:8000/api/v1/monitoring/dashboard

# View real-time metrics
curl http://localhost:8000/api/v1/monitoring/metrics
```

---

## 🎯 Production Deployment Checklist

### **✅ Pre-deployment Checklist:**
- [ ] Environment variables configured
- [ ] Database connections tested
- [ ] External API integrations verified
- [ ] Security keys properly set
- [ ] Monitoring configured
- [ ] Backup strategy implemented
- [ ] Load testing completed
- [ ] Error handling tested

### **✅ Post-deployment Verification:**
- [ ] Health checks passing
- [ ] Real data flowing correctly
- [ ] AI agents responding with real insights
- [ ] Performance metrics acceptable
- [ ] Monitoring alerts configured
- [ ] User authentication working
- [ ] API endpoints responding

---

## 📝 Conclusion

Chuyển từ demo mode sang real data mode yêu cầu:

1. **✅ Proper Configuration**: Environment variables, database setup, API keys
2. **✅ External Integrations**: QuickBooks, Plaid, ERP systems
3. **✅ Data Pipeline**: Real data fetching, processing, storage
4. **✅ Security**: Production-grade authentication và authorization
5. **✅ Monitoring**: Comprehensive observability và alerting
6. **✅ Performance**: Optimization cho real-time data processing

**System Status**: 🟢 **READY FOR PRODUCTION** với proper configuration

---

*Hướng dẫn được tạo bởi AI Assistant*  
*Ngày tạo: 13/09/2025*  
*Version: 1.0 - Real Data Production Guide*
