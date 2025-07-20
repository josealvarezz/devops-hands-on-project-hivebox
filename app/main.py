from fastapi import FastAPI, HTTPException
from .sensebox import get_temps, get_status, SENSEBOX_IDS
from .exceptions import ExternalAPIError
from prometheus_fastapi_instrumentator import Instrumentator

__version__ = "0.2.0"
app = FastAPI()
Instrumentator().instrument(app).expose(app)


@app.get("/version")
async def get_version():
    return {"version": __version__}


@app.get("/temperature")
async def get_temp():
    try:
        temps = get_temps(SENSEBOX_IDS)
    except ExternalAPIError as exc:
        raise HTTPException(
            status_code=502, detail="Error communicating with openSenseMap API"
        ) from exc
    if not temps:
        raise HTTPException(
            status_code=404, detail="No recent temperature data available")
    average_temp = round(sum(float(temp) for temp in temps) / len(temps), 2)
    return {"temperature": average_temp,
            "status": get_status(average_temp)}
