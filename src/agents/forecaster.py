from datetime import datetime, timedelta
from src.core.base_agent import BaseAgent
from src.core.state import AdvisoryState, AnalysisPhase

class ForecasterAgent(BaseAgent):
	def __init__(self):
		super().__init__(name="forecaster")

	async def process(self, state: AdvisoryState) -> AdvisoryState:
		state["current_phase"] = AnalysisPhase.FORECASTING
		key = state.get("key_metrics", {})
		revenue = float(key.get("revenue", 0.0))
		net_income = float(key.get("net_income", 0.0))

		# Very simple cash projection: assume cash changes proportional to net_income
		base_cash = float(state.get("raw_data", {}).get("bank", {}).get("cash", 0.0))
		weeks = []
		cash = base_cash
		for i in range(13):
			date = datetime.utcnow().date() + timedelta(weeks=i+1)
			cash += max(net_income, 0.0) / 13.0
			weeks.append({"week": i+1, "date": str(date), "cash": cash})

		state["cash_flow_forecast"] = {"horizon_weeks": 13, "series": weeks}

		# Simple P&L 12 months: linear growth 1%/month as placeholder
		months = []
		monthly_rev = revenue / 12.0
		for m in range(12):
			date = datetime.utcnow().date().replace(day=1)
			value = monthly_rev * (1 + 0.01 * m)
			months.append({"month": m+1, "date": str(date), "revenue": value})
		state["pnl_forecast"] = {"horizon_months": 12, "series": months}

		state.setdefault("confidence_scores", {})["forecast"] = 0.5
		return state
