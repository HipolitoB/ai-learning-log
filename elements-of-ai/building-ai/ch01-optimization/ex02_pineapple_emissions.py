"""Building AI — Chapter 1 (Optimization), Exercise 2: Minimum Route Emissions.

Generalizes route-emission evaluation to any number of ports and prints the
single lowest-CO2 shipping route starting from port 0 (PAN).
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

CO2_KG_PER_KM = 0.020


def find_best_route(
    route: list[int],
    remaining_ports: list[int],
    best: tuple[float, list[int]],
) -> tuple[float, list[int]]:
    """Return (min_emissions, best_route) via recursive depth-first search."""
    if not remaining_ports:
        distance = sum(
            DISTANCES_KM[i][j] for i, j in zip(route[:-1], route[1:])
        )
        emissions = distance * CO2_KG_PER_KM
        if emissions < best[0]:
            return (emissions, route)
        return best

    for idx, port in enumerate(remaining_ports):
        next_remaining = remaining_ports[:idx] + remaining_ports[idx + 1:]
        best = find_best_route(route + [port], next_remaining, best)
    return best


def main() -> None:
    """Compute and print the optimal shipping route from PAN."""
    best_emissions, best_route = find_best_route(
        [0],
        list(range(1, len(PORT_NAMES))),
        (float("inf"), []),
    )
    labels = " ".join(PORT_NAMES[i] for i in best_route)
    print(f"{labels} {best_emissions:.1f} kg")


if __name__ == "__main__":
    main()
