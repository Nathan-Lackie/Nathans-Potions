import sqlalchemy
from src import database as db


def get_gold() -> int:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT gold FROM global_inventory",
            ),
        ).first()

    if result is None:
        raise RuntimeError("Error getting gold")

    return result[0]


def set_gold(amount: int):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "UPDATE global_inventory SET gold = :amount",
            ).bindparams(amount=amount),
        )


def update_gold(amount: int):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "UPDATE global_inventory SET gold = gold + :amount",
            ).bindparams(amount=amount),
        )
