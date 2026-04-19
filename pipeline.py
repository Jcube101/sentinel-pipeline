import logging
import sys
import time

from supabase import Client, create_client

from config import SUPABASE_SERVICE_KEY, SUPABASE_URL
from fetchers import eonet, firms, gdacs, openaq, usgs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)

EVENTS_TABLE = "events"
AQI_TABLE = "aqi_readings"
BATCH_SIZE = 500


def _chunks(lst: list, size: int):
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def _run_fetcher(name: str, module) -> tuple[list, bool]:
    """Call module.fetch(), return (results, success)."""
    try:
        results = module.fetch()
        logger.info("%s: fetched %d rows", name, len(results))
        return results, True
    except Exception as exc:
        logger.error("%s: fetcher raised an exception — %s", name, exc)
        return [], False


def _upsert(supabase, table: str, rows: list, conflict_key: str) -> int:
    if not rows:
        return 0
    upserted = 0
    for batch in _chunks(rows, BATCH_SIZE):
        supabase.table(table).upsert(batch, on_conflict=conflict_key).execute()
        upserted += len(batch)
    return upserted


def run():
    start = time.monotonic()
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

    # --- Run fetchers ---
    firms_rows,  firms_ok  = _run_fetcher("FIRMS",  firms)
    eonet_rows,  eonet_ok  = _run_fetcher("EONET",  eonet)
    gdacs_rows,  gdacs_ok  = _run_fetcher("GDACS",  gdacs)
    usgs_rows,   usgs_ok   = _run_fetcher("USGS",   usgs)
    openaq_rows, openaq_ok = _run_fetcher("OpenAQ", openaq)

    any_failure = not all([firms_ok, eonet_ok, gdacs_ok, usgs_ok, openaq_ok])

    # --- Write events ---
    all_events = firms_rows + eonet_rows + gdacs_rows + usgs_rows
    try:
        events_upserted = _upsert(supabase, EVENTS_TABLE, all_events, "id")
        logger.info("events: upserted %d rows", events_upserted)
    except Exception as exc:
        logger.error("events: upsert failed — %s", exc)
        events_upserted = 0
        any_failure = True

    # --- Write AQI readings ---
    try:
        aqi_upserted = _upsert(supabase, AQI_TABLE, openaq_rows, "location_id,parameter,recorded_at")
        logger.info("aqi_readings: upserted %d rows", aqi_upserted)
    except Exception as exc:
        logger.error("aqi_readings: upsert failed — %s", exc)
        aqi_upserted = 0
        any_failure = True

    duration = time.monotonic() - start

    print("")
    print("=== Sentinel Pipeline Run ===")
    print(f"  FIRMS:   {len(firms_rows)} events")
    print(f"  EONET:   {len(eonet_rows)} events")
    print(f"  GDACS:   {len(gdacs_rows)} events")
    print(f"  USGS:    {len(usgs_rows)} earthquakes")
    print(f"  OpenAQ:  {len(openaq_rows)} readings")
    print(f"  Total events upserted:       {events_upserted}")
    print(f"  Total AQI readings upserted: {aqi_upserted}")
    print(f"  Duration: {duration:.1f}s")
    print("============================")

    return 1 if any_failure else 0


if __name__ == "__main__":
    sys.exit(run())
