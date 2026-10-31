from dataclasses import dataclass, fields
from math import floor


STAT_MIN = 0
STAT_MAX = 100


@dataclass
class PetStats:
    happiness: int = 100
    hunger: int = 100
    energy: int = 100
    cleanliness: int = 100
    affection: int = 0
    trust: int = 0
    playfulness: int = 50

    def __post_init__(self):
        # Validate and clamp initial values too.
        for stat_name in self.stat_names():
            value = getattr(self, stat_name)
            self._validate_number(value)
            setattr(self, stat_name, self._clamp(value))

    @classmethod
    def stat_names(cls):
        """Return the names of all stats in a consistent order."""
        return [field.name for field in fields(cls)]

    @staticmethod
    def _validate_number(value):
        # bool is a subclass of int in Python, so reject it explicitly.
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Stat values must be numbers.")

    @staticmethod
    def _clamp(value):
        """Keep a stat within the allowed 0–100 range."""
        return max(STAT_MIN, min(STAT_MAX, value))

    def get(self, stat_name):
        """Read a stat by name."""
        if stat_name not in self.stat_names():
            raise KeyError(f"Unknown stat: {stat_name}")
        return getattr(self, stat_name)

    def set(self, stat_name, value):
        """Set a stat, keeping it within the allowed range."""
        if stat_name not in self.stat_names():
            raise KeyError(f"Unknown stat: {stat_name}")

        self._validate_number(value)
        setattr(self, stat_name, self._clamp(value))

    def change(self, stat_name, amount):
        """Increase or decrease a stat by an amount."""
        self._validate_number(amount)
        self.set(stat_name, self.get(stat_name) + amount)

    def get_display_value(self, stat_name):
        """Return a rounded whole-number value for the UI."""
        return round(self.get(stat_name))

    def get_display_value(self, stat_name):
        """Round positive stat values to the nearest whole number."""
        return floor(self.get(stat_name) + 0.5)