from dataclasses import dataclass


# Published when a vehicle is detected by a traffic camera.
@dataclass
class VehicleDetectedEvent:
    vehicle_id: str
    plate_number: str
    camera_id: str
    lane_number: int | None = None


# Published when a detected vehicle exceeds the configured speed limit.
@dataclass
class SpeedViolationEvent:
    vehicle_id: str
    plate_number: str
    measured_speed: float
    speed_limit: float
    camera_id: str


# Published when traffic congestion is detected at an intersection.
@dataclass
class CongestionAlertEvent:
    intersection_id: str
    vehicle_count: int
    severity_level: str
    camera_id: str


# Published when traffic at an intersection returns to normal flow.
@dataclass
class TrafficClearedEvent:
    intersection_id: str
    camera_id: str


# Published when an emergency vehicle is detected and needs priority handling.
@dataclass
class EmergencyVehicleEvent:
    vehicle_id: str
    plate_number: str
    vehicle_type: str
    priority_level: str
    camera_id: str
