from django.shortcuts import render
from pyexcel_xlsx import get_data


class Customer(object):
    def __init__(self, object):
        self.name = None
        self.address = None
        self.meter_number = None
        self.rates = {}
        self.total = 0
        self.day_rate = 0
        self.night_rate = 0
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

    # Variables for cost calculations
    total_cost = None
    day_rate = None
    night_rate = None

    data = get_data("EnergyConsumptionDetail_updated(1470).xlsx")

    keys = data.keys()

    customer_sheets = [cust for cust in keys if "Customer" in cust]

    rate_prices = data["Rate Price"]

    rate_types = []
    for rate in rate_prices:
        if rate[0] == "Rate Name":
            continue
        else:
            rate_types.append(rate[0])

    customers = []
    for sheet_name in customer_sheets:
        sheet_data = data[sheet_name]
        customer = Customer(sheet_data)
        customers.append(customer)

    if request.method == "POST":
        energy_rates = {}
        for cost in rate_prices:
            if cost[0] == "Rate Name":
                continue
            else:
                energy_rates[cost[0]] = cost[1]

        highest_total = 0
        highest_day = 0
        highest_night = 0

        for customer in customers:
            rates = customer.rates.keys()

            for rate in rates:
                if rate in energy_rates:
                    length = len(customer.rates[rate])
                    usage = (
                        customer.rates[rate][length - 1]
                        - customer.rates[rate][0]
                    )
                    cost = usage * energy_rates[rate]
                    if rate == "Day Rate":
                        customer.day_rate = cost
                    elif rate == "Night Rate":
                        customer.night_rate = cost
                    customer.total += cost

            if customer.total > highest_total:
                highest_total = customer.total
                total_cost = customer

            if customer.day_rate > highest_day:
                highest_day = customer.day_rate
                day_rate = customer

            if customer.night_rate > highest_night:
                highest_night = customer.night_rate
                night_rate = customer

    context = {
        "customers": customers,
        "rate_types": rate_types,
        "total_cost": total_cost,
        "day_rate": day_rate,
        "night_rate": night_rate,
    }
    template = "index/customers.html"
    return render(request, template, context)
