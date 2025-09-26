import os, contextlib, uuid
from arize_phoenix import Client
PHOENIX_ENDPOINT = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006/v1/traces")
PHOENIX_PROJECT = os.getenv("PHOENIX_PROJECT_NAME", "nestwell_demo")
_client = Client(endpoint=PHOENIX_ENDPOINT, project_name=PHOENIX_PROJECT)

@contextlib.contextmanager
def traced(name: str, attributes: dict | None = None):
    trace_id = str(uuid.uuid4())
    span = _client.span(name=name, attributes=attributes or {}, trace_id=trace_id)
    try:
        yield span
    finally:
        span.end()

def child_span(parent_span, name: str, attributes: dict | None = None):
    span = _client.span(name=name, attributes=attributes or {}, trace_id=parent_span.trace_id, parent_id=parent_span.span_id)
    return span
