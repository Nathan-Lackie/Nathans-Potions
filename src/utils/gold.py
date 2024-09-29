import sqlalchemy
from src import database as db


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
