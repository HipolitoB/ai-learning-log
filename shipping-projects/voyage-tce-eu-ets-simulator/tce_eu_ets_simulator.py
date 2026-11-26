"""Voyage Charter Time-Charter Equivalent (TCE) & EU-ETS Carbon Simulator.

Models net voyage revenue, bunker fuel burn (VLSFO vs. Bio-LNG), 2026 EU-ETS
maritime allowance obligations (100% intra-EU port-to-port vs. 50% extra-EU),
and resulting net TCE in EUR/day.
"""

from __future__ import annotations

from dataclasses import dataclass

CO2_FACTORS_TONNES_PER_MT: dict[str, float] = {
    "VLSFO": 3.151,
    "MGO": 3.206,
    "BIO_LNG": 0.550,  # Indicative well-to-wake blended factor for comparison
}


@dataclass(frozen=True)
class VoyageScenario:
    route_name: str
    voyage_days: float
    gross_freight_eur: float
    port_and_canal_costs_eur: float
    address_commission_pct: float
    fuel_type: str
    fuel_mt_per_day: float
    fuel_price_eur_per_mt: float
    eua_price_eur: float
    intra_eu: bool


def simulate_voyage_tce(scenario: VoyageScenario) -> dict[str, float | str | bool]:
    """Compute bunker cost, EU-ETS carbon surcharge, and net TCE (EUR/day)."""
    if scenario.voyage_days <= 0:
        raise ValueError("voyage_days must be positive")
    if scenario.fuel_type not in CO2_FACTORS_TONNES_PER_MT:
        raise ValueError(f"Unsupported fuel_type: {scenario.fuel_type}")

    commission_eur = scenario.gross_freight_eur * (scenario.address_commission_pct / 100.0)
    net_freight_eur = scenario.gross_freight_eur - commission_eur

    total_fuel_mt = scenario.fuel_mt_per_day * scenario.voyage_days
    bunker_cost_eur = total_fuel_mt * scenario.fuel_price_eur_per_mt

    co2_tonnes = total_fuel_mt * CO2_FACTORS_TONNES_PER_MT[scenario.fuel_type]
    ets_scope = 1.0 if scenario.intra_eu else 0.5
    ets_cost_eur = co2_tonnes * ets_scope * scenario.eua_price_eur

    net_earnings_eur = net_freight_eur - bunker_cost_eur - scenario.port_and_canal_costs_eur - ets_cost_eur
    tce_eur_per_day = net_earnings_eur / scenario.voyage_days

    return {
        "route_name": scenario.route_name,
        "fuel_type": scenario.fuel_type,
        "intra_eu": scenario.intra_eu,
        "ets_scope_pct": round(ets_scope * 100.0, 1),
        "bunker_cost_eur": round(bunker_cost_eur, 2),
        "co2_tonnes": round(co2_tonnes, 2),
        "ets_cost_eur": round(ets_cost_eur, 2),
        "net_earnings_eur": round(net_earnings_eur, 2),
        "tce_eur_per_day": round(tce_eur_per_day, 2),
    }


def main() -> None:
    scenarios = [
        VoyageScenario(
            route_name="Barcelona -> Piraeus (VLSFO, Intra-EU 100%)",
            voyage_days=5.5,
            gross_freight_eur=145000.0,
            port_and_canal_costs_eur=24000.0,
            address_commission_pct=3.75,
            fuel_type="VLSFO",
            fuel_mt_per_day=24.0,
            fuel_price_eur_per_mt=540.0,
            eua_price_eur=72.0,
            intra_eu=True,
        ),
        VoyageScenario(
            route_name="Casablanca -> Barcelona (VLSFO, Extra-EU 50%)",
            voyage_days=3.0,
            gross_freight_eur=82000.0,
            port_and_canal_costs_eur=16500.0,
            address_commission_pct=3.75,
            fuel_type="VLSFO",
            fuel_mt_per_day=22.0,
            fuel_price_eur_per_mt=540.0,
            eua_price_eur=72.0,
            intra_eu=False,
        ),
        VoyageScenario(
            route_name="Barcelona -> Piraeus (Bio-LNG Blend, Intra-EU 100%)",
            voyage_days=5.5,
            gross_freight_eur=145000.0,
            port_and_canal_costs_eur=24000.0,
            address_commission_pct=3.75,
            fuel_type="BIO_LNG",
            fuel_mt_per_day=20.0,
            fuel_price_eur_per_mt=760.0,
            eua_price_eur=72.0,
            intra_eu=True,
        ),
    ]

    print("Voyage Charter TCE & EU-ETS Simulator (2026 Scope)")
    print("-" * 92)
    for sc in scenarios:
        res = simulate_voyage_tce(sc)
        print(
            f"{res['route_name']:<52} | ETS {res['ets_scope_pct']:>5}%: "
            f"EUR {res['ets_cost_eur']:>8.2f} | TCE: EUR {res['tce_eur_per_day']:>8.2f}/day"
        )
    print("-" * 92)


if __name__ == "__main__":
    main()
