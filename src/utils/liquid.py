import sqlalchemy
import src.database as db


def get_liquid():
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("SELECT type, amount FROM liquid_inventory")
        )

    return dict([liquid.tuple() for liquid in result])


def set_liquid(colors: tuple[int, int, int, int]):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """UPDATE liquid_inventory
                SET amount = CASE
                    WHEN type = 'red' THEN :red
                    WHEN type = 'green' THEN :green
                    WHEN type = 'blue' THEN :blue
                    WHEN type = 'dark' THEN :dark
                END
                WHERE type IN ('red', 'green', 'blue', 'dark');""",
            ).bindparams(
                red=colors[0], green=colors[1], blue=colors[2], dark=colors[3]
            ),
        )


def update_liquid(colors: tuple[int, int, int, int]):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """UPDATE liquid_inventory
                SET amount = CASE
                    WHEN type = 'red' THEN amount + :red
                    WHEN type = 'green' THEN amount + :green
                    WHEN type = 'blue' THEN amount + :blue
                    WHEN type = 'dark' THEN amount + :dark
                END
                WHERE type IN ('red', 'green', 'blue', 'dark');""",
            ).bindparams(
                red=colors[0], green=colors[1], blue=colors[2], dark=colors[3]
            ),
        )
