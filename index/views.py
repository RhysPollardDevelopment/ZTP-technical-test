from django.shortcuts import render
from pyexcel_xlsx import get_data


class Customer(object):
    """
    A customer builder object used to created the information for each
    customer and hold their key details for assessing totals of rates.
    """

    def __init__(self, object):
        """
        Sets data to base level and uses private class to assign excel data
        to properties.
        """
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
            # Used to ignore empty cells.
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

    # Variables for cost calculations to be sent to front end.
    total_cost = None
    day_rate = None
    night_rate = None

    # Data is collected and used to check for any number of customer sheets.
    data = get_data("EnergyConsumptionDetail_updated(1470).xlsx")

    keys = data.keys()

    customer_sheets = [cust for cust in keys if "Customer" in cust]

    # Rate names and prices organised to allow responsive html generation.
    rate_prices = data["Rate Price"]

    rate_types = []
    for rate in rate_prices:
        if rate[0] == "Rate Name":
            continue
        else:
            rate_types.append(rate[0])

    # Customers created using sheet data from excel.
    customers = []
    for sheet_name in customer_sheets:
        sheet_data = data[sheet_name]
        customer = Customer(sheet_data)
        customers.append(customer)

    # If form is posted, organises calculations for total cost, day and night
    # rates.
    if request.method == "POST":
        energy_rates = {}
        for cost in rate_prices:
            if cost[0] == "Rate Name":
                continue
            else:
                energy_rates[cost[0]] = cost[1]

        # Variables to tally highest result against subsequent customers.
        highest_total = 0
        highest_day = 0
        highest_night = 0

        for customer in customers:
            rates = customer.rates.keys()

            # Uses the rate name to find the correct key in rates dict.
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

            # Each sections checks if higher than total, if so it assigns
            # value to variable and stores/updates with correct customer.
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
