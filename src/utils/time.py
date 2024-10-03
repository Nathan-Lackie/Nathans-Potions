import sqlalchemy
from src import database as db


def set_time(day: str, hour: int):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "UPDATE time SET day = :day, hour = :hour",
            ).bindparams(day=day, hour=hour),
        )
