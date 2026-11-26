import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "shipping-projects" / "voyage-tce-eu-ets-simulator"),
)

from tce_eu_ets_simulator import VoyageScenario, simulate_voyage_tce


def test_intra_eu_vs_extra_eu_ets_scope() -> None:
    base = dict(
        route_name="Sample Route",
        voyage_days=4.0,
        gross_freight_eur=100000.0,
        port_and_canal_costs_eur=15000.0,
        address_commission_pct=0.0,
        fuel_type="VLSFO",
        fuel_mt_per_day=25.0,
        fuel_price_eur_per_mt=500.0,
        eua_price_eur=70.0,
    )
    intra = simulate_voyage_tce(VoyageScenario(intra_eu=True, **base))
    extra = simulate_voyage_tce(VoyageScenario(intra_eu=False, **base))
    assert intra["ets_scope_pct"] == 100.0
    assert extra["ets_scope_pct"] == 50.0
    assert intra["ets_cost_eur"] == round(2.0 * float(extra["ets_cost_eur"]), 2)
    assert float(intra["tce_eur_per_day"]) < float(extra["tce_eur_per_day"])


def test_tce_calculation_values() -> None:
    sc = VoyageScenario(
        route_name="Direct Check",
        voyage_days=2.0,
        gross_freight_eur=60000.0,
        port_and_canal_costs_eur=10000.0,
        address_commission_pct=5.0,
        fuel_type="MGO",
        fuel_mt_per_day=10.0,
        fuel_price_eur_per_mt=600.0,
        eua_price_eur=50.0,
        intra_eu=True,
    )
    res = simulate_voyage_tce(sc)
    # Net freight = 57000, bunker = 12000, port = 10000, co2 = 20*3.206=64.12t, ets = 3206 -> net = 31794 -> 15897/day
    assert res["co2_tonnes"] == 64.12
    assert res["ets_cost_eur"] == 3206.0
    assert res["tce_eur_per_day"] == 15897.0
