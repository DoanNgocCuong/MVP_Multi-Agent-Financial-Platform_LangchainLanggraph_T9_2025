# Test all agents in the system
Write-Host "🔍 AI Financial Multi-Agent System - Agent Testing" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Test AI CFO Agent (should work)
Write-Host "1. Testing AI CFO Agent..." -ForegroundColor Yellow
$body = '{"message": "Test AI CFO Agent functionality"}'
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke" -Method POST -Body $body -Headers @{"Content-Type"="application/json"}
    Write-Host "✅ AI CFO Agent: SUCCESS" -ForegroundColor Green
    Write-Host "   Agent ID: $($response.agent_id)" -ForegroundColor Cyan
    Write-Host "   Session ID: $($response.session_id)" -ForegroundColor Cyan
    Write-Host "   Response Length: $($response.response.Length) characters" -ForegroundColor Cyan
} catch {
    Write-Host "❌ AI CFO Agent: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test Forecasting Agent (should fail)
Write-Host "2. Testing Forecasting Agent..." -ForegroundColor Yellow
$body = '{"message": "Test forecasting agent"}'
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/agents/forecasting_agent/invoke" -Method POST -Body $body -Headers @{"Content-Type"="application/json"}
    Write-Host "✅ Forecasting Agent: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "❌ Forecasting Agent: FAILED (Expected)" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test Alert Agent (should fail)
Write-Host "3. Testing Alert Agent..." -ForegroundColor Yellow
$body = '{"message": "Test alert agent"}'
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/agents/alert_agent/invoke" -Method POST -Body $body -Headers @{"Content-Type"="application/json"}
    Write-Host "✅ Alert Agent: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "❌ Alert Agent: FAILED (Expected)" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test Reporting Agent (should fail)
Write-Host "4. Testing Reporting Agent..." -ForegroundColor Yellow
$body = '{"message": "Test reporting agent"}'
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/agents/reporting_agent/invoke" -Method POST -Body $body -Headers @{"Content-Type"="application/json"}
    Write-Host "✅ Reporting Agent: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "❌ Reporting Agent: FAILED (Expected)" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test OCR Agent (should fail)
Write-Host "5. Testing OCR Agent..." -ForegroundColor Yellow
$body = '{"message": "Test OCR agent"}'
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/agents/ocr_agent/invoke" -Method POST -Body $body -Headers @{"Content-Type"="application/json"}
    Write-Host "✅ OCR Agent: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "❌ OCR Agent: FAILED (Expected)" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test Data Sync Agent (should fail)
Write-Host "6. Testing Data Sync Agent..." -ForegroundColor Yellow
$body = '{"message": "Test data sync agent"}'
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/agents/data_sync_agent/invoke" -Method POST -Body $body -Headers @{"Content-Type"="application/json"}
    Write-Host "✅ Data Sync Agent: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "❌ Data Sync Agent: FAILED (Expected)" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test Reconciliation Agent (should fail)
Write-Host "7. Testing Reconciliation Agent..." -ForegroundColor Yellow
$body = '{"message": "Test reconciliation agent"}'
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/agents/reconciliation_agent/invoke" -Method POST -Body $body -Headers @{"Content-Type"="application/json"}
    Write-Host "✅ Reconciliation Agent: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "❌ Reconciliation Agent: FAILED (Expected)" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

Write-Host "🎯 Agent Testing Summary:" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host "✅ AI CFO Agent: ACTIVE (1/7 agents)" -ForegroundColor Green
Write-Host "❌ Other Agents: NOT IMPLEMENTED (6/7 agents)" -ForegroundColor Red
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "- Implement remaining 6 agents" -ForegroundColor White
Write-Host "- Test intelligent routing" -ForegroundColor White
Write-Host "- Add agent-specific functionality" -ForegroundColor White
