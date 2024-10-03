from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import utils

router = APIRouter(
    prefix="/info",
    tags=["info"],
    dependencies=[Depends(auth.get_api_key)],
)


class Timestamp(BaseModel):
    day: str
    hour: int


@router.post("/current_time")
def post_time(timestamp: Timestamp):
    """
    Share current time.
    """

    print(f"Current Time: {timestamp.day} {timestamp.hour}")

    utils.set_time(timestamp.day, timestamp.hour)

    return "OK"
