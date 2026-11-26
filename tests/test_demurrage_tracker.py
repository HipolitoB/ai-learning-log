from datetime import date
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "shipping-projects" / "container-demurrage-tracker"),
)

from demurrage_tracker import Shipment, calculate_demurrage, count_free_time_end


def test_count_free_time_calendar_days() -> None:
    assert count_free_time_end(date(2026, 11, 10), 7, exclude_weekends=False) == date(2026, 11, 16)


def test_count_free_time_excluding_weekends() -> None:
    assert count_free_time_end(date(2026, 11, 12), 7, exclude_weekends=True) == date(2026, 11, 20)


def test_calculate_demurrage_exposed_and_within_free_time() -> None:
    exposed = Shipment("MSCU4829103", "Barcelona", date(2026, 11, 10), date(2026, 11, 21), 7, 95.0)
    res_exposed = calculate_demurrage(exposed, date(2026, 11, 24))
    assert res_exposed["chargeable_days"] == 5
    assert res_exposed["exposure_eur"] == 475.0
    assert res_exposed["status"] == "EXPOSED"

    within = Shipment("CMAU7712049", "Algeciras", date(2026, 11, 19), None, 7, 85.0)
    res_within = calculate_demurrage(within, date(2026, 11, 24))
    assert res_within["chargeable_days"] == 0
    assert res_within["exposure_eur"] == 0.0
    assert res_within["status"] == "WITHIN_FREE_TIME"
