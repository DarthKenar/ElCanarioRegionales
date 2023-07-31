from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import requests
from .models import DollarGraph
from django.utils import timezone

def get_date_all():
    hoy = timezone.localtime()
    ayer = hoy - timezone.timedelta(days=1)
    day = ayer.day
    month = ayer.month
    year = ayer.year
    return day, month, year
def two_digits_minimum(num):
    return f"{num:02d}"
def get_dollar_price():
        print("initiating dollar price collection")
        print("...")
        print("configuring datetime")
        day, month, year = get_date_all()
        print("...")
        print("complete get datetime")
        # data_colection = requests.get(f"https://cont.certisend.com/web/container/api/v1/fintech/ar/bcra/dolar_value?token-susc=eaab7d36d5beb13a7df97cfa86ace7d1&token-api=1861e7f558a07d91d23895dbec81c0c8&date=25%2F01%2F2021&")
        data_colection = requests.get(f"https://cont.certisend.com/web/container/api/v1/fintech/ar/bcra/dolar_value?token-susc=a4cb455dbdfadc51cddc8edd5602d828&token-api=14c79fd8ca3ebe7c03dbcb3d013a2705&date={day}%2F{two_digits_minimum(month)}%2F{year}&")
        print(data_colection)
        print("...")
        data_colection = data_colection.json()
        print(data_colection)
        print("...")
        dollar_price = data_colection['data'][0]['bancos'][1]['mostrador_11hs_vende']
        print(dollar_price)
        print(type(dollar_price))
        dollar_price = dollar_price.replace(",",".")
        print(dollar_price)
        print(type(dollar_price))
        dollar_price = float(dollar_price)
        print(dollar_price)
        print(type(dollar_price))
        print("...")
        dollar = DollarGraph(price = dollar_price)
        dollar.save()
        print("dollar price correctly saved")

scheduler = BackgroundScheduler()
print("scheduler = BackgroundScheduler()")
scheduler.add_job(get_dollar_price, trigger=IntervalTrigger(hours=24))
print("scheduler.add_job(get_dollar_price, trigger=IntervalTrigger(hours=24))")
scheduler.start()
print("scheduler.start()")