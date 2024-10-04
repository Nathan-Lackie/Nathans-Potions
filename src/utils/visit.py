import sqlalchemy
from src import database as db
from src.utils import Customer
from src.utils.customer import set_customers


def __attempt_recent_visit(connection: sqlalchemy.Connection, customer: Customer):
    return connection.execute(
        sqlalchemy.text(
            """SELECT MAX(visits.id) FROM visits
                JOIN customers ON visits.customer_id = customers.id
                WHERE customers.name = :name AND customers.character_class = :character_class AND customers.level = :level"""
        ).bindparams(
            name=customer.customer_name,
            character_class=customer.character_class,
            level=customer.level,
        )
    ).first()


# Gets the id for a customer's most recent visit
def get_recent_visit(customer: Customer) -> int:
    with db.engine.begin() as connection:
        result = __attempt_recent_visit(connection, customer)

        # If this fails, either the requesting customer doesn't exist in the customers table,
        # or they don't have a most recent visit in the visits table
        if result is None or result[0] is None:
            print(f"Warning: Customer {customer.dict()} is not tracked. Remedying.")

            set_customers([customer])
            set_visits([customer])

            result = __attempt_recent_visit(connection, customer)

        # If this *still* fails, something is really wrong
        if result is None or result[0] is None:
            raise RuntimeError(f"Failed to track customer: {customer.dict()}")

    return result[0]


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
