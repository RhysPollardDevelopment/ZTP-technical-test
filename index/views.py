from django.shortcuts import render
from pyexcel_xlsx import get_data


class Customer(object):
    def __init__(self, object):
        self.name = None
        self.address = None
        self.meter_number = None
        self.rates = {}
        self.__set_customer_details(object)

    def __set_customer_details(self, object):
        for field in object:
            if field == []:
                continue
            elif field[0] == "Customer Name":
                self.name = field[1]
            elif field[0] == "Customer Address":
                self.address = field[1]
            elif field[0] == "Meter Number":
                self.meter_number = field[1]
            elif field[0] == "Rate Name":
                continue
            else:
                self.rates[field[0]] = [field[1], field[2]]


def index(request):
    data = get_data("EnergyConsumptionDetail_updated(1470).xlsx")

    keys = data.keys()

    customer_sheets = [cust for cust in keys if "Customer" in cust]

    rate_prices = data["Rate Price"]

    energy_rates = []
    for rate in rate_prices:
        if rate[0] == "Rate Name":
            continue
        else:
            energy_rates.append(rate[0])

    customers = []
    for sheet_name in customer_sheets:
        sheet_data = data[sheet_name]
        customer = Customer(sheet_data)
        customers.append(customer)
        print(customer.rates)

    context = {
        "customers": customers,
        "energy_rates": energy_rates,
    }
    template = "index/customers.html"
    return render(request, template, context)
