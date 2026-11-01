from dataclasses import dataclass

from pet_stats import PetStats


@dataclass
class InteractionResult:
    success: bool
    message: str


class PetInteractions:
    """Apply player actions to Tondu's stats."""

    def __init__(self, stats: PetStats):
        self.stats = stats
        self._last_action = None
        self._repeat_count = 0

    def perform(self, action: str) -> InteractionResult:
        action = action.lower().strip()

        actions = {
            "pet": self._pet,
            "feed": self._feed,
            "play": self._play,
            "sleep": self._sleep,
            "groom": self._groom,
        }

        if action not in actions:
            return InteractionResult(False, f"Unknown action: {action}")

        # Reduce gains when the same action is repeated consecutively.
        if action == self._last_action:
            self._repeat_count += 1
        else:
            self._last_action = action
            self._repeat_count = 0

        # First use: full effect. Repeats: 50%, then 25%, then 10%.
        multiplier = (1.0, 0.5, 0.25, 0.1)[
            min(self._repeat_count, 3)
        ]

        return actions[action](multiplier)

    def _change(self, stat_name, amount):
        self.stats.change(stat_name, round(amount, 2))

    def _pet(self, multiplier):
        self._change("happiness", 5 * multiplier)
        self._change("affection", 2 * multiplier)
        self._change("trust", 1 * multiplier)
        return InteractionResult(True, "Tondu enjoyed being petted.")

    def _feed(self, multiplier):
        if self.stats.get("hunger") >= 100:
            return InteractionResult(False, "Tondu is already full.")

        self._change("hunger", 25 * multiplier)
        self._change("happiness", 3 * multiplier)
        self._change("affection", 1 * multiplier)
        self._change("trust", 1 * multiplier)
        return InteractionResult(True, "You fed Tondu.")

    def _play(self, multiplier):
        if self.stats.get("energy") < 15:
            return InteractionResult(False, "Tondu is too tired to play.")

        self._change("happiness", 10 * multiplier)
        self._change("affection", 2 * multiplier)
        self._change("trust", 1 * multiplier)
        self._change("energy", -10)
        self._change("playfulness", -20)
        return InteractionResult(True, "You played with Tondu.")

    def _sleep(self, multiplier):
        if self.stats.get("energy") >= 100:
            return InteractionResult(False, "Tondu is already fully rested.")

        self._change("energy", 30 * multiplier)
        self._change("happiness", 2 * multiplier)
        return InteractionResult(True, "Tondu had a little rest.")

    def _groom(self, multiplier):
        if self.stats.get("cleanliness") >= 100:
            return InteractionResult(False, "Tondu is already clean.")

        self._change("cleanliness", 25 * multiplier)
        self._change("happiness", 4 * multiplier)
        self._change("affection", 1 * multiplier)
        self._change("trust", 1 * multiplier)
        return InteractionResult(True, "You groomed Tondu.")