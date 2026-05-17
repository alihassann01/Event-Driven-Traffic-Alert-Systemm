from abc import ABC, abstractmethod

from core.events import SpeedViolationEvent
from core.idempotent_base import IdempotentReceiver


class IEventSubscriber(ABC):
    """Interface for services that receive event envelopes from the EventBus."""

    @abstractmethod
    def on_event(self, envelope):
        pass


class AlertService(IdempotentReceiver, IEventSubscriber):
    """Applies penalties for speed violation events."""

    def __init__(self):
        super().__init__()
        self.penalty_count = 0

    def process_event(self, envelope):
        if isinstance(envelope.payload, SpeedViolationEvent):
            self.penalty_count += 1
