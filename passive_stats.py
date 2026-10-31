from pet_stats import PetStats


SECONDS_PER_HOUR = 60 * 60
MAX_OFFLINE_HOURS = 12


def apply_passive_changes(
    stats: PetStats,
    elapsed_seconds: float,
    *,
    awake: bool = True,
    idle: bool = True,
    offline: bool = False,
) -> float:
    """Apply gradual stat changes and return the time actually applied."""

    if elapsed_seconds < 0:
        raise ValueError("Elapsed time cannot be negative.")

    # Limit offline catch-up so a long absence doesn't drain Tondu completely.
    applied_seconds = elapsed_seconds
    if offline:
        applied_seconds = min(
            applied_seconds,
            MAX_OFFLINE_HOURS * SECONDS_PER_HOUR,
        )

    hours = applied_seconds / SECONDS_PER_HOUR

    stats.change("hunger", -3 * hours)

    if awake:
        stats.change("energy", -2 * hours)

    stats.change("cleanliness", -1 * hours)

    if idle:
        stats.change("playfulness", 1 * hours)

    physical_needs = ("hunger", "energy", "cleanliness")
    if any(stats.get(name) < 30 for name in physical_needs):
        stats.change("happiness", -1 * hours)

    return applied_seconds