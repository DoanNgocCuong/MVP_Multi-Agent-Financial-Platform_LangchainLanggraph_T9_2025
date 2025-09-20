# AI Financial Multi-Agent System - API Documentation

## Base

- GET `/` 
  - Returns basic service info.
  - Example (PowerShell):
    ```powershell
    (iwr -UseBasicParsing http://localhost:8000/).Content
    ```

- GET `/health`
  - Returns orchestrator and tool hub health.
  - Example:
    ```powershell
    (iwr -UseBasicParsing http://localhost:8000/health).Content
    ```

- GET `/api/v1/status`
  - Full system status and configuration.
  - Example:
    ```powershell
    (iwr -UseBasicParsing http://localhost:8000/api/v1/status).Content
    ```

## Tools

- GET `/api/v1/tools`
  - List available tools and schemas.
  - Example:
    ```powershell
    (iwr -UseBasicParsing http://localhost:8000/api/v1/tools).Content
    ```

- POST `/api/v1/tools/{tool_name}/execute`
  - Execute a tool with parameters.
  - Example (financial_ratio_calculator):
    ```powershell
    $json='{"parameters":{"ratio_type":"current_ratio","financial_data":{"current_assets":200000,"current_liabilities":100000}},"context":{}}'
    iwr -UseBasicParsing http://localhost:8000/api/v1/tools/financial_ratio_calculator/execute -Method Post -Body $json -ContentType 'application/json' | Select-Object -ExpandProperty Content
    ```
  - Sample Response:
    ```json
    {"success":true,"data":{"ratio":2.0,"current_assets":200000.0,"current_liabilities":100000.0,"interpretation":"Strong liquidity position","benchmark_range":{"min":1.0,"good":2.0,"max":3.0}},"error":null,"metadata":{"ratio_type":"current_ratio","calculation_method":"standard_financial_formula"}}
    ```

## Agents

- POST `/api/v1/agents/{agent_id}/invoke`
  - Invoke a specific agent, e.g. `ai_cfo_agent`.
  - Example:
    ```powershell
    $json='{"message":"Provide a brief financial health review for SMB X"}'
    iwr -UseBasicParsing http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke -Method Post -Body $json -ContentType 'application/json' | Select-Object -ExpandProperty Content
    ```
  - Current Status: returns error while routing (known issue under fix):
    ```json
    {"success":false,"error":"Routing failed: 'coroutine' object has no attribute 'get'"}
    ```

## Workflows

- POST `/api/v1/workflows/{workflow_type}/execute`
  - `workflow_type`: `advisory` | `transactional`
  - Example (advisory):
    ```powershell
    $json='{"message":"Advisory workflow for SMB X"}'
    iwr -UseBasicParsing http://localhost:8000/api/v1/workflows/advisory/execute -Method Post -Body $json -ContentType 'application/json' | Select-Object -ExpandProperty Content
    ```
  - Current Status: advisory returns 500 (known issue to be fixed next).

- GET `/api/v1/workflows/{workflow_type}/stream`
  - Server-Sent Events style streaming of workflow progress.
  - Example:
    ```powershell
    iwr -UseBasicParsing "http://localhost:8000/api/v1/workflows/advisory/stream?message=Run" | Select-Object -ExpandProperty Content
    ```

## Tracing

- GET `/api/v1/trace-test`
  - Emits a demo trace span.
  - Example:
    ```powershell
    (iwr -UseBasicParsing http://localhost:8000/api/v1/trace-test).Content
    ```

## Notes
- Auth: not required in dev mode (use reverse proxy/auth in prod).
- Content-Type: always `application/json` for POSTs.
- Known Issues (as of today):
  - Agent invocation routing error; fix in progress.
  - Advisory workflow 500; fix follows after agent routing.

