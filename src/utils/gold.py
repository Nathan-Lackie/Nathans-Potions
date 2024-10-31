import sqlalchemy
from src import database as db


def get_gold() -> int:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT SUM(update) as total_gold FROM gold",
            ),
        ).one()

    return result.total_gold


def reset_gold():
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """DELETE FROM gold;
                ALTER SEQUENCE gold_id_seq RESTART WITH 1;""",
            ),
        )


def update_gold(amount: int):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "INSERT INTO gold (update) VALUES (:amount)",
            ).bindparams(amount=amount),
        )
