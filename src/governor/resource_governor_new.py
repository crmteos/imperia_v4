"""Resource Governor for Edge SLM and P2P Duty Cycle"""

import time


class ResourceGovernor:
    """Autonomous resource governor for Edge SLM and P2P duty cycle."""

    BATTERY_CRITICAL_PCT = 15
    BATTERY_LOW_PCT = 30
    THERMAL_THROTTLE_CELSIUS = 45.0

    MODES = {
        "CRITICAL": "Pause inference, keep lightweight P2P heartbeat only",
        "BALANCED": "Local SLM execution, selective P2P swarm duty cycle",
        "PERFORMANCE": "Full P2P swarm inference host and local agent execution"
    }

    def __init__(self):
        self._mode = "PERFORMANCE"
        self._metrics_history = []
        self._max_history = 100

    @property
    def mode(self) -> str:
        return self._mode

    @mode.setter
    def mode(self, new_mode: str) -> None:
        if new_mode in self.MODES:
            self._mode = new_mode
        else:
            raise ValueError(f"Invalid mode: {new_mode}")

    def update_metrics(self, battery_pct: float = None,
                       temperature_celsius: float = None,
                       is_charging: bool = None,
                       network_available: bool = None) -> dict:
        metrics = {
            "timestamp": time.time(),
            "battery_pct": battery_pct,
            "temperature_celsius": temperature_celsius,
            "is_charging": is_charging,
            "network_available": network_available
        }
        self._metrics_history.append(metrics)
        if len(self._metrics_history) > self._max_history:
            self._metrics_history.pop(0)
        new_mode = self._determine_mode(metrics)
        if new_mode != self._mode:
            self._mode = new_mode
        return {
            "mode": self._mode,
            "metrics": metrics,
            "previous_mode": self._mode
        }

    def _determine_mode(self, metrics: dict) -> str:
        battery = metrics.get("battery_pct")
        temperature = metrics.get("temperature_celsius")

        if temperature is not None and temperature > self.THERMAL_THROTTLE_CELSIUS:
            return "CRITICAL"
        if battery is not None and battery <= self.BATTERY_CRITICAL_PCT:
            return "CRITICAL"
        if battery is not None and self.BATTERY_CRITICAL_PCT < battery <= self.BATTERY_LOW_PCT:
            return "BALANCED"
        return "PERFORMANCE"

    def get_mode_description(self) -> str:
        return self.MODES.get(self._mode, "Unknown mode")

    def get_status_report(self) -> dict:
        recent_metrics = self._metrics_history[-1] if self._metrics_history else {}
        return {
            "mode": self._mode,
            "mode_description": self.get_mode_description(),
            "battery_pct": recent_metrics.get("battery_pct"),
            "temperature_celsius": recent_metrics.get("temperature_celsius"),
            "is_charging": recent_metrics.get("is_charging"),
            "network_available": recent_metrics.get("network_available"),
            "timestamp": recent_metrics.get("timestamp")
        }


if __name__ == "__main__":
    governor = ResourceGovernor()
    print("Resource Governor Status")
    print("=" * 40)
    print(f"Initial mode: {governor.mode}")
    print(f"Mode description: {governor.get_mode_description()}")
    print()

    test_scenarios = [
        ("Normal operation", 80.0, 35.0, True, True),
        ("Battery low", 25.0, 35.0, False, True),
        ("Battery critical", 10.0, 35.0, False, True),
        ("Thermal throttle", 70.0, 55.0, True, True),
    ]

    for name, battery, temp, charging, network in test_scenarios:
        result = governor.update_metrics(
            battery_pct=battery,
            temperature_celsius=temp,
            is_charging=charging,
            network_available=network
        )
        print(f"Scenario: {name}")
        print(f"  Battery: {battery}%, Temp: {temp}°C")
        print(f"  Mode: {result['mode']} - {governor.get_mode_description()}")
        print()