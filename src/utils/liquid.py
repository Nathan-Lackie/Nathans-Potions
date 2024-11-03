from typing import Literal
import sqlalchemy
import src.database as db


def get_liquid() -> dict[Literal["red", "green", "blue", "dark"], int]:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("SELECT color, SUM(update) FROM liquid GROUP BY color")
        )

    return dict([liquid.tuple() for liquid in result])


def get_liquid_tuple():
    liquid = get_liquid()
    return (liquid["red"], liquid["green"], liquid["blue"], liquid["dark"])


def get_total_liquid() -> int:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("SELECT SUM(update) as total FROM liquid")
        ).one()

    return result.total


def reset_liquid():
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """DELETE FROM liquid;
                ALTER SEQUENCE liquid_id_seq RESTART WITH 1;
                INSERT INTO liquid (color, update)
                VALUES ('red', 0), ('green', 0), ('blue', 0), ('dark', 0)""",
            ),
        )


colors = ("red", "green", "blue", "dark")


def update_liquid(values: tuple[int, int, int, int]):
    with db.engine.begin() as connection:
        for color, value in zip(colors, values):
            if value != 0:
                connection.execute(
                    sqlalchemy.text(
                        "INSERT INTO liquid (color, update) VALUES (:color, :update)",
                    ).bindparams(color=color, update=value),
                )
