from api.bus import BusAPI
import questionary
import inquirer
from ui.main import UI


class Controller:
    def __init__(self):
        self.bus_api = BusAPI()
        self.ui = UI()

    def init_place(self):
        place = None

        while place is None:
            place_str = questionary.text("Nhập điểm dừng : ").ask()
            places_dict = self.bus_api.search_place(place_str)

            if len(places_dict) == 1:
                place = list(places_dict.values())[0]

            elif len(places_dict) > 1:
                questions = [
                    inquirer.List(
                        "place",
                        message="Chọn 1 trong những địa điểm sau đây?",
                        choices=places_dict.keys(),
                    )
                ]
                answer = inquirer.prompt(questions)
                place = places_dict[answer["place"]]

            else:
                print("Không thể tìm kiếm địa điểm bạn vừa nhập! Vui lòng thử lại.")

        addr = self.bus_api.get_place_address(place)
        place["Geo"]["Add"] = addr
        return place

    def display(self, place):
        buses = self.bus_api.get_buses_of_place(place["ObjectID"])

        def get_update_data_func():
            return self.bus_api.get_buses_of_place(place["ObjectID"])

        self.ui.render(place, buses, get_update_data_func)


if __name__ == "__main__":
    controller = Controller()
    place = controller.init_place()
    controller.display(place)
