# AI Financial Multi-Agent System - Automated Testing Script (PowerShell)
# Usage: .\test_automation.ps1 [test_type]
# test_type: all, agents, workflows, tools, performance

param(
    [string]$TestType = "all"
)

$BaseUrl = "http://localhost:8000"
$ErrorActionPreference = "Stop"

# Function to print colored output
function Write-Status {
    param(
        [string]$Status,
        [string]$Message
    )
    
    switch ($Status) {
        "INFO" { Write-Host "ℹ️  $Message" -ForegroundColor Blue }
        "SUCCESS" { Write-Host "✅ $Message" -ForegroundColor Green }
        "WARNING" { Write-Host "⚠️  $Message" -ForegroundColor Yellow }
        "ERROR" { Write-Host "❌ $Message" -ForegroundColor Red }
    }
}

# Function to test HTTP endpoint
function Test-Endpoint {
    param(
        [string]$Method,
        [string]$Url,
        [string]$Data = $null,
        [int]$ExpectedStatus = 200
    )
    
    try {
        $headers = @{
            "Content-Type" = "application/json"
        }
        
        if ($Data) {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -Body $Data -Headers $headers
        } else {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -Headers $headers
        }
        
        Write-Status "SUCCESS" "HTTP 200 - $Url"
        return $true
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Status "ERROR" "HTTP $statusCode (expected $ExpectedStatus) - $Url"
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to test system status
function Test-SystemStatus {
    Write-Status "INFO" "Testing System Status..."
    
    $tests = @(
        @{ Method = "GET"; Url = "$BaseUrl/health" },
        @{ Method = "GET"; Url = "$BaseUrl/api/v1/status" },
        @{ Method = "GET"; Url = "$BaseUrl/" }
    )
    
    $passed = 0
    foreach ($test in $tests) {
        if (Test-Endpoint -Method $test.Method -Url $test.Url) {
            $passed++
        }
    }
    
    return $passed -eq $tests.Count
}

# Function to test agents
function Test-Agents {
    Write-Status "INFO" "Testing Agents..."
    
    $agentTests = @(
        "Phân tích tình hình tài chính của công ty chúng tôi trong quý 3",
        "Dự báo tài chính cho quý 4 và năm sau",
        "Đánh giá rủi ro tài chính và đưa ra khuyến nghị",
        "Tạo báo cáo tài chính tổng hợp cho ban lãnh đạo",
        "So sánh hiệu suất tài chính với các công ty cùng ngành"
    )
    
    $passed = 0
    foreach ($message in $agentTests) {
        $data = @{
            message = $message
        } | ConvertTo-Json
        
        if (Test-Endpoint -Method "POST" -Url "$BaseUrl/api/v1/agents/ai_cfo_agent/invoke" -Data $data) {
            $passed++
        }
    }
    
    return $passed -eq $agentTests.Count
}

# Function to test workflows
function Test-Workflows {
    Write-Status "INFO" "Testing Workflows..."
    
    $workflowTests = @(
        @{
            Method = "POST"
            Url = "$BaseUrl/api/v1/workflows/advisory/execute"
            Data = @{
                message = "Cần tư vấn tài chính chiến lược cho quyết định đầu tư mới"
            } | ConvertTo-Json
        },
        @{
            Method = "POST"
            Url = "$BaseUrl/api/v1/workflows/transactional/execute"
            Data = @{
                message = "Xử lý và phân loại các giao dịch tài chính trong tháng"
            } | ConvertTo-Json
        },
        @{
            Method = "GET"
            Url = "$BaseUrl/api/v1/workflows/advisory/stream?message=Test streaming workflow"
        }
    )
    
    $passed = 0
    foreach ($test in $workflowTests) {
        if (Test-Endpoint -Method $test.Method -Url $test.Url -Data $test.Data) {
            $passed++
        }
    }
    
    return $passed -eq $workflowTests.Count
}

# Function to test tools
function Test-Tools {
    Write-Status "INFO" "Testing Tools..."
    
    $toolTests = @(
        @{
            Method = "GET"
            Url = "$BaseUrl/api/v1/tools"
        },
        @{
            Method = "POST"
            Url = "$BaseUrl/api/v1/tools/financial_ratio_calculator/execute"
            Data = @{
                ratio_type = "current_ratio"
                financial_data = @{
                    current_assets = 100000
                    current_liabilities = 50000
                }
            } | ConvertTo-Json -Depth 3
        },
        @{
            Method = "POST"
            Url = "$BaseUrl/api/v1/tools/cash_flow_analyzer/execute"
            Data = @{
                cash_flows = @(
                    @{
                        period = "2025-Q1"
                        operating_cash_flow = 50000
                        investing_cash_flow = -10000
                        financing_cash_flow = -5000
                        net_cash_flow = 35000
                    }
                )
                analysis_type = "trend"
            } | ConvertTo-Json -Depth 3
        },
        @{
            Method = "POST"
            Url = "$BaseUrl/api/v1/tools/profitability_analyzer/execute"
            Data = @{
                financial_data = @{
                    revenue = 1000000
                    cost_of_goods_sold = 600000
                    operating_expenses = 200000
                    net_income = 150000
                    total_assets = 2000000
                    total_equity = 1200000
                }
                analysis_type = "comprehensive"
            } | ConvertTo-Json -Depth 3
        }
    )
    
    $passed = 0
    foreach ($test in $toolTests) {
        if (Test-Endpoint -Method $test.Method -Url $test.Url -Data $test.Data) {
            $passed++
        }
    }
    
    return $passed -eq $toolTests.Count
}

# Function to test performance
function Test-Performance {
    Write-Status "INFO" "Testing Performance..."
    
    $data = @{
        message = "Test performance"
    } | ConvertTo-Json
    
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    $result = Test-Endpoint -Method "POST" -Url "$BaseUrl/api/v1/agents/ai_cfo_agent/invoke" -Data $data
    $stopwatch.Stop()
    
    $duration = $stopwatch.Elapsed.TotalSeconds
    
    if ($duration -lt 10) {
        Write-Status "SUCCESS" "Response time: $([math]::Round($duration, 2))s (Good)"
    } elseif ($duration -lt 30) {
        Write-Status "WARNING" "Response time: $([math]::Round($duration, 2))s (Acceptable)"
    } else {
        Write-Status "ERROR" "Response time: $([math]::Round($duration, 2))s (Too slow)"
    }
    
    return $result
}

# Function to test intelligent routing
function Test-IntelligentRouting {
    Write-Status "INFO" "Testing Intelligent Routing..."
    
    $routingTests = @(
        "Tôi cần dự báo tài chính cho quý tới",
        "Tạo báo cáo tài chính tổng hợp",
        "Đánh giá rủi ro và cảnh báo"
    )
    
    $passed = 0
    foreach ($message in $routingTests) {
        $data = @{
            message = $message
        } | ConvertTo-Json
        
        if (Test-Endpoint -Method "POST" -Url "$BaseUrl/api/v1/agents/ai_cfo_agent/invoke" -Data $data) {
            $passed++
        }
    }
    
    return $passed -eq $routingTests.Count
}

# Function to run comprehensive test
function Invoke-ComprehensiveTest {
    Write-Status "INFO" "Running Comprehensive Test Suite..."
    
    $totalTests = 19  # Total number of tests
    $passedTests = 0
    
    # Run tests
    if (Test-SystemStatus) { $passedTests += 3 }
    if (Test-Agents) { $passedTests += 5 }
    if (Test-Workflows) { $passedTests += 3 }
    if (Test-Tools) { $passedTests += 4 }
    if (Test-Performance) { $passedTests += 1 }
    if (Test-IntelligentRouting) { $passedTests += 3 }
    
    # Print summary
    Write-Host ""
    Write-Status "INFO" "Test Summary:"
    Write-Host "Total Tests: $totalTests"
    Write-Host "Passed: $passedTests"
    Write-Host "Failed: $($totalTests - $passedTests)"
    
    if ($passedTests -eq $totalTests) {
        Write-Status "SUCCESS" "All tests passed! 🎉"
        exit 0
    } else {
        Write-Status "ERROR" "Some tests failed! 😞"
        exit 1
    }
}

# Main execution
function Main {
    Write-Host "🔍 AI Financial Multi-Agent System - Automated Testing" -ForegroundColor Cyan
    Write-Host "======================================================" -ForegroundColor Cyan
    Write-Host "Base URL: $BaseUrl"
    Write-Host "Test Type: $TestType"
    Write-Host ""
    
    switch ($TestType) {
        "all" { Invoke-ComprehensiveTest }
        "status" { Test-SystemStatus }
        "agents" { Test-Agents }
        "workflows" { Test-Workflows }
        "tools" { Test-Tools }
        "performance" { Test-Performance }
        "routing" { Test-IntelligentRouting }
        default {
            Write-Host "Usage: .\test_automation.ps1 [all|status|agents|workflows|tools|performance|routing]"
            exit 1
        }
    }
}

# Check if required modules are available
function Test-Dependencies {
    try {
        # Test if Invoke-RestMethod is available
        $null = Get-Command Invoke-RestMethod -ErrorAction Stop
        return $true
    }
    catch {
        Write-Status "ERROR" "PowerShell version too old or missing required cmdlets"
        Write-Status "INFO" "Please use PowerShell 5.1 or later"
        return $false
    }
}

# Run main function
if (Test-Dependencies) {
    Main
} else {
    exit 1
}
