import sqlalchemy
from src import database as db


def get_liquid_capacity() -> int:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT capacity FROM capacity WHERE type = 'liquid'",
            ),
        ).first()

    if result is None:
        raise RuntimeError("Error getting liquid capacity")

    return result[0] * 10000
