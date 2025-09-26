import os, contextlib, uuid

# Mock implementation for Phoenix tracing when the library is not available
class MockSpan:
    def __init__(self, name, attributes=None, trace_id=None):
        self.name = name
        self.attributes = attributes or {}
        self.trace_id = trace_id or str(uuid.uuid4())
        self.span_id = str(uuid.uuid4())

    def end(self):
        pass

class MockClient:
    def span(self, name, attributes=None, trace_id=None, parent_id=None):
        return MockSpan(name, attributes, trace_id)

_client = MockClient()

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