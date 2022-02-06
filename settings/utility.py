def _convert(data):
    return [item[0] for item in data]

def total_coast(quantity, price):

    order_total_coast = 0

    for ind, itm in enumerate(price):
        order_total_coast += quantity[ind]*price[ind]

        return order_total_coast

def total_quantity(quantity):
    order_total_quantity = 0
    for itm in quantity:
        order_total_quantity += itm

        return order_total_quantity

def get_total_coast(DB):
    all_product_id = DB.select_all_products_id()
    all_price = [DB.select_single_product_price(itm) for itm in all_product_id]
    all_quantity = [DB.select_single_product_quantity(itm) for itm in all_product_id]
    return total_coast(all_quantity, all_price)

def get_total_quantity(DB):
    all_product_id = DB.select_all_products_id()
    all_quantity = [DB.select_single_product_quantity(itm) for itm in all_product_id]
    return total_quantity(all_quantity)
