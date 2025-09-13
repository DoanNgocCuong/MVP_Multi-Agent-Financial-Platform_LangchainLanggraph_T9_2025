from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time
import structlog
from opentelemetry import trace
from src.core.state import AdvisoryState

tracer = trace.get_tracer(__name__)
logger = structlog.get_logger()

class BaseAgent(ABC):
	def __init__(self, name: str):
		self.name = name

	@abstractmethod
	async def process(self, state: AdvisoryState) -> AdvisoryState:
		raise NotImplementedError

	@tracer.start_as_current_span("agent.execute")
	async def execute(self, state: AdvisoryState) -> AdvisoryState:
		span = trace.get_current_span()
		span.set_attribute("agent.name", self.name)
		start = time.perf_counter()
		logger.info("agent_start", agent=self.name)
		try:
			new_state = await self.process(state)
			return new_state
		except Exception as e:
			logger.error("agent_error", agent=self.name, error=str(e))
			state.setdefault("errors", []).append(f"{self.name}: {e}")
			span.record_exception(e)
			raise
		finally:
			elapsed = time.perf_counter() - start
			logger.info("agent_end", agent=self.name, elapsed=elapsed)
			span.set_attribute("agent.elapsed", elapsed)
