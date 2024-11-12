from typing import Literal
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from enum import Enum
from src import utils
from src.utils import Customer

router = APIRouter(
    prefix="/carts",
    tags=["cart"],
    dependencies=[Depends(auth.get_api_key)],
)


class search_sort_options(str, Enum):
    customer_name = "customer_name"
    item_sku = "item_sku"
    line_item_total = "line_item_total"
    timestamp = "timestamp"


column_names = {
    "customer_name": "customer",
    "item_sku": "item",
    "line_item_total": "gold",
    "timestamp": "timestamp",
}


class search_order(BaseModel):
    preview: str
    next: str


class Result(BaseModel):
    line_item_id: int
    item_sku: str
    customer_name: str
    line_item_total: int
    timestamp: str


class SearchOrder(BaseModel):
    previous: str
    next: str
    results: list[Result]


@router.get("/search/", tags=["search"])
def search_orders(
    customer_name: str = "",
    potion_sku: str = "",
    search_page: str = "1",
    sort_col: search_sort_options = search_sort_options.timestamp,
    sort_order: Literal["asc", "desc"] = "desc",
):
    """
    Search for cart line items by customer name and/or potion sku.

    Customer name and potion sku filter to orders that contain the
    string (case insensitive). If the filters aren't provided, no
    filtering occurs on the respective search term.

    Search page is a cursor for pagination. The response to this
    search endpoint will return previous or next if there is a
    previous or next page of results available. The token passed
    in that search response can be passed in the next search request
    as search page to get that page of results.

    Sort col is which column to sort by and sort order is the direction
    of the search. They default to searching by timestamp of the order
    in descending order.

    The response itself contains a previous and next page token (if
    such pages exist) and the results as an array of line items. Each
    line item contains the line item id (must be unique), item sku,
    customer name, line item total (in gold), and timestamp of the order.
    Your results must be paginated, the max results you can return at any
    time is 5 total line items.
    """

    search_result = utils.search_orders(
        int(search_page),
        customer_name,
        potion_sku,
        column_names[sort_col],
        sort_order.upper(),
    )

    previous_page = int(search_page) - 1
    previous_page = "" if previous_page == 0 else previous_page

    next_page = int(search_page) + 1
    next_page = next_page if search_result.has_next_page else ""

    return SearchOrder(
        previous=str(previous_page),
        next=str(next_page),
        results=[
            Result(
                line_item_id=result.id,
                item_sku=f"{result.item} ({result.quantity}x)",
                customer_name=result.customer,
                line_item_total=result.gold,
                timestamp=result.time.isoformat(),
            )
            for result in search_result.orders
        ],
    )


@router.post("/visits/{visit_id}")
def post_visits(visit_id: int, customers: list[Customer]):
    """
    Which customers visited the shop today?
    """
    print(f"List of customers who visited the shop: {customers}")

    utils.set_customers(customers)

    utils.set_visits(customers)

    return "OK"


@router.post("/")
def create_cart(customer: Customer):
    """ """
    cart_id = utils.get_recent_visit(customer)

    print(f"New cart created with id {cart_id}. Customer: {customer.dict()}")
    return {"cart_id": cart_id}


class CartItem(BaseModel):
    quantity: int


@router.post("/{cart_id}/items/{item_sku}")
def set_item_quantity(cart_id: int, item_sku: str, cart_item: CartItem):
    """ """
    utils.add_to_cart(cart_id, item_sku, cart_item.quantity)

    print(f"Item {item_sku} (x{cart_item.quantity}) added to cart {cart_id}")

    return "OK"


class CartCheckout(BaseModel):
    payment: str


@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):
    """ """
    print(f"Checkout for cart {cart_id}: {cart_checkout.dict()}")

    result = utils.checkout_cart(cart_id)

    return {"total_potions_bought": result.potions, "total_gold_paid": result.gold}
