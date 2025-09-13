from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import uuid

from src.core.orchestrator import AdvisoryOrchestrator
from src.core.state import AdvisoryState, AnalysisPhase
from src.agents.data_collector import DataCollectorAgent
from src.agents.analyzer import FinancialAnalyzerAgent
from src.agents.forecaster import ForecasterAgent
from src.agents.alert_manager import AlertManagerAgent
from src.agents.advisor import AdvisorAgent
from src.agents.explainer import ExplainerAgent
from src.agents.supervisor import SupervisorAgent

app = FastAPI(title="AI CFO Advisory API")

_agents = {
	"data_collector": DataCollectorAgent(),
	"analyzer": FinancialAnalyzerAgent(),
	"forecaster": ForecasterAgent(),
	"alert_manager": AlertManagerAgent(),
	"advisor": AdvisorAgent(),
	"explainer": ExplainerAgent(),
	"supervisor": SupervisorAgent(),
}
_orchestrator = AdvisoryOrchestrator(_agents)

class AdvisoryRequest(BaseModel):
	company_id: str
	user_id: str
	request_type: str
	parameters: Optional[Dict[str, Any]] = None
	streaming: bool = False

@app.post("/api/v1/advisory/analyze")
async def analyze(req: AdvisoryRequest):
	initial_state: AdvisoryState = {
		"request_id": str(uuid.uuid4()),
		"user_id": req.user_id,
		"company_id": req.company_id,
		"request_type": req.request_type,
		"current_phase": AnalysisPhase.DATA_COLLECTION,
		"messages": [],
		"raw_data": {},
		"key_metrics": {},
		"confidence_scores": {},
		"errors": [],
	}
	if req.parameters:
		initial_state.setdefault("parameters", {}).update(req.parameters)

	if req.streaming:
		async def event_source():
			async for event in _orchestrator.astream_events(initial_state):
				payload = {"event": event.get("event"), "data": event.get("data")}
				yield f"data: {json.dumps(payload, default=str)}\n\n"
		return StreamingResponse(event_source(), media_type="text/event-stream")

	final_state = await _orchestrator.ainvoke(initial_state)
	return final_state
