from core.event_bus import EventBus
from core.event_envelope import EventEnvelope
from core.events import (
    VehicleDetectedEvent,
    SpeedViolationEvent,
    CongestionAlertEvent,
    TrafficClearedEvent,
)
from core.subscribers import (
    AlertService,
    LoggingService,
    DashboardService,
    ReportingService,
)


print("=" * 50)
print("=== Traffic Alert System Starting ===")
print("=" * 50)

# ── Create the central event bus ──────────────────────────────────────
bus = EventBus()

# ── Create service instances ──────────────────────────────────────────
alert_service = AlertService()
logging_service = LoggingService()
dashboard_service = DashboardService()
reporting_service = ReportingService()

# ── Subscribe all services to the bus ─────────────────────────────────
bus.subscribe(alert_service)
bus.subscribe(logging_service)
bus.subscribe(dashboard_service)
bus.subscribe(reporting_service)
print("All services subscribed.\n")

# ── 1. Vehicle Detected ───────────────────────────────────────────────
print("-" * 50)
vehicle_event = VehicleDetectedEvent(
    vehicle_id="V001",
    plate_number="ABC-123",
    camera_id="CAM_01",
    lane_number=2,
)
envelope1 = EventEnvelope(
    correlation_id="JOURNEY_001",
    source_id="CAM_01",
    payload=vehicle_event,
)
bus.publish(envelope1)

# ── 2. Speed Violation ────────────────────────────────────────────────
print("-" * 50)
speed_event = SpeedViolationEvent(
    vehicle_id="V002",
    plate_number="XYZ-999",
    measured_speed=95.0,
    speed_limit=60.0,
    camera_id="CAM_02",
)
envelope2 = EventEnvelope(
    correlation_id="JOURNEY_001",
    source_id="CAM_02",
    payload=speed_event,
)
bus.publish(envelope2)

# ── 3. Congestion Alert ──────────────────────────────────────────────
print("-" * 50)
congestion_event = CongestionAlertEvent(
    intersection_id="INT_05",
    vehicle_count=85,
    severity_level="HIGH",
    camera_id="CAM_03",
)
envelope3 = EventEnvelope(
    correlation_id="JOURNEY_001",
    source_id="CAM_03",
    payload=congestion_event,
)
bus.publish(envelope3)

# ── 4. Traffic Cleared ───────────────────────────────────────────────
print("-" * 50)
cleared_event = TrafficClearedEvent(
    intersection_id="INT_05",
    camera_id="CAM_03",
)
envelope4 = EventEnvelope(
    correlation_id="JOURNEY_001",
    source_id="CAM_03",
    payload=cleared_event,
)
bus.publish(envelope4)

# ── Demonstrate Unsubscribe ──────────────────────────────────────────
print("\n" + "=" * 50)
print("=== Demonstrating Unsubscribe ===")
print("=" * 50)

bus.unsubscribe(dashboard_service)
print("DashboardService has been unsubscribed.\n")

print("-" * 50)
vehicle_event2 = VehicleDetectedEvent(
    vehicle_id="V003",
    plate_number="LMN-456",
    camera_id="CAM_01",
    lane_number=1,
)
envelope5 = EventEnvelope(
    correlation_id="JOURNEY_001",
    source_id="CAM_01",
    payload=vehicle_event2,
)
bus.publish(envelope5)
print("(Notice: DashboardService did NOT receive this event)\n")

# ── Final Summary ────────────────────────────────────────────────────
print("=" * 50)
print("=== Final Summary ===")
print("=" * 50)
print(f"Total penalties issued   : {alert_service.penalty_count}")
print(f"Total log entries        : {len(logging_service.log)}")
print(f"Total report data points : {len(reporting_service.report_data)}")
