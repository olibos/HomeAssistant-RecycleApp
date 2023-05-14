from array import array
from datetime import date, datetime, timedelta
from typing import Dict, List, Tuple
from requests import Session
import re

from custom_components.recycle_app.const import COLLECTION_TYPES

_secret: str = ""
_accessToken: str = ""


class FostPlusApi:
    __session: Session = None
    __endpoint: str

    def __ensure_initialization(self):
        if (self.__session): return

        self.__session = Session()
        self.__session.headers.update(
            {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "HomeAssistant-RecycleApp",
                "x-consumer": "recycleapp.be"
            })

        base_url = self.__session.get("https://recycleapp.be/config/app.settings.json").json()["API"]
        self.__endpoint = f"{base_url}/app/v1"

    def __get_secret(self) -> str:
        self.__ensure_initialization()
        html = self.__session.get("https://www.recycleapp.be/").text
        script_url = next(re.finditer(
            r"src=\"([^\"]+main\.[^\"]+\.js)\"", html)).group(1)
        script = self.__session.get("https://www.recycleapp.be/" + script_url).text
        return next(re.finditer(r"\"(\w{200,})\"", script)).group(1)

    def __get_access_token(self) -> str:
        self.__ensure_initialization()
        for _ in range(2):
            response = self.__session.get(
                f"{self.__endpoint}/access-token", headers={"x-secret": self.secret})
            if response.status_code == 200:
                return response.json()["accessToken"]
            if response.status_code == 401:
                global _secret
                _secret = None

    @property
    def secret(self) -> str:
        global _secret
        if (not _secret):
            _secret = self.__get_secret()
        return _secret

    @property
    def access_token(self) -> str:
        global _accessToken
        if (not _accessToken):
            _accessToken = self.__get_access_token()

        return _accessToken

    def __post(self, action: str, data=None):
        self.__ensure_initialization()
        for _ in range(2):
            headers = {"Authorization": self.access_token}
            response = self.__session.post(
                f"{self.__endpoint}/{action}", json=data, headers=headers)
            if response.status_code == 200:
                return response.json()

            if response.status_code == 401:
                global _accessToken
                _accessToken = None

    def __get(self, action: str):
        self.__ensure_initialization()
        for _ in range(2):
            headers = {"Authorization": self.access_token}
            response = self.__session.get(
                f"{self.__endpoint}/{action}", headers=headers)
            if response.status_code == 200:
                return response.json()

            if response.status_code == 401:
                global _accessToken
                _accessToken = None

    def get_zip_code(self, zip_code: int, language: str = "fr") -> tuple[str, str]:
        result = self.__get(f"zipcodes?q={zip_code}")
        if result["total"] != 1:
            raise FostPlusApiException("invalid_zipcode")
        item = result["items"][0]
        return (item["id"], f'{item["code"]} - {item["names"][0][language]}')

    def get_street(self, street: str, zip_code_id: str, language: str = "fr") -> tuple[str, str]:
        street = street.strip().lower()
        result = self.__post(f"streets?q={street}&zipcodes={zip_code_id}")
        if result["total"] != 1:
            item = next((i for i in result["items"] if i["names"][language].strip().lower() == street), None)
            if (not item):
                raise FostPlusApiException("invalid_streetname")
            return (item["id"], item["names"][language])

        return (result["items"][0]["id"], result["items"][0]["names"][language])

    def get_fractions(self, zip_code_id: str, street_id: str, house_number: int, language: str, size: int = 100) -> Dict[str, Tuple[str, str]]:
        this_year = datetime.now().year
        items = []
        page = 1
        while True:
            response = self.__get(f'collections?zipcodeId={zip_code_id}&streetId={street_id}&houseNumber={house_number}&fromDate={this_year}-01-01&untilDate={this_year}-12-31&page={page}&size={size}')
            items += response["items"]
            page += 1
            if page > response["pages"]:
                break
        return {f["fraction"]["logo"]["id"]: (f["fraction"]["color"], f["fraction"]["name"][language]) for f in items if "logo" in f["fraction"] and f["fraction"]["logo"]["id"] in COLLECTION_TYPES}

    def get_collections(self, zip_code_id: str, street_id: str, house_number: int, from_date: date = None, until_date: date = None, size=100) -> dict[str, date]:
        if (not from_date):
            from_date = datetime.now()
        if (not until_date):
            until_date = from_date + timedelta(weeks=8)
        result = {}
        EMPTY_DICT = {}
        collections: array[dict] = self.__get(
            f'collections?zipcodeId={zip_code_id}&streetId={street_id}&houseNumber={house_number}&fromDate={from_date.strftime("%Y-%m-%d")}&untilDate={until_date.strftime("%Y-%m-%d")}&size={size}')["items"]
        for item in collections:
            if item.get("exception", EMPTY_DICT).get("replacedBy", None):
                continue
            fraction_id = item.get("fraction", EMPTY_DICT).get(
                "logo", EMPTY_DICT).get("id", None)
            if fraction_id not in COLLECTION_TYPES:
                continue
            parts = item.get(
                "timestamp", "2999-12-31T").split('T')[0].split('-')
            collection_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
            current_date = result.get(fraction_id, date.max)
            if collection_date < current_date:
                result[fraction_id] = collection_date

        return result


class FostPlusApiException(Exception):
    def __init__(self, code: str) -> None:
        self.__code = code

    @property
    def code(self) -> str:
        return self.__code
