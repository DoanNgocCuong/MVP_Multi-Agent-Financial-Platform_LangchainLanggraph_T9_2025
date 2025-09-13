"""Financial analysis and calculation tools."""

from typing import Any, Dict, List, Optional
from decimal import Decimal, ROUND_HALF_UP
import math

from ai_financial.mcp.tools.base_tool import BaseTool, ToolResult
from ai_financial.core.logging import get_logger, get_tracer

logger = get_logger(__name__)
tracer = get_tracer(__name__)


class FinancialRatioTool(BaseTool):
    """Tool for calculating financial ratios."""
    
    def __init__(self):
        super().__init__(
            name="financial_ratio_calculator",
            description="Calculate various financial ratios including liquidity, profitability, and leverage ratios",
            category="financial_analysis",
            version="1.0.0",
            required_permissions=["read_financial_data"],
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> ToolResult:
        """Execute financial ratio calculation."""
        with tracer.start_as_current_span("financial_ratio.execute"):
            try:
                if not self.validate_parameters(parameters):
                    return ToolResult(
                        success=False,
                        error="Invalid parameters"
                    )
                
                ratio_type = parameters.get("ratio_type")
                financial_data = parameters.get("financial_data", {})
                
                if ratio_type == "current_ratio":
                    result = self._calculate_current_ratio(financial_data)
                elif ratio_type == "quick_ratio":
                    result = self._calculate_quick_ratio(financial_data)
                elif ratio_type == "debt_to_equity":
                    result = self._calculate_debt_to_equity(financial_data)
                elif ratio_type == "return_on_equity":
                    result = self._calculate_roe(financial_data)
                elif ratio_type == "return_on_assets":
                    result = self._calculate_roa(financial_data)
                elif ratio_type == "gross_margin":
                    result = self._calculate_gross_margin(financial_data)
                elif ratio_type == "net_margin":
                    result = self._calculate_net_margin(financial_data)
                elif ratio_type == "asset_turnover":
                    result = self._calculate_asset_turnover(financial_data)
                else:
                    return ToolResult(
                        success=False,
                        error=f"Unknown ratio type: {ratio_type}"
                    )
                
                return ToolResult(
                    success=True,
                    data=result,
                    metadata={
                        "ratio_type": ratio_type,
                        "calculation_method": "standard_financial_formula"
                    }
                )
                
            except Exception as e:
                logger.error(
                    "Financial ratio calculation failed",
                    tool_name=self.name,
                    error=str(e),
                )
                
                return ToolResult(
                    success=False,
                    error=f"Calculation failed: {str(e)}"
                )
    
    def _calculate_current_ratio(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate current ratio."""
        current_assets = Decimal(str(data.get("current_assets", 0)))
        current_liabilities = Decimal(str(data.get("current_liabilities", 0)))
        
        if current_liabilities == 0:
            ratio = None
            interpretation = "Cannot calculate - no current liabilities"
        else:
            ratio = float(current_assets / current_liabilities)
            
            if ratio >= 2.0:
                interpretation = "Strong liquidity position"
            elif ratio >= 1.0:
                interpretation = "Adequate liquidity"
            else:
                interpretation = "Potential liquidity concerns"
        
        return {
            "ratio": ratio,
            "current_assets": float(current_assets),
            "current_liabilities": float(current_liabilities),
            "interpretation": interpretation,
            "benchmark_range": {"min": 1.0, "good": 2.0, "max": 3.0}
        }
    
    def _calculate_quick_ratio(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate quick ratio (acid test)."""
        current_assets = Decimal(str(data.get("current_assets", 0)))
        inventory = Decimal(str(data.get("inventory", 0)))
        current_liabilities = Decimal(str(data.get("current_liabilities", 0)))
        
        quick_assets = current_assets - inventory
        
        if current_liabilities == 0:
            ratio = None
            interpretation = "Cannot calculate - no current liabilities"
        else:
            ratio = float(quick_assets / current_liabilities)
            
            if ratio >= 1.0:
                interpretation = "Strong short-term liquidity"
            elif ratio >= 0.5:
                interpretation = "Adequate short-term liquidity"
            else:
                interpretation = "Potential short-term liquidity issues"
        
        return {
            "ratio": ratio,
            "quick_assets": float(quick_assets),
            "current_liabilities": float(current_liabilities),
            "interpretation": interpretation,
            "benchmark_range": {"min": 0.5, "good": 1.0, "max": 2.0}
        }
    
    def _calculate_debt_to_equity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate debt-to-equity ratio."""
        total_debt = Decimal(str(data.get("total_debt", 0)))
        total_equity = Decimal(str(data.get("total_equity", 0)))
        
        if total_equity == 0:
            ratio = None
            interpretation = "Cannot calculate - no equity"
        else:
            ratio = float(total_debt / total_equity)
            
            if ratio <= 0.3:
                interpretation = "Conservative debt level"
            elif ratio <= 0.6:
                interpretation = "Moderate debt level"
            elif ratio <= 1.0:
                interpretation = "High debt level"
            else:
                interpretation = "Very high debt level - potential risk"
        
        return {
            "ratio": ratio,
            "total_debt": float(total_debt),
            "total_equity": float(total_equity),
            "interpretation": interpretation,
            "benchmark_range": {"min": 0.0, "good": 0.5, "max": 1.0}
        }
    
    def _calculate_roe(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate return on equity."""
        net_income = Decimal(str(data.get("net_income", 0)))
        total_equity = Decimal(str(data.get("total_equity", 0)))
        
        if total_equity == 0:
            ratio = None
            interpretation = "Cannot calculate - no equity"
        else:
            ratio = float(net_income / total_equity)
            
            if ratio >= 0.15:
                interpretation = "Excellent return on equity"
            elif ratio >= 0.10:
                interpretation = "Good return on equity"
            elif ratio >= 0.05:
                interpretation = "Moderate return on equity"
            else:
                interpretation = "Low return on equity"
        
        return {
            "ratio": ratio,
            "net_income": float(net_income),
            "total_equity": float(total_equity),
            "interpretation": interpretation,
            "benchmark_range": {"min": 0.05, "good": 0.15, "max": 0.25}
        }
    
    def _calculate_roa(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate return on assets."""
        net_income = Decimal(str(data.get("net_income", 0)))
        total_assets = Decimal(str(data.get("total_assets", 0)))
        
        if total_assets == 0:
            ratio = None
            interpretation = "Cannot calculate - no assets"
        else:
            ratio = float(net_income / total_assets)
            
            if ratio >= 0.10:
                interpretation = "Excellent asset utilization"
            elif ratio >= 0.05:
                interpretation = "Good asset utilization"
            elif ratio >= 0.02:
                interpretation = "Moderate asset utilization"
            else:
                interpretation = "Poor asset utilization"
        
        return {
            "ratio": ratio,
            "net_income": float(net_income),
            "total_assets": float(total_assets),
            "interpretation": interpretation,
            "benchmark_range": {"min": 0.02, "good": 0.10, "max": 0.20}
        }
    
    def _calculate_gross_margin(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate gross profit margin."""
        revenue = Decimal(str(data.get("revenue", 0)))
        cost_of_goods_sold = Decimal(str(data.get("cost_of_goods_sold", 0)))
        
        if revenue == 0:
            ratio = None
            interpretation = "Cannot calculate - no revenue"
        else:
            gross_profit = revenue - cost_of_goods_sold
            ratio = float(gross_profit / revenue)
            
            if ratio >= 0.40:
                interpretation = "Excellent gross margin"
            elif ratio >= 0.25:
                interpretation = "Good gross margin"
            elif ratio >= 0.15:
                interpretation = "Moderate gross margin"
            else:
                interpretation = "Low gross margin"
        
        return {
            "ratio": ratio,
            "gross_profit": float(gross_profit) if revenue > 0 else 0,
            "revenue": float(revenue),
            "cost_of_goods_sold": float(cost_of_goods_sold),
            "interpretation": interpretation,
            "benchmark_range": {"min": 0.15, "good": 0.40, "max": 0.70}
        }
    
    def _calculate_net_margin(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate net profit margin."""
        net_income = Decimal(str(data.get("net_income", 0)))
        revenue = Decimal(str(data.get("revenue", 0)))
        
        if revenue == 0:
            ratio = None
            interpretation = "Cannot calculate - no revenue"
        else:
            ratio = float(net_income / revenue)
            
            if ratio >= 0.15:
                interpretation = "Excellent profitability"
            elif ratio >= 0.10:
                interpretation = "Good profitability"
            elif ratio >= 0.05:
                interpretation = "Moderate profitability"
            else:
                interpretation = "Low profitability"
        
        return {
            "ratio": ratio,
            "net_income": float(net_income),
            "revenue": float(revenue),
            "interpretation": interpretation,
            "benchmark_range": {"min": 0.05, "good": 0.15, "max": 0.30}
        }
    
    def _calculate_asset_turnover(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate asset turnover ratio."""
        revenue = Decimal(str(data.get("revenue", 0)))
        total_assets = Decimal(str(data.get("total_assets", 0)))
        
        if total_assets == 0:
            ratio = None
            interpretation = "Cannot calculate - no assets"
        else:
            ratio = float(revenue / total_assets)
            
            if ratio >= 2.0:
                interpretation = "Excellent asset efficiency"
            elif ratio >= 1.0:
                interpretation = "Good asset efficiency"
            elif ratio >= 0.5:
                interpretation = "Moderate asset efficiency"
            else:
                interpretation = "Poor asset efficiency"
        
        return {
            "ratio": ratio,
            "revenue": float(revenue),
            "total_assets": float(total_assets),
            "interpretation": interpretation,
            "benchmark_range": {"min": 0.5, "good": 2.0, "max": 4.0}
        }
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """Get parameters schema for financial ratio tool."""
        return {
            "type": "object",
            "properties": {
                "ratio_type": {
                    "type": "string",
                    "enum": [
                        "current_ratio",
                        "quick_ratio", 
                        "debt_to_equity",
                        "return_on_equity",
                        "return_on_assets",
                        "gross_margin",
                        "net_margin",
                        "asset_turnover"
                    ],
                    "description": "Type of financial ratio to calculate"
                },
                "financial_data": {
                    "type": "object",
                    "properties": {
                        "current_assets": {"type": "number"},
                        "current_liabilities": {"type": "number"},
                        "inventory": {"type": "number"},
                        "total_debt": {"type": "number"},
                        "total_equity": {"type": "number"},
                        "total_assets": {"type": "number"},
                        "net_income": {"type": "number"},
                        "revenue": {"type": "number"},
                        "cost_of_goods_sold": {"type": "number"}
                    },
                    "description": "Financial data for ratio calculation"
                }
            },
            "required": ["ratio_type", "financial_data"]
        }


class CashFlowAnalysisTool(BaseTool):
    """Tool for cash flow analysis."""
    
    def __init__(self):
        super().__init__(
            name="cash_flow_analyzer",
            description="Analyze cash flow patterns and trends",
            category="financial_analysis",
            version="1.0.0",
            required_permissions=["read_financial_data"],
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> ToolResult:
        """Execute cash flow analysis."""
        with tracer.start_as_current_span("cash_flow_analysis.execute"):
            try:
                if not self.validate_parameters(parameters):
                    return ToolResult(
                        success=False,
                        error="Invalid parameters"
                    )
                
                cash_flows = parameters.get("cash_flows", [])
                analysis_type = parameters.get("analysis_type", "comprehensive")
                
                if analysis_type == "trend":
                    result = self._analyze_trend(cash_flows)
                elif analysis_type == "seasonal":
                    result = self._analyze_seasonal_patterns(cash_flows)
                elif analysis_type == "volatility":
                    result = self._analyze_volatility(cash_flows)
                elif analysis_type == "comprehensive":
                    result = self._comprehensive_analysis(cash_flows)
                else:
                    return ToolResult(
                        success=False,
                        error=f"Unknown analysis type: {analysis_type}"
                    )
                
                return ToolResult(
                    success=True,
                    data=result,
                    metadata={
                        "analysis_type": analysis_type,
                        "periods_analyzed": len(cash_flows)
                    }
                )
                
            except Exception as e:
                logger.error(
                    "Cash flow analysis failed",
                    tool_name=self.name,
                    error=str(e),
                )
                
                return ToolResult(
                    success=False,
                    error=f"Analysis failed: {str(e)}"
                )
    
    def _analyze_trend(self, cash_flows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cash flow trends."""
        if len(cash_flows) < 2:
            return {"error": "Need at least 2 periods for trend analysis"}
        
        # Calculate period-over-period changes
        changes = []
        for i in range(1, len(cash_flows)):
            prev_flow = cash_flows[i-1].get("net_cash_flow", 0)
            curr_flow = cash_flows[i].get("net_cash_flow", 0)
            
            if prev_flow != 0:
                change_pct = ((curr_flow - prev_flow) / abs(prev_flow)) * 100
            else:
                change_pct = 0 if curr_flow == 0 else 100
            
            changes.append(change_pct)
        
        avg_change = sum(changes) / len(changes) if changes else 0
        
        if avg_change > 10:
            trend = "Strong Positive"
        elif avg_change > 0:
            trend = "Positive"
        elif avg_change > -10:
            trend = "Stable"
        else:
            trend = "Declining"
        
        return {
            "trend": trend,
            "average_change_percent": round(avg_change, 2),
            "period_changes": changes,
            "total_periods": len(cash_flows)
        }
    
    def _analyze_seasonal_patterns(self, cash_flows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze seasonal cash flow patterns."""
        if len(cash_flows) < 12:
            return {"warning": "Need at least 12 months for seasonal analysis"}
        
        # Group by month (assuming monthly data)
        monthly_flows = {}
        for i, flow in enumerate(cash_flows):
            month = (i % 12) + 1
            if month not in monthly_flows:
                monthly_flows[month] = []
            monthly_flows[month].append(flow.get("net_cash_flow", 0))
        
        # Calculate monthly averages
        monthly_averages = {}
        for month, flows in monthly_flows.items():
            monthly_averages[month] = sum(flows) / len(flows)
        
        # Find peak and trough months
        peak_month = max(monthly_averages, key=monthly_averages.get)
        trough_month = min(monthly_averages, key=monthly_averages.get)
        
        return {
            "monthly_averages": monthly_averages,
            "peak_month": peak_month,
            "trough_month": trough_month,
            "seasonal_variance": max(monthly_averages.values()) - min(monthly_averages.values())
        }
    
    def _analyze_volatility(self, cash_flows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cash flow volatility."""
        flows = [flow.get("net_cash_flow", 0) for flow in cash_flows]
        
        if len(flows) < 2:
            return {"error": "Need at least 2 periods for volatility analysis"}
        
        mean_flow = sum(flows) / len(flows)
        variance = sum((x - mean_flow) ** 2 for x in flows) / len(flows)
        std_dev = math.sqrt(variance)
        
        # Coefficient of variation
        cv = (std_dev / abs(mean_flow)) * 100 if mean_flow != 0 else 0
        
        if cv < 20:
            volatility_level = "Low"
        elif cv < 50:
            volatility_level = "Moderate"
        else:
            volatility_level = "High"
        
        return {
            "mean_cash_flow": round(mean_flow, 2),
            "standard_deviation": round(std_dev, 2),
            "coefficient_of_variation": round(cv, 2),
            "volatility_level": volatility_level,
            "min_flow": min(flows),
            "max_flow": max(flows)
        }
    
    def _comprehensive_analysis(self, cash_flows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform comprehensive cash flow analysis."""
        trend_analysis = self._analyze_trend(cash_flows)
        volatility_analysis = self._analyze_volatility(cash_flows)
        
        # Calculate additional metrics
        flows = [flow.get("net_cash_flow", 0) for flow in cash_flows]
        positive_periods = sum(1 for flow in flows if flow > 0)
        negative_periods = len(flows) - positive_periods
        
        return {
            "trend_analysis": trend_analysis,
            "volatility_analysis": volatility_analysis,
            "positive_periods": positive_periods,
            "negative_periods": negative_periods,
            "positive_period_ratio": positive_periods / len(flows) if flows else 0,
            "total_net_flow": sum(flows),
            "average_flow": sum(flows) / len(flows) if flows else 0
        }
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """Get parameters schema for cash flow analysis tool."""
        return {
            "type": "object",
            "properties": {
                "cash_flows": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "period": {"type": "string"},
                            "operating_cash_flow": {"type": "number"},
                            "investing_cash_flow": {"type": "number"},
                            "financing_cash_flow": {"type": "number"},
                            "net_cash_flow": {"type": "number"}
                        }
                    },
                    "description": "Array of cash flow data by period"
                },
                "analysis_type": {
                    "type": "string",
                    "enum": ["trend", "seasonal", "volatility", "comprehensive"],
                    "description": "Type of cash flow analysis to perform"
                }
            },
            "required": ["cash_flows"]
        }


class ProfitabilityAnalysisTool(BaseTool):
    """Tool for profitability analysis."""
    
    def __init__(self):
        super().__init__(
            name="profitability_analyzer",
            description="Analyze profitability metrics and trends",
            category="financial_analysis",
            version="1.0.0",
            required_permissions=["read_financial_data"],
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> ToolResult:
        """Execute profitability analysis."""
        with tracer.start_as_current_span("profitability_analysis.execute"):
            try:
                if not self.validate_parameters(parameters):
                    return ToolResult(
                        success=False,
                        error="Invalid parameters"
                    )
                
                financial_data = parameters.get("financial_data", {})
                analysis_type = parameters.get("analysis_type", "comprehensive")
                
                if analysis_type == "margins":
                    result = self._analyze_margins(financial_data)
                elif analysis_type == "returns":
                    result = self._analyze_returns(financial_data)
                elif analysis_type == "efficiency":
                    result = self._analyze_efficiency(financial_data)
                elif analysis_type == "comprehensive":
                    result = self._comprehensive_profitability_analysis(financial_data)
                else:
                    return ToolResult(
                        success=False,
                        error=f"Unknown analysis type: {analysis_type}"
                    )
                
                return ToolResult(
                    success=True,
                    data=result,
                    metadata={
                        "analysis_type": analysis_type,
                        "calculation_method": "standard_profitability_metrics"
                    }
                )
                
            except Exception as e:
                logger.error(
                    "Profitability analysis failed",
                    tool_name=self.name,
                    error=str(e),
                )
                
                return ToolResult(
                    success=False,
                    error=f"Analysis failed: {str(e)}"
                )
    
    def _analyze_margins(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze profit margins."""
        revenue = Decimal(str(data.get("revenue", 0)))
        cogs = Decimal(str(data.get("cost_of_goods_sold", 0)))
        operating_expenses = Decimal(str(data.get("operating_expenses", 0)))
        net_income = Decimal(str(data.get("net_income", 0)))
        
        if revenue == 0:
            return {"error": "Cannot analyze margins with zero revenue"}
        
        gross_profit = revenue - cogs
        operating_profit = gross_profit - operating_expenses
        
        margins = {
            "gross_margin": float(gross_profit / revenue),
            "operating_margin": float(operating_profit / revenue),
            "net_margin": float(net_income / revenue),
            "gross_profit": float(gross_profit),
            "operating_profit": float(operating_profit),
            "revenue": float(revenue)
        }
        
        # Add interpretations
        margins["interpretations"] = {
            "gross_margin": self._interpret_margin(margins["gross_margin"], "gross"),
            "operating_margin": self._interpret_margin(margins["operating_margin"], "operating"),
            "net_margin": self._interpret_margin(margins["net_margin"], "net")
        }
        
        return margins
    
    def _analyze_returns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze return metrics."""
        net_income = Decimal(str(data.get("net_income", 0)))
        total_assets = Decimal(str(data.get("total_assets", 0)))
        total_equity = Decimal(str(data.get("total_equity", 0)))
        invested_capital = Decimal(str(data.get("invested_capital", total_assets)))
        
        returns = {}
        
        if total_assets > 0:
            returns["return_on_assets"] = float(net_income / total_assets)
        
        if total_equity > 0:
            returns["return_on_equity"] = float(net_income / total_equity)
        
        if invested_capital > 0:
            returns["return_on_invested_capital"] = float(net_income / invested_capital)
        
        # Add interpretations
        returns["interpretations"] = {}
        for metric, value in returns.items():
            if metric != "interpretations":
                returns["interpretations"][metric] = self._interpret_return(value, metric)
        
        return returns
    
    def _analyze_efficiency(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze operational efficiency."""
        revenue = Decimal(str(data.get("revenue", 0)))
        total_assets = Decimal(str(data.get("total_assets", 0)))
        inventory = Decimal(str(data.get("inventory", 0)))
        accounts_receivable = Decimal(str(data.get("accounts_receivable", 0)))
        
        efficiency = {}
        
        if total_assets > 0:
            efficiency["asset_turnover"] = float(revenue / total_assets)
        
        if inventory > 0:
            efficiency["inventory_turnover"] = float(revenue / inventory)
        
        if accounts_receivable > 0:
            efficiency["receivables_turnover"] = float(revenue / accounts_receivable)
            efficiency["days_sales_outstanding"] = 365 / efficiency["receivables_turnover"]
        
        return efficiency
    
    def _comprehensive_profitability_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive profitability analysis."""
        margins = self._analyze_margins(data)
        returns = self._analyze_returns(data)
        efficiency = self._analyze_efficiency(data)
        
        # Overall profitability score
        score_components = []
        
        if "gross_margin" in margins and margins["gross_margin"] is not None:
            score_components.append(min(margins["gross_margin"] * 100, 100))
        
        if "return_on_assets" in returns:
            score_components.append(min(returns["return_on_assets"] * 500, 100))
        
        if "asset_turnover" in efficiency:
            score_components.append(min(efficiency["asset_turnover"] * 50, 100))
        
        overall_score = sum(score_components) / len(score_components) if score_components else 0
        
        return {
            "margins_analysis": margins,
            "returns_analysis": returns,
            "efficiency_analysis": efficiency,
            "overall_profitability_score": round(overall_score, 2),
            "score_interpretation": self._interpret_overall_score(overall_score)
        }
    
    def _interpret_margin(self, margin: float, margin_type: str) -> str:
        """Interpret margin values."""
        if margin_type == "gross":
            if margin >= 0.5:
                return "Excellent gross margin"
            elif margin >= 0.3:
                return "Good gross margin"
            elif margin >= 0.15:
                return "Moderate gross margin"
            else:
                return "Low gross margin"
        elif margin_type == "operating":
            if margin >= 0.2:
                return "Excellent operating efficiency"
            elif margin >= 0.1:
                return "Good operating efficiency"
            elif margin >= 0.05:
                return "Moderate operating efficiency"
            else:
                return "Poor operating efficiency"
        elif margin_type == "net":
            if margin >= 0.15:
                return "Excellent profitability"
            elif margin >= 0.1:
                return "Good profitability"
            elif margin >= 0.05:
                return "Moderate profitability"
            else:
                return "Low profitability"
        
        return "Unknown margin type"
    
    def _interpret_return(self, return_value: float, return_type: str) -> str:
        """Interpret return values."""
        if return_value >= 0.15:
            return "Excellent returns"
        elif return_value >= 0.1:
            return "Good returns"
        elif return_value >= 0.05:
            return "Moderate returns"
        else:
            return "Low returns"
    
    def _interpret_overall_score(self, score: float) -> str:
        """Interpret overall profitability score."""
        if score >= 80:
            return "Excellent overall profitability"
        elif score >= 60:
            return "Good overall profitability"
        elif score >= 40:
            return "Moderate overall profitability"
        else:
            return "Poor overall profitability"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """Get parameters schema for profitability analysis tool."""
        return {
            "type": "object",
            "properties": {
                "financial_data": {
                    "type": "object",
                    "properties": {
                        "revenue": {"type": "number"},
                        "cost_of_goods_sold": {"type": "number"},
                        "operating_expenses": {"type": "number"},
                        "net_income": {"type": "number"},
                        "total_assets": {"type": "number"},
                        "total_equity": {"type": "number"},
                        "invested_capital": {"type": "number"},
                        "inventory": {"type": "number"},
                        "accounts_receivable": {"type": "number"}
                    },
                    "description": "Financial data for profitability analysis"
                },
                "analysis_type": {
                    "type": "string",
                    "enum": ["margins", "returns", "efficiency", "comprehensive"],
                    "description": "Type of profitability analysis to perform"
                }
            },
            "required": ["financial_data"]
        }