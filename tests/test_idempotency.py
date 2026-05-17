from core.event_bus import EventBus
from core.event_envelope import EventEnvelope
from core.events import SpeedViolationEvent
from core.subscribers import AlertService


def test_duplicate_speed_violation_blocked():
    # This proves duplicate deliveries are ignored, which prevents retries or
    # network glitches from applying the same speed-violation penalty twice.
    fixed_event_id = "test-uuid-1234"
    speed_event = SpeedViolationEvent(
        vehicle_id="V001",
        plate_number="ABC-123",
        measured_speed=95.0,
        speed_limit=60.0,
        camera_id="CAM_01",
    )
    envelope = EventEnvelope(
        correlation_id="test-correlation-001",
        source_id="CAM_01",
        payload=speed_event,
    )
    envelope.event_id = fixed_event_id

    event_bus = EventBus()
    alert_service = AlertService()
    event_bus.subscribe(alert_service)

    event_bus.publish(envelope)
    event_bus.publish(envelope)

    assert alert_service.penalty_count == 1
