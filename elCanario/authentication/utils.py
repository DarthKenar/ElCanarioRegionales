from django.utils import timezone

def get_today_date_all():
    hoy = timezone.localtime()
    day = hoy.day
    month = hoy.month
    year = hoy.year
    return day, month, year