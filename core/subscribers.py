from abc import ABC, abstractmethod

from core.idempotent_base import IdempotentReceiver
from core.events import (
    VehicleDetectedEvent,
    SpeedViolationEvent,
    CongestionAlertEvent,
    TrafficClearedEvent,
)


class IEventSubscriber(ABC):
    """Interface for services that receive event envelopes from the EventBus.

    Every subscriber must implement the on_event method so the EventBus
    can deliver envelopes in a uniform way regardless of the concrete
    service behind the subscription.
    """

    @abstractmethod
    def on_event(self, envelope):
        pass


class AlertService(IdempotentReceiver, IEventSubscriber):
    """Monitors speed-violation events and issues penalty notices.

    Inherits from IdempotentReceiver to guarantee that the same violation
    is never penalised twice, even if the event is delivered more than once.
    """

    def __init__(self):
        super().__init__()
        self.penalty_count = 0

    def process_event(self, envelope):
        if isinstance(envelope.payload, SpeedViolationEvent):
            self.penalty_count += 1
            print(
                f"[PENALTY NOTICE] Plate: {envelope.payload.plate_number} | "
                f"Speed: {envelope.payload.measured_speed} km/h "
                f"(limit {envelope.payload.speed_limit} km/h) — "
                f"Penalty #{self.penalty_count}"
            )


class LoggingService(IdempotentReceiver, IEventSubscriber):
    """Records every unique event as a structured log entry.

    Uses idempotent processing to avoid duplicate log records when the
    same event envelope is delivered more than once.
    """

    def __init__(self):
        super().__init__()
        self.log = []

    def process_event(self, envelope):
        entry = {
            "event_id": envelope.event_id,
            "event_type": envelope.event_type,
            "timestamp": envelope.timestamp,
            "source_id": envelope.source_id,
            "payload": envelope.payload,
        }
        self.log.append(entry)
        print(f"[LOG] {entry}")


class DashboardService(IEventSubscriber):
    """Pushes real-time status updates to the traffic-management dashboard.

    Handles vehicle detections, congestion alerts, and traffic-cleared
    notifications so that operators always see the latest road conditions.
    """

    def on_event(self, envelope):
        payload = envelope.payload

        if isinstance(payload, VehicleDetectedEvent):
            print(
                f"[DASHBOARD] Vehicle detected — Plate: {payload.plate_number} | "
                f"Camera: {payload.camera_id} | Lane: {payload.lane_number}"
            )

        elif isinstance(payload, CongestionAlertEvent):
            print(
                f"[DASHBOARD] Congestion alert — Intersection: {payload.intersection_id} | "
                f"Vehicles: {payload.vehicle_count} | Severity: {payload.severity_level}"
            )

        elif isinstance(payload, TrafficClearedEvent):
            print(
                f"[DASHBOARD] Traffic cleared — Intersection: {payload.intersection_id} | "
                f"Camera: {payload.camera_id}"
            )


class ReportingService(IEventSubscriber):
    """Collects vehicle-detection and speed-violation data for periodic reports.

    Stores raw event payloads so they can be aggregated, filtered, or
    exported later by the reporting pipeline.
    """

    def __init__(self):
        self.report_data = []

    def on_event(self, envelope):
        payload = envelope.payload

        if isinstance(payload, VehicleDetectedEvent):
            self.report_data.append(payload)

        elif isinstance(payload, SpeedViolationEvent):
            self.report_data.append(payload)
