from src.core.base_agent import BaseAgent
from src.core.state import AdvisoryState, AnalysisPhase

class SupervisorAgent(BaseAgent):
	def __init__(self):
		super().__init__(name="supervisor")

	async def process(self, state: AdvisoryState) -> AdvisoryState:
		conf = state.get("confidence_scores", {})
		overall = (
			conf.get("analysis", 0.0) * 0.4
			+ conf.get("forecast", 0.0) * 0.25
			+ conf.get("alerts", 0.0) * 0.2
			+ conf.get("explanations", 0.0) * 0.15
		)
		state.setdefault("confidence_scores", {})["overall"] = overall
		state["current_phase"] = AnalysisPhase.COMPLETE
		return state
