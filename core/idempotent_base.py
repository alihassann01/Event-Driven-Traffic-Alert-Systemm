from abc import ABC, abstractmethod


class IdempotentReceiver(ABC):
    """
    Base class for the Idempotent Receiver Pattern.

    It prevents the same event from being processed more than once by tracking
    event IDs that have already been handled. This matters in event-driven systems
    because network glitches or retries can cause duplicate deliveries.
    """

    def __init__(self):
        self.seen_ids = set()

    def on_event(self, envelope):
        if envelope.event_id in self.seen_ids:
            print(f"Duplicate event detected: {envelope.event_id}")
            return

        self.seen_ids.add(envelope.event_id)
        self.process_event(envelope)

    @abstractmethod
    def process_event(self, envelope):
        pass
