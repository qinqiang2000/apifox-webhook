from datetime import datetime

import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from config.settings import *

app = FastAPI()


class ApiFoxEvent(BaseModel):
    event: str
    title: str
    content: str


def notify_yzj(msg):
    data = {"content": f" {msg}"}
    requests.post(YUNZHIJIA_NOTIFY_URL, json=data)


@app.post("/apifox/{project}")
async def handle_apifox_event(project: str, request: Request, event: ApiFoxEvent):
    headers = request.headers
    logging.info(f"Received headers: {headers}")

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    msg = f"[{dt_string} {project}] {event}"
    logging.info(msg)

    notify_yzj(msg)

    return {"message": "Event processed"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9191)
