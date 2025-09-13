from datetime import datetime
from src.core.base_agent import BaseAgent
from src.core.state import AdvisoryState, AnalysisPhase

class ExplainerAgent(BaseAgent):
	def __init__(self):
		super().__init__(name="explainer")

	async def process(self, state: AdvisoryState) -> AdvisoryState:
		fh = state.get("financial_health")
		explanations = {}
		if fh:
			explanations["overall"] = f"Overall financial health is {fh.overall_score:.1f}. Key drivers: profitability {fh.profitability_health:.1f}, liquidity {fh.liquidity_health:.1f}."
		citations = [{"source": "snapshot:mock_bank", "note": "cash/current_ratio"}]
		state["explanations"] = explanations
		state["citations"] = citations
		state.setdefault("confidence_scores", {})["explanations"] = 0.6
		state["current_phase"] = AnalysisPhase.EXPLANATION
		return state
