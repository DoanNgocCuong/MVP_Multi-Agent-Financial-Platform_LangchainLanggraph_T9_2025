import asyncio
from datetime import datetime
from src.core.base_agent import BaseAgent
from src.core.state import AdvisoryState, AnalysisPhase

class DataCollectorAgent(BaseAgent):
	def __init__(self):
		super().__init__(name="data_collector")

	async def process(self, state: AdvisoryState) -> AdvisoryState:
		state["current_phase"] = AnalysisPhase.DATA_COLLECTION

		async def _mock_erp():
			await asyncio.sleep(0.2)
			return {"revenue": 120000, "cogs": 72000}

		async def _mock_accounting():
			await asyncio.sleep(0.2)
			return {"opex": 30000, "interest": 2000}

		async def _mock_bank():
			await asyncio.sleep(0.2)
			return {"cash": 40000, "short_term_debt": 15000, "current_assets": 65000, "current_liabilities": 42000}

		erp, acc, bank = await asyncio.gather(_mock_erp(), _mock_accounting(), _mock_bank())

		state["raw_data"] = {"erp": erp, "accounting": acc, "bank": bank}
		state["data_sources"] = ["mock_erp", "mock_accounting", "mock_bank"]
		state["last_sync_timestamp"] = datetime.utcnow()
		state.setdefault("messages", []).append({
			"ts": datetime.utcnow().isoformat(),
			"agent": "data_collector",
			"msg": "Thu thập dữ liệu mock xong"
		})
		return state
