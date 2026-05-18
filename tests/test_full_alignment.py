from core.event_bus import EventBus
from core.event_envelope import EventEnvelope
from core.events import (
    CongestionAlertEvent,
    SpeedViolationEvent,
    VehicleDetectedEvent,
)
from core.subscribers import DashboardService, ReportingService


class CaptureSubscriber:
    def __init__(self):
        self.received = []

    def on_event(self, envelope):
        self.received.append(envelope)


def test_vehicle_detected_lane_number_is_backward_compatible():
    event = VehicleDetectedEvent(
        vehicle_id="V001",
        plate_number="ABC-123",
        camera_id="CAM_01",
    )

    assert event.lane_number is None


def test_dashboard_and_reporting_ignore_duplicate_event_ids():
    vehicle_event = VehicleDetectedEvent(
        vehicle_id="V001",
        plate_number="ABC-123",
        camera_id="CAM_01",
    )
    envelope = EventEnvelope(
        correlation_id="journey-001",
        source_id="CAM_01",
        payload=vehicle_event,
    )
    envelope.event_id = "duplicate-event-id"

    dashboard = DashboardService()
    reporting = ReportingService()
    event_bus = EventBus()
    event_bus.subscribe(dashboard)
    event_bus.subscribe(reporting)

    event_bus.publish(envelope)
    event_bus.publish(envelope)

    assert len(dashboard.updates) == 1
    assert len(reporting.report_data) == 1


def test_bounded_queue_evicts_least_important_event():
    subscriber = CaptureSubscriber()
    event_bus = EventBus(max_queue_size=2, auto_flush=False)
    event_bus.subscribe(subscriber)

    vehicle_envelope = EventEnvelope(
        correlation_id="journey-001",
        source_id="CAM_01",
        payload=VehicleDetectedEvent("V001", "ABC-123", "CAM_01"),
    )
    speed_envelope = EventEnvelope(
        correlation_id="journey-002",
        source_id="CAM_02",
        payload=SpeedViolationEvent("V002", "XYZ-999", 95.0, 60.0, "CAM_02"),
    )
    congestion_envelope = EventEnvelope(
        correlation_id="journey-003",
        source_id="CAM_03",
        payload=CongestionAlertEvent("INT_05", 120, "CRITICAL", "CAM_03"),
    )

    event_bus.publish(vehicle_envelope)
    event_bus.publish(speed_envelope)
    event_bus.publish(congestion_envelope)

    assert event_bus.pending_count(subscriber) == 2

    event_bus.flush(subscriber)

    received_types = [envelope.event_type for envelope in subscriber.received]
    assert received_types == ["SpeedViolationEvent", "CongestionAlertEvent"]
