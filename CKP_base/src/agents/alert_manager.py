from datetime import datetime
from src.core.base_agent import BaseAgent
from src.core.state import AdvisoryState, AnalysisPhase

class AlertManagerAgent(BaseAgent):
	def __init__(self):
		super().__init__(name="alert_manager")

	async def process(self, state: AdvisoryState) -> AdvisoryState:
		# Simple rules on health/ratios
		alerts = []
		key = state.get("key_metrics", {})
		fh = state.get("financial_health")
		cr = float(key.get("current_ratio", 0.0))
		if fh and fh.overall_score < 50:
			alerts.append({
				"id": "low_overall_health",
				"severity": "P1",
				"message": f"Overall health low: {fh.overall_score:.1f}",
				"suggested_action": "Review OPEX and accelerate collections",
				"ts": datetime.utcnow().isoformat(),
			})
		if cr < 1.0:
			alerts.append({
				"id": "liquidity_risk",
				"severity": "P1",
				"message": f"Current ratio below 1.0: {cr:.2f}",
				"suggested_action": "Increase cash buffer / extend payables",
				"ts": datetime.utcnow().isoformat(),
			})

		state["alerts"] = alerts
		state.setdefault("confidence_scores", {})["alerts"] = 0.6
		state["current_phase"] = AnalysisPhase.ALERT_GENERATION
		return state
