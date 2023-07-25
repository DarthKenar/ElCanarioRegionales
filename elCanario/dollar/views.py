from django.shortcuts import render
from django_cron import CronJobBase, Schedule
import requests
from django.utils import timezone
from .models import DollarGraph

# Create your views here.
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # 120 = every 2 hours
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'dollar.MyCronJob'     # a unique code

    
    def do(self):
        print("AAAAAAAAAAAAAAAAALUCIALUCIALUCIAAAAAAAAAAAAAAAAAAA")
    def get_uds_sell_price_from_bna(self):
        print("-------------Cron Task-------------")
        # data_colection = requests.get("https://cont.certisend.com/web/container/api/v1/fintech/ar/bcra/dolar_value?token-susc=eaab7d36d5beb13a7df97cfa86ace7d1&token-api=1861e7f558a07d91d23895dbec81c0c8&date=18%2F07%2F2023")
        # data_colection = data_colection.json()
        # data_colection = data_colection['data'][0]['bancos'][1]['mostrador_11hs_vende']
        # dolar_price = DollarGraph(dolar_price=data_colection)
    