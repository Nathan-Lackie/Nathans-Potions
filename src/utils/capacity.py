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


def set_liquid_capacity(capacity: int):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "UPDATE capacity SET capacity = :capacity WHERE type = 'liquid'",
            ).bindparams(capacity=capacity),
        )


def get_potion_capacity() -> int:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT capacity FROM capacity WHERE type = 'potion'",
            ),
        ).first()

    if result is None:
        raise RuntimeError("Error getting potion capacity")

    return result[0] * 50


def set_potion_capacity(capacity: int):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "UPDATE capacity SET capacity = :capacity WHERE type = 'potion'",
            ).bindparams(capacity=capacity),
        )
