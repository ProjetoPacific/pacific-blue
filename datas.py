#calculadora de datas

from datetime import date, datetime


def hoje():
    return date.today().strftime("%d/%m/%Y")


def dias_desde(data_texto):
    data = datetime.strptime(data_texto, "%d/%m/%Y").date()
    return (date.today() - data).days
