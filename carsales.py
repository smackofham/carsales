""" Pulls car data from carsales.com.au. """

from bs4scrape import BsScrape
from cars import IndividualCar
from excel import convert_data_to_excel_readable, write_data

url = str(input('Please paste the url of the search page.'))
# url = 'https://www.carsales.com.au/cars/toyota/corolla/victoria-state/under-5000/?area=Stock&vertical=car&WT.z_srchsrcx=makemodel'

print('The url is: ' + url)


def main_loop():
    current_search = BsScrape(url)
    no_pages_to_search = current_search.calculate_no_pages()
    total_cars_found = 0
    car_list = []
    # Debugging
    # print(no_pages_to_search)

    for i in range(no_pages_to_search):
        # 12 cars per page.
        for j in range(12):
            # Try and except block due to the last page throwing index
            # IndexError if there are less than 12 cars.
            try:
                searched_car = IndividualCar(current_search.car_list_data)
                searched_car.pull_data(j)
                convert_data_to_excel_readable(car_list, searched_car)
                total_cars_found += 1
                # searched_car.print_stats()
                # print(car_list)
                # print(total_cars_found)
            except IndexError:
                # print('IndexError')
                pass
        # Stops the function from searching for the next page when it is on the last page to be searched.
        if i < no_pages_to_search - 1:
            current_search = BsScrape(current_search.next_page())
        else:
            pass
    write_data('car.name', car_list)
    print('Total number of cars found: ' + str(total_cars_found))
    # print(car_list)


main_loop()
