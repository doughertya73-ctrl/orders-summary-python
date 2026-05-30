def get_orders_summary(*, data, from_, to, group_by, min_amount=None):
    raise NotImplementedError("Not implemented")
def get_orders_summary(*, data, from_, to, group_by, min_amount=None):
    groups = {}

    for order in data:
        order_date = order["orderDate"]

        # Date filter (inclusive)
        if not (from_ <= order_date <= to):
            continue

        amount = sum(
            item["quantity"] * item["unitPrice"]
            for item in order["items"]
        )

        # Optional minimum amount filter
        if min_amount is not None and amount < min_amount:
            continue

        if group_by == "day":
            key = order_date
        elif group_by == "customer":
            key = order["customerId"]
        else:
            raise ValueError("group_by must be 'day' or 'customer'")

        if key not in groups:
            groups[key] = {
                "count": 0,
                "totalAmount": 0,
            }

        groups[key]["count"] += 1
        groups[key]["totalAmount"] += amount

    result = []

    for key in sorted(groups):
        count = groups[key]["count"]
        total = groups[key]["totalAmount"]

        result.append(
            {
                "key": key,
                "count": count,
                "totalAmount": total,
                "avgAmount": total / count,
            }
        )

    return result
