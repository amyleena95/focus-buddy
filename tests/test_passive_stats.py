import unittest

from pet_stats import PetStats
from passive_stats import apply_passive_changes, SECONDS_PER_HOUR


class TestPassiveStats(unittest.TestCase):
    def test_needs_change_over_one_hour(self):
        stats = PetStats()

        apply_passive_changes(stats, SECONDS_PER_HOUR)

        self.assertEqual(stats.hunger, 97)
        self.assertEqual(stats.energy, 98)
        self.assertEqual(stats.cleanliness, 99)
        self.assertEqual(stats.playfulness, 51)

    def test_energy_does_not_decrease_while_asleep(self):
        stats = PetStats()

        apply_passive_changes(
            stats,
            SECONDS_PER_HOUR,
            awake=False,
        )

        self.assertEqual(stats.energy, 100)

    def test_playfulness_does_not_increase_when_not_idle(self):
        stats = PetStats()

        apply_passive_changes(
            stats,
            SECONDS_PER_HOUR,
            idle=False,
        )

        self.assertEqual(stats.playfulness, 50)

    def test_happiness_decreases_when_a_need_is_low(self):
        stats = PetStats(hunger=20)

        apply_passive_changes(stats, SECONDS_PER_HOUR)

        self.assertEqual(stats.happiness, 99)

    def test_offline_time_is_capped_at_twelve_hours(self):
        stats = PetStats()

        applied = apply_passive_changes(
            stats,
            24 * SECONDS_PER_HOUR,
            offline=True,
        )

        self.assertEqual(applied, 12 * SECONDS_PER_HOUR)
        self.assertEqual(stats.hunger, 64)

    def test_stat_values_stay_in_range(self):
        stats = PetStats(hunger=2, energy=1, cleanliness=1)

        apply_passive_changes(stats, 10 * SECONDS_PER_HOUR)

        self.assertGreaterEqual(stats.hunger, 0)
        self.assertGreaterEqual(stats.energy, 0)
        self.assertGreaterEqual(stats.cleanliness, 0)


if __name__ == "__main__":
    unittest.main()