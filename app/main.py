from fastapi import FastAPI, HTTPException
from .sensebox import get_temps, FIRST_SENSEBOX_ID, SECOND_SENSEBOX_ID, THIRD_SENSEBOX_ID

__version__ = "0.0.1"
app = FastAPI()


@app.get("/version")
async def get_version():
    return {"version": __version__}


@app.get("/temperature")
async def get_temp():
    temps = get_temps(
        [FIRST_SENSEBOX_ID, SECOND_SENSEBOX_ID, THIRD_SENSEBOX_ID])
    if not temps:
        raise HTTPException(
            status_code=404, detail="No recent temperature data available")
    average_temp = sum(float(temp) for temp in temps) / len(temps)
    return {"temperature": round(average_temp, 2)}
