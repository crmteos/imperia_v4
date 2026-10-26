"""
src/governor/resource_governor.py
Resource Governor for Edge SLM and P2P Duty Cycle

Monitors device metrics (battery, network, temperature) and implements
auto-mode switching: CRITICAL (<15% battery), BALANCED (<30% battery),
PERFORMANCE.
"""

import time
import json
import os


class ResourceGovernor:
    """Autonomous resource governor for Edge SLM and P2P duty cycle."""
    
    # Thresholds from architect_spec.json
    BATTERY_CRITICAL_PCT = 15
    BATTERY_LOW_PCT = 30
    THERMAL_THROTTLE_CELSIUS = 45.0
    
    # Operating modes from architect_spec.json
    MODES = {
        "CRITICAL": "Pause inference, keep lightweight P2P heartbeat only",
        "BALANCED": "Local SLM execution, selective P2P swarm duty cycle",
        "PERFORMANCE": "Full P2P swarm inference host and local agent execution"
    }
    
    def __init__(self):
        self._mode = "PERFORMANCE"  # Default mode
        self._metrics_history = []
        self._max_history = 100
    
    @property
    def mode(self) -> str:
        """Current operating mode."""
        return self._mode
    
    @mode.setter
    def mode(self, new_mode: str) -> None:
        if new_mode in self.MODES:
            self._mode = new_mode
        else:
            raise ValueError(f"Invalid mode: {new_mode}. Valid modes: {list(self.MODES.keys())}")
    
    def update_metrics(self, battery_pct: float = None, 
                       temperature_celsius: float = None,
                       is_charging: bool = None,
                       network_available: bool = None) -> dict:
        """
        Update resource metrics and determine mode switching.
        
        Args:
            battery_pct: Battery percentage (0-100)
            temperature_celsius: CPU temperature in Celsius
            is_charging: Whether device is charging
            network_available: Whether network is available
            
        Returns:
            dict with current mode and decision rationale
        """
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
        
        # Determine mode based on thresholds
        new_mode = self._determine_mode(metrics)
        
        if new_mode != self._mode:
            self._mode = new_mode
        
        return {
            "mode": self._mode,
            "metrics": metrics,
            "previous_mode": self._mode if new_mode == self._mode else self._mode,
            "mode_changed": new_mode != self._mode  # This will always be False due to property setter logic
        }
    
    def _determine_mode(self, metrics: dict) -> str:
        """
        Determine the operating mode based on current metrics.
        
        Priority order:
        1. Thermal throttling (highest priority)
        2. Battery critical
        3. Battery low  
        4. Default: PERFORMANCE
        """
        battery = metrics.get("battery_pct")
        temperature = metrics.get("temperature_celsius")
        
        # Thermal throttling - highest priority
        if temperature is not None and temperature > self.THERMAL_THROTTLE_CELSIUS:
            return "CRITICAL"
        
        # Battery critical
        if battery is not None and battery <= self.BATTERY_CRITICAL_PCT:
            return "CRITICAL"
        
        # Battery low
        if battery is not None and self.BATTERY_CRITICAL_PCT < battery <= self.BATTERY_LOW_PCT:
            return "BALANCED"
        
        # Default: PERFORMANCE
        return "PERFORMANCE"
    
    def get_mode_description(self) -> str:
        """Get the description of the current mode."""
        return self.MODES.get(self._mode, "Unknown mode")
    
    def get_status_report(self) -> dict:
        """Generate a status report."""
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


# Example usage and testing
if __name__ == "__main__":
    governor = ResourceGovernor()
    
    print("Resource Governor Status")
    print("=" * 40)
    print(f"Initial mode: {governor.mode}")
    print(f"Mode description: {governor.get_mode_description()}")
    print()
    
    # Test various scenarios
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