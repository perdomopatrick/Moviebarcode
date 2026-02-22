# Moviebarcode

A Moviebarcode represents a film/video as a single image by averaging the colours of each individual frame (or every few seconds) into thin, chronological, vertical slivers.

Runs locally.

:image:

### Set up environment:
```bat
uv sync
```

### Run:
```bat
:: Open Docker
.venv\Scripts\activate
docker build -t moviebarcode .
main.py
```
```bat
deactivate & :: to leave virtual environment
```

### Tech:
- Python 
- Docker
- FFmpeg
- CustomTkinter (UI)
