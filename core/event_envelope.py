import uuid
from datetime import datetime


class EventEnvelope:
    """Wraps an event payload with metadata for publishing and tracking."""

    def __init__(self, correlation_id: str, source_id: str, payload: object, schema_version: int = 1):
        self.event_id: str = str(uuid.uuid4())
        self.correlation_id: str = correlation_id
        self.schema_version: int = schema_version
        self.source_id: str = source_id
        self.timestamp: str = datetime.now().isoformat()
        self.event_type: str = type(payload).__name__
        self.payload: object = payload
