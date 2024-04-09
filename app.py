import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from config.settings import *

app = FastAPI()


def chat_doc(msg):
    data = {"content": "",
            "notifyParams": [{"type": "openIds", "values": [msg.operatorOpenid]}]}
    requests.post(YUNZHIJIA_NOTIFY_URL, json=data)


class ApiFoxEvent(BaseModel):
    event: str
    title: str
    content: str


@app.post("/apifox/{project}")
async def handle_apifox_event(project: str, request: Request, event: ApiFoxEvent):
    headers = request.headers
    logging.info(f"Received headers: {headers}")

    logging.info(f"[{project}]: {event}")
    # logging.info(f"Title: {event.title}")
    # logging.info(f"Content: {event.content}")

    return {"message": "Event processed"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9191)
