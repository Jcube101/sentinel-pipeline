# Sentinel Roadmap

## Phase 1 — Pipeline (COMPLETE ✅)
- [x] Supabase schema design (events, aqi_readings, sources, categories tables)
- [x] NASA FIRMS fetcher (fire hotspots)
- [x] NASA EONET fetcher (wildfires, cyclones)
- [x] GDACS fetcher (floods, cyclones, earthquakes)
- [x] USGS fetcher (earthquakes)
- [x] OpenAQ fetcher (AQI readings)
- [x] pipeline.py orchestrator
- [x] backfill.py for historical data
- [x] archive.py for local SQLite archiving
- [x] 60-day rolling cleanup on Supabase
- [x] Windows Task Scheduler for automated archiving
- [x] Render cron job (daily 6:30am IST)
- [x] Monorepo restructure (pipeline/ + frontend/)

## Phase 2 — Frontend V1 (IN PROGRESS 🔧)

### Structure
- [ ] Vite + React + TypeScript scaffold in frontend/
- [ ] Standalone design system (dark, utilitarian, data-forward — separate identity from job-joseph.com)
- [ ] Deployed as Render static site

### Landing page
- [ ] Hero section explaining what Sentinel is
- [ ] Live event count stats (fires, floods, cyclones, earthquakes)
- [ ] "View Live Map" CTA
- [ ] Data sources attribution section
- [ ] Footer with GitHub link

### Dashboard page (/dashboard)
- [ ] MapLibre GL map centred on India (dark OpenFreeMap tiles)
- [ ] Coloured event markers by category fire=#ef4444, flood=#3b82f6, cyclone=#8b5cf6, earthquake=#f59e0b
- [ ] Supercluster clustering for FIRMS hotspots
- [ ] Category filter toggles (fire/flood/cyclone/earthquake)
- [ ] Status filter (open/closed/all)
- [ ] Days range filter (7/30/90 days)
- [ ] Event detail panel on marker click
- [ ] Stats bar using Recharts (event counts over time)
- [ ] Mobile responsive layout

### Data layer
- [ ] Supabase client (anon key, env vars on Render)
- [ ] useNaturalEvents hook (React Query, 15min stale)
- [ ] useAqiReadings hook (React Query, 30min stale)

## Phase 3 — Frontend V2 (PLANNED 📋)
- [ ] AQI heatmap overlay layer
- [ ] Cyclone track lines from EONET geometry sequences
- [ ] Historical trend charts (Recharts, 90-day view)
- [ ] Tighter India bbox filtering (remove border noise)
- [ ] OpenAQ pagination for more station coverage
- [ ] Custom subdomain (sentinel.job-joseph.com)

## Phase 4 — Enhancements (FUTURE 💡)
- [ ] Alert/notification system for high severity events
- [ ] Public API endpoint for Sentinel data
- [ ] OpenAPI documentation
- [ ] Flood season historical analysis (June-September)
- [ ] Expand coverage beyond India bbox

---

## Build Log

| Date | Milestone |
|------|-----------|
| Apr 2026 | Pipeline complete — all 5 fetchers working |
| Apr 2026 | 100k+ events backfilled into Supabase |
| Apr 2026 | Render cron deployed, daily automation live |
| Apr 2026 | Monorepo restructured |
| Apr 2026 | Frontend V1 in progress |
