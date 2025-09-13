from typing import Dict, AsyncGenerator, Literal
from datetime import datetime
from src.core.state import AdvisoryState, AnalysisPhase
from src.core.base_agent import BaseAgent

class AdvisoryOrchestrator:
	def __init__(self, agents: Dict[str, BaseAgent]):
		self.agents = agents

	async def _route_request(self, state: AdvisoryState) -> AdvisoryState:
		state["current_phase"] = AnalysisPhase.DATA_COLLECTION
		state.setdefault("messages", []).append({
			"ts": datetime.utcnow().isoformat(),
			"agent": "router",
			"msg": f"request_type={state.get('request_type')}"
		})
		state.setdefault("raw_data", {})
		state.setdefault("key_metrics", {})
		state.setdefault("confidence_scores", {})
		state.setdefault("errors", [])
		return state

	def _determine_flow(self, state: AdvisoryState) -> Literal["full_analysis", "quick_check", "forecast", "what_if"]:
		return state.get("request_type", "quick_check")

	async def _run_pipeline(self, state: AdvisoryState, emit=None) -> AdvisoryState:
		# router
		state = await self._route_request(state)
		if emit:
			await emit({"event": "router", "data": {"phase": str(state["current_phase"])}})

		flow = self._determine_flow(state)
		if flow in ("full_analysis",):
			# data_collector -> analyzer -> forecaster -> alert_manager -> advisor -> explainer -> supervisor
			state = await self.agents["data_collector"].execute(state)
			if emit:
				await emit({"event": "data_collection", "data": {"phase": str(state["current_phase"])}})
			state = await self.agents["analyzer"].execute(state)
			if emit:
				await emit({"event": "analysis", "data": {"phase": str(state["current_phase"],)}})
			state = await self.agents["forecaster"].execute(state)
			if emit:
				await emit({"event": "forecasting", "data": {"phase": str(state["current_phase"])}})
			state = await self.agents["alert_manager"].execute(state)
			state = await self.agents["advisor"].execute(state)
			state = await self.agents["explainer"].execute(state)
			state = await self.agents["supervisor"].execute(state)
			if emit:
				await emit({"event": "complete", "data": {"phase": str(state["current_phase"])}})
			return state
		elif flow in ("quick_check",):
			# analyzer -> forecaster -> alert_manager -> advisor -> explainer -> supervisor
			state = await self.agents["analyzer"].execute(state)
			if emit:
				await emit({"event": "analysis", "data": {"phase": str(state["current_phase"])}})
			state = await self.agents["forecaster"].execute(state)
			if emit:
				await emit({"event": "forecasting", "data": {"phase": str(state["current_phase"])}})
			state = await self.agents["alert_manager"].execute(state)
			state = await self.agents["advisor"].execute(state)
			state = await self.agents["explainer"].execute(state)
			state = await self.agents["supervisor"].execute(state)
			if emit:
				await emit({"event": "complete", "data": {"phase": str(state["current_phase"])}})
			return state
		else:
			# forecast / what_if minimal: forecaster -> explainer -> supervisor
			state = await self.agents["forecaster"].execute(state)
			if emit:
				await emit({"event": "forecasting", "data": {"phase": str(state["current_phase"])}})
			state = await self.agents["explainer"].execute(state)
			state = await self.agents["supervisor"].execute(state)
			if emit:
				await emit({"event": "complete", "data": {"phase": str(state["current_phase"])}})
			return state

	async def astream_events(self, initial_state: AdvisoryState) -> AsyncGenerator[Dict, None]:
		queue = []
		async def emit(evt):
			queue.append(evt)
		await self._run_pipeline(initial_state, emit=emit)
		for evt in queue:
			yield evt

	async def ainvoke(self, initial_state: AdvisoryState) -> AdvisoryState:
		return await self._run_pipeline(initial_state)
