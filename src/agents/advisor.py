from datetime import datetime
from src.core.base_agent import BaseAgent
from src.core.state import AdvisoryState, AnalysisPhase

class AdvisorAgent(BaseAgent):
	def __init__(self):
		super().__init__(name="advisor")

	async def process(self, state: AdvisoryState) -> AdvisoryState:
		recos = []
		alerts = state.get("alerts", [])
		for a in alerts:
			if a.get("id") == "liquidity_risk":
				recos.append({
					"title": "Improve liquidity",
					"action": "Negotiate longer payment terms; offer early-payment discount to customers",
					"expected_impact": "+0.2-0.4 to current ratio",
					"ts": datetime.utcnow().isoformat(),
				})
			if a.get("id") == "low_overall_health":
				recos.append({
					"title": "Reduce OPEX 5%",
					"action": "Cut discretionary spend and renegotiate key vendor contracts",
					"expected_impact": "+2-4 pts to health",
					"ts": datetime.utcnow().isoformat(),
				})
		state["recommendations"] = recos
		state.setdefault("confidence_scores", {})["advisory"] = 0.55
		state["current_phase"] = AnalysisPhase.ADVISORY
		return state
