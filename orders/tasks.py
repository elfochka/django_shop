from store.celery import app
from django.shortcuts import redirect


@app.task
def check_card_number(card_number):
    if int(card_number.replace(" ", "")) % 2 == 0 and not card_number.endswith('0'):
        return redirect("orders:cart")
    else:
        return redirect("orders:cart")
