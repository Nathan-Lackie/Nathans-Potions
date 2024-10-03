import sqlalchemy
from src import database as db
from src.utils.customer import Customer


def set_visits(customers: list[Customer]):
    with db.engine.begin() as connection:
        for customer in customers:
            connection.execute(
                sqlalchemy.text(
                    """INSERT INTO visits (customer_id, day, hour)
                    SELECT customers.id, time.day, time.hour FROM time, customers
                    WHERE customers.name = :name AND customers.character_class = :character_class AND customers.level = :level""",
                ).bindparams(
                    name=customer.customer_name,
                    character_class=customer.character_class,
                    level=customer.level,
                ),
            )
