from fastapi import FastAPI

app = FastAPI()


__version__ = "0.0.1"


@app.get("/version")
async def get_version():
    return {"version": __version__}
