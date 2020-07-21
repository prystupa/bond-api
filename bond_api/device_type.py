"""Bond Device type enumeration."""


class DeviceType:
    """Bond Device type enumeration."""
    CEILING_FAN = "CF"
    MOTORIZED_SHADES = "MS"
    FIREPLACE = "FP"
    GENERIC_DEVICE = "GX"

    @staticmethod
    def is_fan(device_type: str) -> bool:
        """Checks if specified device type is a fan."""
        return device_type == DeviceType.CEILING_FAN

    @staticmethod
    def is_shades(device_type: str) -> bool:
        """Checks if specified device type is shades."""
        return device_type == DeviceType.MOTORIZED_SHADES

    @staticmethod
    def is_fireplace(device_type: str) -> bool:
        """Checks if specified device type is fireplace."""
        return device_type == DeviceType.FIREPLACE

    @staticmethod
    def is_generic(device_type: str) -> bool:
        """Checks if specified device type is generic."""
        return device_type == DeviceType.GENERIC_DEVICE
