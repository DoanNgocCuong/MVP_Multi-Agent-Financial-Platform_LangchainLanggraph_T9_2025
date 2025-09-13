from __future__ import annotations
from typing import TypedDict, List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class AnalysisPhase(str, Enum):
	DATA_COLLECTION = "data_collection"
	ANALYSIS = "analysis"
	FORECASTING = "forecasting"
	ALERT_GENERATION = "alert_generation"
	ADVISORY = "advisory"
	EXPLANATION = "explanation"
	COMPLETE = "complete"

class FinancialHealth(BaseModel):
	cash_flow_health: float  # 0-100
	profitability_health: float
	liquidity_health: float
	debt_health: float
	overall_score: float
	timestamp: datetime

class AdvisoryState(TypedDict, total=False):
	request_id: str
	user_id: str
	company_id: str
	request_type: str  # "full_analysis", "quick_check", "forecast", "what_if"
	current_phase: AnalysisPhase
	messages: List[Dict[str, Any]]
	raw_data: Dict[str, Any]
	data_sources: List[str]
	last_sync_timestamp: Optional[datetime]
	financial_health: FinancialHealth | None
	key_metrics: Dict[str, Any]
	trends: Dict[str, Any]
	cash_flow_forecast: Optional[Dict[str, Any]]
	pnl_forecast: Optional[Dict[str, Any]]
	scenarios: List[Dict[str, Any]]
	alerts: List[Dict[str, Any]]
	recommendations: List[Dict[str, Any]]
	action_items: List[Dict[str, Any]]
	explanations: Dict[str, str]
	citations: List[Dict[str, str]]
	confidence_scores: Dict[str, float]
	processing_time: float
	token_usage: Dict[str, int]
	errors: List[str]
