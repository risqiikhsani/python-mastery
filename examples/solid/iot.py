from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Dict, Union, Any
from pydantic import BaseModel, Field, field_validator, model_validator

# 1. ENUMS & CONSTANTS

class DeviceType(str, Enum):
    THERMOSTAT = "thermostat"
    SECURITY_CAMERA = "security_camera"
    MOTION_DETECTOR = "motion_detector"

class SystemAlertLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

# 2. PYDANTIC MODELS (Telemetry Validation & Deep Nesting)

class DeviceMetadata(BaseModel):
    firmware_version: str = Field(..., pattern=r"^v\d+\.\d+\.\d+$")  # e.g., "v2.1.14"
    battery_level_pct: float = Field(..., ge=0.0, le=100.0)

class TelemetryPacket(BaseModel):
    packet_id: str
    device_id: str
    device_type: DeviceType
    timestamp: datetime
    metadata: DeviceMetadata
    sensor_readings: Dict[str, Any]

    @field_validator("timestamp")
    @classmethod
    def prevent_future_timestamps(cls, v):
        if v > datetime.now():
            raise ValueError("Timestamp cannot be in the future")
        return v
    
    @model_validator(mode="after")
    def validate_payload_by_type(self) -> "TelemetryPacket":
        readings = self.sensor_readings

        if self.device_type == DeviceType.THERMOSTAT:
            if "temperature_c" not in readings or "humidity_pct" not in readings:
                raise ValueError("Thermostat packets must include 'temperature_c' and 'humidity_pct'")
            # Faulty sensor protection: block extreme, unphysical anomalies
            if not (-40.0 <= readings["temperature_c"] <= 60.0):
                raise ValueError("Temperature reading falls outside survival threshold (-40C to 60C).")
        
        elif self.device_type == DeviceType.SECURITY_CAMERA:
            if "motion_detected" not in readings or "frame_analysed_count" not in readings:
                raise ValueError("Security Camera payloads must contain 'motion_detected' and 'frame_analysed_count'.")

        return self
    
# 3. ABSTRACTION & INHERITANCE (Telemetry Processing Pipeline)

class TelemetryProcessor(ABC):

    def __init__(self, target_database_name: str):
        self.db_name = target_database_name

    @abstractmethod
    def evaluate_metrics(self, packet: TelemetryPacket) -> SystemAlertLevel:
        """Analyzes readings and flags anomalies or security incidents."""
        pass

    def log_to_time_series_db(self, packet: TelemetryPacket):
        """Shared utility method inherited by all pipeline subclasses."""
        print(f"[Storage] Appending packet {packet.packet_id} into time-series bucket: '{self.db_name}'")

class ClimateProcessor(TelemetryProcessor):
    """Concrete stream processing for climate control devices like thermostats."""

    def evaluate_metrics(self, packet: TelemetryPacket) -> SystemAlertLevel:
        temp = packet.sensor_readings["temperature_c"]
        humidity = packet.sensor_readings["humidity_pct"]

        if temp > 40.0 or temp < 5.0:
            print(f"⚠️ [Climate Alert] Extreme climate threshold breached: {temp}°C")
            return SystemAlertLevel.WARNING
        elif humidity > 80.0:
            print(f"⚠️ [Climate Alert] High humidity detected: {humidity}%")
            return SystemAlertLevel.WARNING
        return SystemAlertLevel.INFO
    
class SecurityProcessor(TelemetryProcessor):
    """Concrete stream processing security camera and tactical sensor feeds."""

    def evaluate_metrics(self, packet: TelemetryPacket) -> SystemAlertLevel:
        is_motion = packet.sensor_readings.get("motion_detected", False)
        frames = packet.sensor_readings.get("frame_analysed_count", 0)
        
        # Severe alert if motion is caught across multiple concurrent system frames
        if is_motion and frames > 30:
            print(f"🚨 [Security Breach] High confidence activity trace detected!")
            return SystemAlertLevel.CRITICAL
        elif is_motion:
            print(f"🔍 [Security Note] Minor motion event flagged.")
            return SystemAlertLevel.WARNING
        return SystemAlertLevel.INFO
    
# 4. COMPOSITION & EVENT ROUTER ENGINE

class SmartHomeCentralHub:
    """The central composition coordinator.
    
    It houses multiple dedicated processing subsystems and routes arriving data
    polymorphically based on configuration mappings.
    """

    def __init__(self, stream_registry: Dict[DeviceType, TelemetryProcessor]):
        self._registry = stream_registry

    def ingest_packet(self, raw_json_data: dict) -> bool:
        print(f"\n📡 Hub received raw wireless telemetry signal...")

        # Step 1: Enforce structural sanitization using Pydantic
        try:
            packet = TelemetryPacket(**raw_json_data)
            print(f"✅ Telemetry verified. Device: {packet.device_id} ({packet.device_type.value}) passed parsing.")
        except Exception as validation_error:
            print(f"❌ Drop Packet: Network payload rejected as corrupt/malformed.\n{validation_error}")
            return False
        
        # Step 2: Extract processor via polymorphic mapping
        processor = self._registry.get(packet.device_type)
        if not processor:
            print(f"❌ System Error: Unregistered device runtime pipeline for type {packet.device_type}.")
            return False
        
        # Step 3: Execute Business Pipeline Logic
        alert_level = processor.evaluate_metrics(packet)
        print(f"   - Processing Result Analysis Status: [{alert_level.value}]")

        # Step 4: Persistent logging via inherited base class logic
        processor.log_to_time_series_db(packet)
        return True
    
# Setup our composable stream routing rules
pipeline_routing_table = {
    DeviceType.THERMOSTAT: ClimateProcessor(target_database_name="hvac_environmental_logs"),
    DeviceType.SECURITY_CAMERA: SecurityProcessor(target_database_name="perimeter_security_logs"),
    DeviceType.MOTION_DETECTOR: SecurityProcessor(target_database_name="perimeter_security_logs")
}

# Construct the Orchestration Hub injecting dependencies
iot_hub = SmartHomeCentralHub(stream_registry=pipeline_routing_table)

# SAMPLE 1: Normal Thermostat Ingestion

normal_thermostat_data = {
    "packet_id": "PKT-10041",
    "device_id": "DEV-HVAC-99",
    "device_type": "thermostat",
    "timestamp": str(datetime.now()),
    "metadata": {"firmware_version": "v1.0.4", "battery_level_pct": 84.5},
    "sensor_readings": {"temperature_c": 22.4, "humidity_pct": 45.0}
}

iot_hub.ingest_packet(normal_thermostat_data)

# SAMPLE 2: Extreme Sensor Fault Check (Caught by Pydantic Model Validator)

glitched_thermostat_data = {
    "packet_id": "PKT-10042",
    "device_id": "DEV-HVAC-99",
    "device_type": "thermostat",
    "timestamp": str(datetime.now()),
    "metadata": {"firmware_version": "v1.0.4", "battery_level_pct": 84.5},
    # ❌ -50.0C fails our survival validator block check!
    "sensor_readings": {"temperature_c": -50.0, "humidity_pct": 12.0} 
}
iot_hub.ingest_packet(glitched_thermostat_data)

# SAMPLE 3: Critical Security Breach Telemetry Processing

security_breach_data = {
    "packet_id": "PKT-88192",
    "device_id": "DEV-CAM-BACKYARD",
    "device_type": "security_camera",
    "timestamp": str(datetime.now()),
    "metadata": {"firmware_version": "v3.2.1", "battery_level_pct": 99.1},
    "sensor_readings": {"motion_detected": True, "frame_analysed_count": 142}
}
iot_hub.ingest_packet(security_breach_data)