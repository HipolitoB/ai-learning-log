"""Building AI — Chapter 1 (Optimization), Exercise 1: Listing Pineapple Routes.

Generates every possible shipping route starting from Panama (PAN) across all
remaining ports and prints each route alongside its estimated CO2 emissions.
"""

PORT_NAMES = ["PAN", "AMS", "CAS", "NYC", "HEL"]

# Sea distances between ports in kilometers (converted from nautical miles).
DISTANCES_KM = [
    [0, 8943, 8019, 3652, 10545],
    [8943, 0, 2619, 6317, 2078],
    [8019, 2619, 0, 5836, 4939],
    [3652, 6317, 5836, 0, 7825],
    [10545, 2078, 4939, 7825, 0],
]

# Emissions factor: 20 g CO2 per km per metric ton of cargo -> 0.020 kg/km.
CO2_KG_PER_KM = 0.020


def route_emissions(route: list[int]) -> float:
    """Return total CO2 emissions (kg) for a sequence of port indices."""
    total_distance = sum(
        DISTANCES_KM[i][j] for i, j in zip(route[:-1], route[1:])
    )
    return total_distance * CO2_KG_PER_KM


def permutations(route: list[int], remaining_ports: list[int]) -> None:
    """Recursively enumerate and print all routes starting with `route`."""
    if not remaining_ports:
        emissions = route_emissions(route)
        labels = " ".join(PORT_NAMES[i] for i in route)
        print(f"{labels} {emissions:.1f} kg")
        return

    for idx, port in enumerate(remaining_ports):
        next_remaining = remaining_ports[:idx] + remaining_ports[idx + 1:]
        permutations(route + [port], next_remaining)


def main() -> None:
    """Start recursion from PAN (index 0) across ports 1..4 (24 total routes)."""
    permutations([0], list(range(1, len(PORT_NAMES))))


if __name__ == "__main__":
    main()
