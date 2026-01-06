"""
Unit management using Pint library.
"""

from pint import UnitRegistry

# Create a single UnitRegistry instance for the entire package
ureg = UnitRegistry()
Q_ = ureg.Quantity
