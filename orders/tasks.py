from orders.models import Order
from store.celery import app


@app.task
def check_card_number(card_number, order_id):
    order = Order.objects.get(pk=order_id)
    if int(card_number.replace(" ", "")) % 2 == 0 and not card_number.endswith("0"):
        order.status = "paid"
        order.is_paid = True
        order.save()
    else:
        order.status = "unpaid"
        order.save()
