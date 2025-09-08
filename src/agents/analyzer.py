from datetime import datetime
from math import isfinite
from src.core.base_agent import BaseAgent
from src.core.state import AdvisoryState, AnalysisPhase, FinancialHealth

class FinancialAnalyzerAgent(BaseAgent):
	def __init__(self):
		super().__init__(name="analyzer")

	async def process(self, state: AdvisoryState) -> AdvisoryState:
		state["current_phase"] = AnalysisPhase.ANALYSIS
		raw = state.get("raw_data", {})
		erp = raw.get("erp", {})
		acc = raw.get("accounting", {})
		bank = raw.get("bank", {})

		revenue = float(erp.get("revenue", 0.0))
		cogs = float(erp.get("cogs", 0.0))
		opex = float(acc.get("opex", 0.0))
		interest = float(acc.get("interest", 0.0))
		cash = float(bank.get("cash", 0.0))
		current_assets = float(bank.get("current_assets", 0.0))
		current_liabilities = float(bank.get("current_liabilities", 0.0))
		short_term_debt = float(bank.get("short_term_debt", 0.0))

		gross_profit = revenue - cogs
		ebit = gross_profit - opex
		net_income = ebit - interest
		current_ratio = (current_assets / current_liabilities) if current_liabilities else 0.0

		profitability_health = _clip_scale(net_income / revenue * 100 if revenue else 0, -50, 50)
		liquidity_health = _clip_scale((current_ratio - 1.0) * 50, 0, 100)
		cash_flow_health = _clip_scale((cash / max(revenue/12, 1)) * 20, 0, 100)
		debt_health = _clip_scale((1 - min(short_term_debt / max(current_assets, 1), 1)) * 100, 0, 100)
		overall = (profitability_health * 0.35 + liquidity_health * 0.25 + cash_flow_health * 0.25 + debt_health * 0.15)

		state["key_metrics"] = {
			"revenue": revenue,
			"cogs": cogs,
			"gross_profit": gross_profit,
			"opex": opex,
			"ebit": ebit,
			"interest": interest,
			"net_income": net_income,
			"current_ratio": current_ratio,
		}

		state["financial_health"] = FinancialHealth(
			cash_flow_health=cash_flow_health,
			profitability_health=profitability_health,
			liquidity_health=liquidity_health,
			debt_health=debt_health,
			overall_score=overall,
			timestamp=datetime.utcnow(),
		)

		state.setdefault("confidence_scores", {})["analysis"] = 0.6
		state.setdefault("messages", []).append({
			"ts": datetime.utcnow().isoformat(),
			"agent": "analyzer",
			"msg": f"Health={overall:.1f} | CR={current_ratio:.2f}"
		})
		return state


def _clip_scale(value: float, lo: float, hi: float) -> float:
	if not isfinite(value):
		return 0.0
	if value <= lo:
		return 0.0
	if value >= hi:
		return 100.0
	return (value - lo) / (hi - lo) * 100.0
