"""Logging configuration with OpenTelemetry integration."""

import logging
import sys
from typing import Any, Dict

import structlog
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

try:
    from opentelemetry.instrumentation.logging import LoggingInstrumentor
    LOGGING_INSTRUMENTATION_AVAILABLE = True
except ImportError:
    LOGGING_INSTRUMENTATION_AVAILABLE = False

from ai_financial.core.config import settings


def setup_logging() -> None:
    """Set up structured logging with OpenTelemetry integration."""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.JSONRenderer() if settings.monitoring.log_format == "json" 
            else structlog.dev.ConsoleRenderer(colors=True),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.monitoring.log_level.upper())
        ),
        logger_factory=structlog.WriteLoggerFactory(sys.stdout),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard logging
    logging.basicConfig(
        level=getattr(logging, settings.monitoring.log_level.upper()),
        format="%(message)s",
        stream=sys.stdout,
    )
    
    # Suppress noisy loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


def setup_tracing() -> None:
    """Set up OpenTelemetry tracing."""
    
    # Check if tracer provider is already set to avoid override
    if trace.get_tracer_provider() is not None and hasattr(trace.get_tracer_provider(), '_resource'):
        return
    
    # Create resource
    resource = Resource.create({
        "service.name": settings.monitoring.otel_service_name,
        "service.version": "0.1.0",
        "deployment.environment": settings.environment,
    })
    
    # Set up tracer provider
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)
    
    # Set up OTLP exporter
    if settings.monitoring.otel_exporter_otlp_endpoint:
        otlp_exporter = OTLPSpanExporter(
            endpoint=settings.monitoring.otel_exporter_otlp_endpoint,
            headers=_parse_otlp_headers(settings.monitoring.otel_exporter_otlp_headers),
        )
        
        # Add span processor
        span_processor = BatchSpanProcessor(otlp_exporter)
        tracer_provider.add_span_processor(span_processor)
    
    # Instrument logging if available
    if LOGGING_INSTRUMENTATION_AVAILABLE:
        LoggingInstrumentor().instrument(set_logging_format=True)
    else:
        # Log a warning if logging instrumentation is not available
        logger = get_logger(__name__)
        logger.warning("OpenTelemetry logging instrumentation not available. Install opentelemetry-instrumentation-logging for full logging integration.")


def _parse_otlp_headers(headers_str: str) -> Dict[str, str]:
    """Parse OTLP headers from string format."""
    if not headers_str:
        return {}
    
    headers = {}
    for header in headers_str.split(","):
        if "=" in header:
            key, value = header.strip().split("=", 1)
            headers[key] = value
    
    return headers


def get_logger(name: str) -> Any:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


def get_tracer(name: str) -> trace.Tracer:
    """Get an OpenTelemetry tracer instance."""
    return trace.get_tracer(name)


# Initialize logging and tracing
setup_logging()
setup_tracing()

# Export commonly used instances
logger = get_logger(__name__)
tracer = get_tracer(__name__)