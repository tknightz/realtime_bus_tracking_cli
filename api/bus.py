import requests
from urllib.parse import urlencode


class BusAPI:
    def __init__(self):
        self.requester = requests.Session()

        self.headers = {
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://timbus.vn",
            "Referer": "http://timbus.vn/",
            "Accept-Language": "en-US, en;q=0.9",
        }

        self.path = {
            "act": "route",
            "slng": 0,
            "slat": 0,
            "sadd": "",
            "elng": 0,
            "elat": 0,
            "eadd": "",
            "opts": 2,
        }

        # Get cookies before making any requests
        self.preload()

    def preload(self):
        self.requester.get("http://timbus.vn")
        self.headers[
            "Cookie"
        ] = f'ASP.NET_SessionId={self.requester.cookies.get("ASP.NET_SessionId")}'

    # Interface for making request.
    def send_request(self, method, endpoint, data):
        return self.requester.request(
            method, endpoint, headers=self.headers, data=data
        ).json()

    def search_place(self, place_name):
        endpoint = "http://timbus.vn/Engine/Business/Search/action.ashx"
        data = f"act=searchfull&typ=2&key={place_name.replace(' ', '+')}"
        response = self.send_request("post", endpoint, data)
        places = response["dt"]["Data"]
        return {place["Name"]: place for place in places}

    def get_place_address(self, place):
        lng = place["Geo"]["Lng"]
        lat = place["Geo"]["Lat"]

        endpoint = "http://timbus.vn/Engine/Business/Route/action.ashx"
        data = f"act=geo2add&lng={lng}&lat={lat}"
        response = self.send_request("post", endpoint, data)

        return response["dt"]["Address"]

    def get_buses_of_place(self, place_id):
        endpoint = "http://timbus.vn/Engine/Business/Vehicle/action.ashx"
        data = f"act=partremained&State=false&StationID={place_id}&FleetOver="
        response = self.send_request("post", endpoint, data)
        return response["dt"]

    def find_path(self, start_place, end_place):
        path_data = {
            "act": "route",
            "slng": start_place["Geo"]["Lng"],
            "slat": start_place["Geo"]["Lat"],
            "sadd": start_place["Geo"]["Add"],
            "elng": end_place["Geo"]["Lng"],
            "elat": end_place["Geo"]["Lat"],
            "eadd": end_place["Geo"]["Add"],
            "opts": 2,
        }

        endpoint = "http://timbus.vn/Engine/Business/Route/action.ashx"
        data = urlencode(path_data)
        return self.send_request("post", endpoint, data=data)
