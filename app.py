from datetime import datetime
from fastapi import Depends, HTTPException
import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from config.settings import *
from dotenv import load_dotenv

app = FastAPI()
# 加载环境变量
load_dotenv()


class ApiFoxEvent(BaseModel):
    event: str
    title: str
    content: str


def notify_yzj(msg):
    data = {"content": f" {msg}"}
    requests.post(YUNZHIJIA_NOTIFY_URL, json=data)


async def verify_token(token: str = None):
    if token != os.getenv("APIFOX_KEY"):
        raise HTTPException(status_code=403, detail="Invalid token")
    return True


@app.post("/apifox/{project}")
async def handle_apifox_event(project: str, request: Request, event: ApiFoxEvent, token: bool = Depends(verify_token)):
    headers = request.headers
    logging.info(f"Received headers: {headers}")

    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{dt_string} {project}] {event}"

    logging.info(msg)
    notify_yzj(msg)

    return {"message": "Event processed"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9191)
