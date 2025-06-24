from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
import requests
FIRST_SENSEBOX_ID = "5c72ec079e6756001987288b"
SECOND_SENSEBOX_ID = "61eec6bf848248001ba4beeb"
THIRD_SENSEBOX_ID = "61bf38bf19a991001b0e5cb4"
APIURL = "https://api.opensensemap.org/boxes/"


def get_temps(sensebox_ids: list[str]):
    temps = []
    for sensebox_id in sensebox_ids:
        try:
            sensebox_data = requests.get(f"{APIURL}/{sensebox_id}").json()
        except Exception as exc:
            raise HTTPException(
                status_code=502, detail="Error fetching data from openSenseMap") from exc
        sensor = sensebox_data.get("sensors")[2]
        last_measurement = sensor.get("lastMeasurement") if sensor else None

        if (
            last_measurement
            and last_measurement.get("value") is not None
            and last_measurement.get("createdAt")
        ):
            try:
                created_at = datetime.strptime(
                    last_measurement["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                if now - created_at <= timedelta(hours=1):
                    temps.append(last_measurement["value"])
            except Exception:
                continue
    return temps
