import unittest

from pet_stats import PetStats
from pet_interactions import PetInteractions


class TestPetInteractions(unittest.TestCase):
    def test_pet_increases_happiness_affection_and_trust(self):
        stats = PetStats()
        interactions = PetInteractions(stats)

        result = interactions.perform("pet")

        self.assertTrue(result.success)
        self.assertEqual(stats.happiness, 100)  # Clamped at maximum
        self.assertEqual(stats.affection, 2)
        self.assertEqual(stats.trust, 1)

    def test_feed_increases_hunger(self):
        stats = PetStats(hunger=50)
        interactions = PetInteractions(stats)

        result = interactions.perform("feed")

        self.assertTrue(result.success)
        self.assertEqual(stats.hunger, 75)

    def test_feed_is_rejected_when_full(self):
        stats = PetStats(hunger=100)
        interactions = PetInteractions(stats)

        result = interactions.perform("feed")

        self.assertFalse(result.success)
        self.assertEqual(stats.hunger, 100)

    def test_play_is_rejected_when_energy_is_too_low(self):
        stats = PetStats(energy=14)
        interactions = PetInteractions(stats)

        result = interactions.perform("play")

        self.assertFalse(result.success)
        self.assertEqual(stats.energy, 14)

    def test_play_consumes_energy_and_playfulness(self):
        stats = PetStats(energy=50, playfulness=50)
        interactions = PetInteractions(stats)

        result = interactions.perform("play")

        self.assertTrue(result.success)
        self.assertEqual(stats.energy, 40)
        self.assertEqual(stats.playfulness, 30)

    def test_sleep_restores_energy(self):
        stats = PetStats(energy=50)
        interactions = PetInteractions(stats)

        result = interactions.perform("sleep")

        self.assertTrue(result.success)
        self.assertEqual(stats.energy, 80)

    def test_groom_restores_cleanliness(self):
        stats = PetStats(cleanliness=50)
        interactions = PetInteractions(stats)

        result = interactions.perform("groom")

        self.assertTrue(result.success)
        self.assertEqual(stats.cleanliness, 75)

    def test_repeated_petting_has_diminishing_returns(self):
        stats = PetStats(happiness=0)
        interactions = PetInteractions(stats)

        interactions.perform("pet")
        interactions.perform("pet")

        self.assertEqual(stats.happiness, 7.5)

    def test_unknown_action_is_rejected(self):
        interactions = PetInteractions(PetStats())

        result = interactions.perform("bathe")

        self.assertFalse(result.success)


if __name__ == "__main__":
    unittest.main()