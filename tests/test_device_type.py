"""Unit tests for DeviceType."""

from bond_api.device_type import DeviceType


def test_compare_device_types():
    """Tests that constants are configured and compared correctly."""
    assert DeviceType.CEILING_FAN == "CF"
    assert DeviceType.is_fan("CF")

    assert DeviceType.MOTORIZED_SHADES == "MS"
    assert DeviceType.is_shades("MS")

    assert DeviceType.FIREPLACE == "FP"
    assert DeviceType.is_fireplace("FP")

    assert DeviceType.GENERIC_DEVICE == "GX"
    assert DeviceType.is_generic("GX")
