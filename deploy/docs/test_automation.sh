#!/bin/bash
# AI Financial Multi-Agent System - Automated Testing Script
# Usage: ./test_automation.sh [test_type]
# test_type: all, agents, workflows, tools, performance

set -e

BASE_URL="http://localhost:8000"
TEST_TYPE=${1:-all}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "INFO") echo -e "${BLUE}ℹ️  $message${NC}" ;;
        "SUCCESS") echo -e "${GREEN}✅ $message${NC}" ;;
        "WARNING") echo -e "${YELLOW}⚠️  $message${NC}" ;;
        "ERROR") echo -e "${RED}❌ $message${NC}" ;;
    esac
}

# Function to test HTTP endpoint
test_endpoint() {
    local method=$1
    local url=$2
    local data=$3
    local expected_status=${4:-200}
    
    local response
    local http_code
    
    if [ -n "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            -H "Content-Type: application/json" \
            -d "$data")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            -H "Content-Type: application/json")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    response_body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" -eq "$expected_status" ]; then
        print_status "SUCCESS" "HTTP $http_code - $url"
        return 0
    else
        print_status "ERROR" "HTTP $http_code (expected $expected_status) - $url"
        echo "Response: $response_body"
        return 1
    fi
}

# Function to test system status
test_system_status() {
    print_status "INFO" "Testing System Status..."
    
    # Test health endpoint
    test_endpoint "GET" "$BASE_URL/health" "" 200
    
    # Test status endpoint
    test_endpoint "GET" "$BASE_URL/api/v1/status" "" 200
    
    # Test root endpoint
    test_endpoint "GET" "$BASE_URL/" "" 200
}

# Function to test agents
test_agents() {
    print_status "INFO" "Testing Agents..."
    
    local agent_tests=(
        "Phân tích tình hình tài chính của công ty chúng tôi trong quý 3"
        "Dự báo tài chính cho quý 4 và năm sau"
        "Đánh giá rủi ro tài chính và đưa ra khuyến nghị"
        "Tạo báo cáo tài chính tổng hợp cho ban lãnh đạo"
        "So sánh hiệu suất tài chính với các công ty cùng ngành"
    )
    
    for message in "${agent_tests[@]}"; do
        test_endpoint "POST" "$BASE_URL/api/v1/agents/ai_cfo_agent/invoke" \
            "{\"message\": \"$message\"}" 200
    done
}

# Function to test workflows
test_workflows() {
    print_status "INFO" "Testing Workflows..."
    
    # Test advisory workflow
    test_endpoint "POST" "$BASE_URL/api/v1/workflows/advisory/execute" \
        '{"message": "Cần tư vấn tài chính chiến lược cho quyết định đầu tư mới"}' 200
    
    # Test transactional workflow
    test_endpoint "POST" "$BASE_URL/api/v1/workflows/transactional/execute" \
        '{"message": "Xử lý và phân loại các giao dịch tài chính trong tháng"}' 200
    
    # Test workflow streaming
    test_endpoint "GET" "$BASE_URL/api/v1/workflows/advisory/stream?message=Test streaming workflow" "" 200
}

# Function to test tools
test_tools() {
    print_status "INFO" "Testing Tools..."
    
    # Test list tools
    test_endpoint "GET" "$BASE_URL/api/v1/tools" "" 200
    
    # Test financial ratio calculator
    test_endpoint "POST" "$BASE_URL/api/v1/tools/financial_ratio_calculator/execute" \
        '{
            "ratio_type": "current_ratio",
            "financial_data": {
                "current_assets": 100000,
                "current_liabilities": 50000
            }
        }' 200
    
    # Test cash flow analyzer
    test_endpoint "POST" "$BASE_URL/api/v1/tools/cash_flow_analyzer/execute" \
        '{
            "cash_flows": [
                {
                    "period": "2025-Q1",
                    "operating_cash_flow": 50000,
                    "investing_cash_flow": -10000,
                    "financing_cash_flow": -5000,
                    "net_cash_flow": 35000
                }
            ],
            "analysis_type": "trend"
        }' 200
    
    # Test profitability analyzer
    test_endpoint "POST" "$BASE_URL/api/v1/tools/profitability_analyzer/execute" \
        '{
            "financial_data": {
                "revenue": 1000000,
                "cost_of_goods_sold": 600000,
                "operating_expenses": 200000,
                "net_income": 150000,
                "total_assets": 2000000,
                "total_equity": 1200000
            },
            "analysis_type": "comprehensive"
        }' 200
}

# Function to test performance
test_performance() {
    print_status "INFO" "Testing Performance..."
    
    local start_time
    local end_time
    local duration
    
    # Test response time
    start_time=$(date +%s.%N)
    test_endpoint "POST" "$BASE_URL/api/v1/agents/ai_cfo_agent/invoke" \
        '{"message": "Test performance"}' 200
    end_time=$(date +%s.%N)
    duration=$(echo "$end_time - $start_time" | bc)
    
    if (( $(echo "$duration < 10" | bc -l) )); then
        print_status "SUCCESS" "Response time: ${duration}s (Good)"
    elif (( $(echo "$duration < 30" | bc -l) )); then
        print_status "WARNING" "Response time: ${duration}s (Acceptable)"
    else
        print_status "ERROR" "Response time: ${duration}s (Too slow)"
    fi
}

# Function to test intelligent routing
test_intelligent_routing() {
    print_status "INFO" "Testing Intelligent Routing..."
    
    local routing_tests=(
        "Tôi cần dự báo tài chính cho quý tới"
        "Tạo báo cáo tài chính tổng hợp"
        "Đánh giá rủi ro và cảnh báo"
    )
    
    for message in "${routing_tests[@]}"; do
        test_endpoint "POST" "$BASE_URL/api/v1/agents/ai_cfo_agent/invoke" \
            "{\"message\": \"$message\"}" 200
    done
}

# Function to run comprehensive test
run_comprehensive_test() {
    print_status "INFO" "Running Comprehensive Test Suite..."
    
    local total_tests=0
    local passed_tests=0
    
    # Count total tests
    total_tests=$((total_tests + 3))  # System status
    total_tests=$((total_tests + 5))  # Agents
    total_tests=$((total_tests + 3))  # Workflows
    total_tests=$((total_tests + 4))  # Tools
    total_tests=$((total_tests + 1))  # Performance
    total_tests=$((total_tests + 3))  # Intelligent routing
    
    # Run tests
    test_system_status && passed_tests=$((passed_tests + 3))
    test_agents && passed_tests=$((passed_tests + 5))
    test_workflows && passed_tests=$((passed_tests + 3))
    test_tools && passed_tests=$((passed_tests + 4))
    test_performance && passed_tests=$((passed_tests + 1))
    test_intelligent_routing && passed_tests=$((passed_tests + 3))
    
    # Print summary
    echo ""
    print_status "INFO" "Test Summary:"
    echo "Total Tests: $total_tests"
    echo "Passed: $passed_tests"
    echo "Failed: $((total_tests - passed_tests))"
    
    if [ $passed_tests -eq $total_tests ]; then
        print_status "SUCCESS" "All tests passed! 🎉"
        exit 0
    else
        print_status "ERROR" "Some tests failed! 😞"
        exit 1
    fi
}

# Main execution
main() {
    echo "🔍 AI Financial Multi-Agent System - Automated Testing"
    echo "======================================================"
    echo "Base URL: $BASE_URL"
    echo "Test Type: $TEST_TYPE"
    echo ""
    
    case $TEST_TYPE in
        "all")
            run_comprehensive_test
            ;;
        "status")
            test_system_status
            ;;
        "agents")
            test_agents
            ;;
        "workflows")
            test_workflows
            ;;
        "tools")
            test_tools
            ;;
        "performance")
            test_performance
            ;;
        "routing")
            test_intelligent_routing
            ;;
        *)
            echo "Usage: $0 [all|status|agents|workflows|tools|performance|routing]"
            exit 1
            ;;
    esac
}

# Check if required tools are installed
check_dependencies() {
    local missing_deps=()
    
    if ! command -v curl &> /dev/null; then
        missing_deps+=("curl")
    fi
    
    if ! command -v jq &> /dev/null; then
        missing_deps+=("jq")
    fi
    
    if ! command -v bc &> /dev/null; then
        missing_deps+=("bc")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_status "ERROR" "Missing dependencies: ${missing_deps[*]}"
        print_status "INFO" "Please install missing dependencies and try again"
        exit 1
    fi
}

# Run main function
check_dependencies
main
