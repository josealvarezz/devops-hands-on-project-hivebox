import os
from datetime import datetime, timezone, timedelta
import requests
from .exceptions import ExternalAPIError

DEFAULT_IDS = "5c72ec079e6756001987288b,61eec6bf848248001ba4beeb,61bf38bf19a991001b0e5cb4"
SENSEBOX_IDS = os.getenv("SENSEBOX_IDS", DEFAULT_IDS).split(',')

APIURL = "https://api.opensensemap.org/boxes/"


def get_temps(sensebox_ids: list[str]):
    temps = []
    for sensebox_id in sensebox_ids:
        sensebox_id = sensebox_id.strip()
        if not sensebox_id:
            continue

        try:
            response = requests.get(f"{APIURL}/{sensebox_id}", timeout=10)

            response.raise_for_status()

            sensebox_data = response.json()

            sensors_list = sensebox_data.get("sensors")
            if not sensors_list or not isinstance(sensors_list, list):
                print(
                    f"Warning: No 'sensors' list found for box ID {sensebox_id}. Skipping.")
                continue

            temp_sensor = None
            for sensor in sensors_list:
                if isinstance(sensor, dict) and sensor.get("title") == "Temperatur":
                    temp_sensor = sensor
                    break
            if not temp_sensor:
                print(
                    f"Warning: No temperature sensor found for box ID {sensebox_id}. Skipping.")
                continue

            last_measurement = temp_sensor.get("lastMeasurement")

            if (
                last_measurement
                and last_measurement.get("value") is not None
                and last_measurement.get("createdAt")
            ):
                created_at = datetime.strptime(
                    last_measurement["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)

                if now - created_at <= timedelta(hours=1):
                    temps.append(float(last_measurement["value"]))

        except requests.exceptions.HTTPError as http_err:
            print(
                f"Warning: HTTP error for ID '{sensebox_id}': {http_err}. Skipping.")
            continue
        except requests.exceptions.RequestException as req_err:
            raise ExternalAPIError(
                f"Network error for ID '{sensebox_id}': {req_err}."
            ) from req_err
        except (ValueError, KeyError, TypeError) as e:
            print(
                f"Warning: Data processing error for ID '{sensebox_id}': {e}. Skipping.")
            continue

    return temps


def get_status(temp: float):
    if temp < 10:
        return "Too Cold"
    elif 11 <= temp <= 36:
        return "Good"
    elif temp > 37:
        return "Too Hot"
