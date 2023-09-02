from store.celery import app
import time


@app.task
def check_card_number(card_number: int):
    time.sleep(3)
    if card_number % 2 == 0 and not str(card_number).endswith('0'):
        return 'ok'
    else:
        return 'error'
