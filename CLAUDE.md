# Sentinel Pipeline

Python data pipeline for the Sentinel natural disaster tracker.
Fetches from 5 APIs and upserts to Supabase every 30 minutes via Render cron.

## Stack
- Python 3.11
- supabase-py
- requests
- python-dotenv

## Environment Variables
- SUPABASE_URL
- SUPABASE_SERVICE_KEY
- FIRMS_MAP_KEY
- OPENAQ_API_KEY

## Data Sources
- FIRMS: fire hotspots (India bbox: 68.7,8.4,97.4,37.1)
- EONET: cyclones + wildfires (category filter + India bbox)
- GDACS: floods, cyclones, earthquakes (GeoJSON feed)
- USGS: earthquakes (India bbox, min magnitude 4.0)
- OpenAQ: AQI readings for Indian cities (PM2.5, PM10, NO2)

## Supabase Tables
- events: all disaster events
- aqi_readings: air quality readings

## Schema — events table
id: text (primary key, deterministic)
external_id: text
source: text (FIRMS | EONET | GDACS | USGS)
category: text (fire | flood | cyclone | earthquake)
title: text
description: text
severity: text (low | medium | high | extreme)
severity_value: numeric
severity_unit: text
status: text (open | closed)
started_at: timestamptz
closed_at: timestamptz
latitude: numeric
longitude: numeric
place_name: text
geometry: jsonb
source_url: text
raw: jsonb
created_at: timestamptz
updated_at: timestamptz

## Schema — aqi_readings table
id: bigint (auto)
location_id: text
location_name: text
city: text
latitude: numeric
longitude: numeric
parameter: text (pm25 | pm10 | no2 | so2 | o3)
value: numeric
unit: text
recorded_at: timestamptz
created_at: timestamptz

## Key Rules
- Every fetcher returns List[dict] matching Supabase schema exactly
- IDs must be deterministic — built from source data, never random UUIDs
- Always upsert, never plain insert (conflict key: id column)
- One fetcher must never crash the whole pipeline — wrap each in try/except
- Log clearly: source name, rows fetched, rows upserted, any errors
- Never hardcode credentials — always read from environment variables