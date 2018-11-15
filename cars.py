import re


class Cars:

    def __init__(self, car_list_data):
        """ Gets the raw html elements for each car feature.
        car_list_data is the bs4 text. """
        self.car_list_data = car_list_data
        # Car title and year
        self.summary = car_list_data.select('div a h2')
        # Odometer reading, body type, transmission, engine
        self.features = car_list_data.select('div.feature-text')
        # Price in AUD
        self.prices = car_list_data.select('a.price-container div.price')


class IndividualCar(Cars):
    """ To add new properties, have to add them in the following places:
    __init__, pull_data() and in convert_data_to_excel_readable() in the excel.py file
    Also need to add a function that defines it (e.g. def car_numberplate). """
    def __init__(self, car_list_data):
        super().__init__(car_list_data)
        self.name = ''
        self.odometer = 0
        self.body = 0
        self.transmission = 0
        self.engine = 0
        self.price = 0
        self.year = 0
        self.url = 0

    def car_url(self, i):
        self.url = self.car_list_data.select('div.action-buttons.n_align-right.n_width-min a')[i].get('href')
        self.url = 'https://www.carsales.com.au' + self.url

    def car_year(self, i):
        self.year = str(self.summary[i].getText()[0:4])
        if 'Manufacturer Marketing Year' in self.name:
            wordlist = re.sub("[^\w]", " ", self.name).split()
            self.year = str(wordlist[0])

    def car_name(self, i):
        # i is a value decided by a previous function that loops to get all the car names
        self.name = str(self.summary[i].getText()[5:])
        if 'Manufacturer Marketing Year' in self.name:
            # Splits the whole name into a list for manipulation.
            wordlist = re.sub("[^\w]", " ", self.name).split()
            self.name = str(wordlist[1] + ' '
                            + wordlist[2] + ' ' + wordlist[3] + ' '
                            + wordlist[4] + ' ')
            self.year = str(wordlist[0])
        # Finds the weird naming for certain cars and removes it.

    def car_odometer(self, n):
        # Need to state n in previous function.
        # Multiply by 4 to get the location of the element.
        odometer_base = str(self.features[4*n].getText())
        car_odo_wordlist = re.sub("[^\w]", " ", odometer_base).split()
        self.odometer = str(car_odo_wordlist[0])

    def car_body(self, i):
        self.body = str(self.features[4 * i + 1].getText())

    def car_transmission(self, n):
        self.transmission = str(self.features[4 * n + 2].getText())

    def car_engine(self, n):
        self.engine = str(self.features[4 * n + 3].getText())

    def car_price(self, n):
        self.price = str(self.prices[n].getText())

    def pull_data(self, n):
        """ Pulls all the data using one method.
        n is there to iterate through the 12 different cars on each page. """
        self.car_year(n)
        self.car_name(n)
        self.car_odometer(n)
        self.car_body(n)
        self.car_transmission(n)
        self.car_engine(n)
        self.car_price(n)
        self.car_url(n)

    def print_stats(self):
        print(self.name, self.odometer, self.body, self.transmission,
              self.engine, self.price)

