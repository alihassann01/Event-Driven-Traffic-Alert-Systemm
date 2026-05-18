from core.event_bus import EventBus
from core.event_envelope import EventEnvelope
from core.events import EmergencyVehicleEvent


class CaptureSubscriber:
    def __init__(self):
        self.received = []

    def on_event(self, envelope):
        self.received.append(envelope)


def test_fifth_event_type_requires_no_event_bus_change():
    # This proves the EventBus is decoupled: a new event type can be wrapped in
    # an envelope and delivered through the same publish/subscribe mechanism.
    emergency_event = EmergencyVehicleEvent(
        vehicle_id="EV001",
        plate_number="EMG-911",
        vehicle_type="Ambulance",
        priority_level="CRITICAL",
        camera_id="CAM_04",
    )
    envelope = EventEnvelope(
        correlation_id="EMERGENCY_001",
        source_id="CAM_04",
        payload=emergency_event,
    )

    event_bus = EventBus()
    subscriber = CaptureSubscriber()
    event_bus.subscribe(subscriber)

    event_bus.publish(envelope)

    assert len(subscriber.received) == 1
    assert subscriber.received[0].event_type == "EmergencyVehicleEvent"
    assert subscriber.received[0].payload is emergency_event
