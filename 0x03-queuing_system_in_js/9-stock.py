import asyncio
from functools import wraps

import redis
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
client = redis.Redis()

# Data: List of products
list_products = [
    {
        "itemId": 1,
        "itemName": "Suitcase 250",
        "price": 50,
        "initialAvailableQuantity": 4,
    },
    {
        "itemId": 2,
        "itemName": "Suitcase 450",
        "price": 100,
        "initialAvailableQuantity": 10,
    },
    {
        "itemId": 3,
        "itemName": "Suitcase 650",
        "price": 350,
        "initialAvailableQuantity": 2,
    },
    {
        "itemId": 4,
        "itemName": "Suitcase 1050",
        "price": 550,
        "initialAvailableQuantity": 5,
    },
]


def get_item_by_id(item_id):
    """
    Retrieve a product by its ID.

    Args:
        item_id (int): The ID of the product.

    Returns:
        dict: The product with the given ID, or None if not found.
    """
    return next(
        (item for item in list_products if item["itemId"] == item_id),
        None
    )


def async_redis(method):
    """
    Decorator to run a Redis method asynchronously.

    Args:
        method (function): The Redis method to run asynchronously.

    Returns:
        function: The wrapped asynchronous function.
    """

    @wraps(method)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, method, *args, **kwargs)

    return wrapper


@async_redis
def reserve_stock_by_id(item_id, stock):
    """
    Reserve stock for a product by its ID.

    Args:
        item_id (int): The ID of the product.
        stock (int): The stock to reserve.
    """
    client.set(f"item.{item_id}", stock)


@async_redis
def get_current_reserved_stock_by_id(item_id):
    """
    Get the current reserved stock for a product by its ID.

    Args:
        item_id (int): The ID of the product.

    Returns:
        int: The current reserved stock.
    """
    stock = client.get(f"item.{item_id}")
    return int(stock) if stock else 0


@app.route("/list_products", methods=["GET"])
def list_products_route():
    """
    List all products.

    Returns:
        Response: JSON response containing the list of all products.
    """
    return jsonify(list_products)


@app.route("/list_products/<int:item_id>", methods=["GET"])
async def get_product_route(item_id):
    """
    Get product details including current stock.

    Args:
        item_id (int): The ID of the product.

    Returns:
        Response: JSON response containing the product details
        and current stock.
    """
    product_item = get_item_by_id(item_id)
    if not product_item:
        return jsonify({"status": "Product not found"}), 404

    try:
        reserved_stock = await get_current_reserved_stock_by_id(item_id)
        current_quantity = product_item["initialAvailableQuantity"] - \
            reserved_stock
        return jsonify({**product_item, "currentQuantity": current_quantity})
    except Exception:
        return jsonify({"status": "Internal Server Error"}), 500


@app.route("/reserve_product/<int:item_id>", methods=["GET"])
async def reserve_product_route(item_id):
    """
    Reserve a product.

    Args:
        item_id (int): The ID of the product.

    Returns:
        Response: JSON response containing the reservation status.
    """
    product_item = get_item_by_id(item_id)
    if not product_item:
        return jsonify({"status": "Product not found"}), 404

    try:
        reserved_stock = await get_current_reserved_stock_by_id(item_id)
        if reserved_stock >= product_item["initialAvailableQuantity"]:
            return jsonify(
                {"status": "Not enough stock available", "itemId": item_id}
            )

        await reserve_stock_by_id(item_id, reserved_stock + 1)
        return jsonify({"status": "Reservation confirmed", "itemId": item_id})
    except Exception:
        return jsonify({"status": "Internal Server Error"}), 500


async def reset_products_stock():
    """
    Reset the stock for all products in Redis.
    """
    await asyncio.gather(
        *(reserve_stock_by_id(item["itemId"], 0) for item in list_products)
    )


if __name__ == "__main__":
    asyncio.run(reset_products_stock())
    app.run(host="0.0.0.0", port=1245)
