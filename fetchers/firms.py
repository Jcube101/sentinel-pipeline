import csv
import hashlib
import io
import logging
from datetime import datetime, timezone

import requests

from config import FIRMS_MAP_KEY, INDIA_BBOX_FIRMS

logger = logging.getLogger(__name__)

ENDPOINT = (
    "https://firms.modaps.eosdis.nasa.gov/api/area/csv"
    "/{key}/VIIRS_NOAA20_NRT/{bbox}/1"
)


def _severity(frp: float) -> str:
    if frp > 100:
        return "extreme"
    if frp > 50:
        return "high"
    if frp > 10:
        return "medium"
    return "low"


def _parse_datetime(acq_date: str, acq_time: str) -> str:
    """Return ISO 8601 UTC string from FIRMS acq_date (YYYY-MM-DD) and acq_time (HHMM)."""
    acq_time = acq_time.zfill(4)
    dt = datetime.strptime(f"{acq_date} {acq_time}", "%Y-%m-%d %H%M")
    return dt.replace(tzinfo=timezone.utc).isoformat()


def fetch() -> list[dict]:
    url = ENDPOINT.format(key=FIRMS_MAP_KEY, bbox=INDIA_BBOX_FIRMS)
    logger.info("FIRMS: fetching from %s", url)

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as exc:
        logger.error("FIRMS: request failed — %s", exc)
        return []

    try:
        reader = csv.DictReader(io.StringIO(resp.text))
        rows = list(reader)
    except Exception as exc:
        logger.error("FIRMS: CSV parse failed — %s", exc)
        return []

    events = []
    for row in rows:
        try:
            lat = float(row["latitude"])
            lon = float(row["longitude"])
            acq_date = row["acq_date"]
            acq_time = row["acq_time"]
            frp = float(row.get("frp") or 0)

            event_id = f"FIRMS-{lat}-{lon}-{acq_date}-{acq_time}"
            started_at = _parse_datetime(acq_date, acq_time)

            events.append({
                "id": event_id,
                "external_id": event_id,
                "source": "FIRMS",
                "category": "fire",
                "title": f"Fire hotspot at ({lat:.4f}, {lon:.4f})",
                "description": (
                    f"VIIRS NOAA-20 fire hotspot. "
                    f"Brightness: {row.get('bright_ti4', 'N/A')} K, "
                    f"FRP: {frp} MW, "
                    f"Confidence: {row.get('confidence', 'N/A')}."
                ),
                "severity": _severity(frp),
                "severity_value": frp,
                "severity_unit": "MW",
                "status": "open",
                "started_at": started_at,
                "closed_at": None,
                "latitude": lat,
                "longitude": lon,
                "place_name": None,
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "source_url": "https://firms.modaps.eosdis.nasa.gov/",
                "raw": dict(row),
                "created_at": None,
                "updated_at": None,
            })
        except Exception as exc:
            logger.warning("FIRMS: skipping row due to error — %s | row=%s", exc, row)

    logger.info("FIRMS: fetched %d fire hotspot events", len(events))
    return events


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    results = fetch()
    print(f"\nTotal events: {len(results)}")
    print("\nFirst 3 results:")
    for event in results[:3]:
        print({k: v for k, v in event.items() if k != "raw"})
