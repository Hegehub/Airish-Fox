# Google Maps

Set these variables to enable the store map:

- `GOOGLE_MAPS_API_KEY`
- `GOOGLE_MAPS_MAP_ID`
- `GOOGLE_MAPS_DEFAULT_ZOOM=15`

In production, restrict the key by HTTP referrer/domain and enable only the APIs required for the embedded Maps JavaScript experience. If `GOOGLE_MAPS_API_KEY` is empty, store pages render an address and directions fallback instead of loading Google Maps JavaScript.
