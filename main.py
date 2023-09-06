import logging
import os
from datetime import datetime

from fastapi import FastAPI
from starlette import status
from starlette.responses import Response

from custom_i18n.schd import Languages
from generate_calendar import main as generate_calendar

app = FastAPI(
    title="ITMO Schedule API",
    version="1.0",
    description="API for converting ITMO schedule to iCalendar format",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)


def check_env():
    if not os.getenv("API_KEY"):
        msg = "API_KEY is not set"
        raise ValueError(msg)


check_env()


@app.get("/")
def get_root() -> Response:
    return Response(content=None, status_code=status.HTTP_200_OK)


@app.get("/{api_key}/{start_date}/{end_date}/{language}/schedule.ics")
def get_calendar(
    api_key: str,
    start_date: str | datetime,
    end_date: str | datetime,
    language: Languages,
) -> Response:
    if api_key != os.getenv("API_KEY"):
        return Response(content=None, status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        calendar = generate_calendar(start_date, end_date, language=language)
    except Exception as e:
        return Response(
            content={"result": None, "error": e.__str__()},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(
        content=calendar,
        media_type="text/calendar",
        status_code=status.HTTP_200_OK,
    )
