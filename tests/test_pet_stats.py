import unittest

from pet_stats import PetStats


class TestPetStats(unittest.TestCase):
    def test_all_seven_stats_exist(self):
        stats = PetStats()

        self.assertEqual(
            stats.stat_names(),
            [
                "happiness",
                "hunger",
                "energy",
                "cleanliness",
                "affection",
                "trust",
                "playfulness",
            ],
        )

    def test_default_values(self):
        stats = PetStats()

        self.assertEqual(stats.happiness, 100)
        self.assertEqual(stats.hunger, 100)
        self.assertEqual(stats.energy, 100)
        self.assertEqual(stats.cleanliness, 100)
        self.assertEqual(stats.affection, 0)
        self.assertEqual(stats.trust, 0)
        self.assertEqual(stats.playfulness, 50)

    def test_values_are_clamped(self):
        stats = PetStats()

        stats.set("happiness", 150)
        stats.set("hunger", -10)

        self.assertEqual(stats.happiness, 100)
        self.assertEqual(stats.hunger, 0)

    def test_change_updates_stat(self):
        stats = PetStats()

        stats.change("affection", 5)
        stats.change("playfulness", -10)

        self.assertEqual(stats.affection, 5)
        self.assertEqual(stats.playfulness, 40)

    def test_unknown_stat_is_rejected(self):
        stats = PetStats()

        with self.assertRaises(KeyError):
            stats.set("thirst", 50)

    def test_non_numeric_value_is_rejected(self):
        stats = PetStats()

        with self.assertRaises(TypeError):
            stats.set("happiness", "high")


if __name__ == "__main__":
    unittest.main()