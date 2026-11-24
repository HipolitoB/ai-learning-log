"""Container Demurrage & Detention (D&D) Free-Time & Exposure Tracker.

Calculates port free-time expiration, chargeable days (supporting calendar vs.
business-day rules), and total EUR/USD exposure across multi-port shipments.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class Shipment:
    container_id: str
    port: str
    discharge_date: date
    gate_out_date: date | None
    free_days: int
    daily_rate_eur: float
    exclude_weekends_in_free_time: bool = False


def count_free_time_end(start: date, free_days: int, exclude_weekends: bool) -> date:
    """Return the last free day (inclusive) starting from discharge_date."""
    if free_days <= 0:
        return start - timedelta(days=1)

    current = start
    counted = 0
    while True:
        is_weekend = current.weekday() >= 5
        if not (exclude_weekends and is_weekend):
            counted += 1
        if counted >= free_days:
            return current
        current += timedelta(days=1)


def calculate_demurrage(shipment: Shipment, as_of: date) -> dict[str, object]:
    """Compute free-time end date, chargeable days, and accrued demurrage."""
    effective_end = shipment.gate_out_date or as_of
    last_free_day = count_free_time_end(
        shipment.discharge_date,
        shipment.free_days,
        shipment.exclude_weekends_in_free_time,
    )
    chargeable_days = max(0, (effective_end - last_free_day).days)
    exposure_eur = round(chargeable_days * shipment.daily_rate_eur, 2)
    status = "EXPOSED" if chargeable_days > 0 else "WITHIN_FREE_TIME"
    return {
        "container_id": shipment.container_id,
        "port": shipment.port,
        "last_free_day": last_free_day.isoformat(),
        "effective_end": effective_end.isoformat(),
        "chargeable_days": chargeable_days,
        "exposure_eur": exposure_eur,
        "status": status,
    }


def main() -> None:
    today = date(2026, 11, 24)
    shipments = [
        Shipment("MSCU4829103", "Barcelona (ESBCN)", date(2026, 11, 10), date(2026, 11, 21), free_days=7, daily_rate_eur=95.0),
        Shipment("MAEU9031224", "Piraeus (GRPIR)", date(2026, 11, 12), None, free_days=7, daily_rate_eur=110.0, exclude_weekends_in_free_time=True),
        Shipment("CMAU7712049", "Algeciras (ESALG)", date(2026, 11, 19), None, free_days=7, daily_rate_eur=85.0),
    ]

    total_exposure = 0.0
    print(f"Demurrage Exposure Report (as of {today.isoformat()})")
    print("-" * 78)
    for s in shipments:
        res = calculate_demurrage(s, today)
        total_exposure += float(res["exposure_eur"])
        print(
            f"{res['container_id']} | {res['port']:<18} | Last Free: {res['last_free_day']} | "
            f"Days: {res['chargeable_days']:>2} | EUR {res['exposure_eur']:>7.2f} | {res['status']}"
        )
    print("-" * 78)
    print(f"Total Accrued Demurrage Exposure: EUR {total_exposure:.2f}")


if __name__ == "__main__":
    main()
