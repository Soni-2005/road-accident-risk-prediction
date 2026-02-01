import os

WEATHER_API_KEY = os.getenv("3cf3bfdbb59e3e15a9758d617bd658af")

if WEATHER_API_KEY is None:
    raise RuntimeError("WEATHER_API_KEY not set in environment")
