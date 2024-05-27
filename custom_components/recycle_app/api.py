"""FostPlus API."""
from array import array
from collections import defaultdict
from datetime import date, datetime, timedelta
import re
from typing import Optional

from .const import COLLECTION_TYPES
from requests import Session


class FostPlusApi:
    __session: Optional[Session] = None
    __endpoint: str
    __secret: Optional[str] = None
    __access_token: Optional[str] = None

    def initialize(self) -> None:
        self.__ensure_initialization()

    def __ensure_initialization(self):
        if self.__session:
            return

        self.__session = Session()
        self.__session.headers.update(
            {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "HomeAssistant-RecycleApp",
                "x-consumer": "recycleapp.be",
            }
        )

        base_url = self.__session.get(
            "https://www.recycleapp.be/config/app.settings.json"
        ).json()["API"]
        self.__endpoint = f"{base_url}/app/v1"

    def __get_secret(self) -> str:
        self.__ensure_initialization()
        html = self.__session.get("https://www.recycleapp.be/").text
        script_url = next(
            re.finditer(
                r"src=\"([a-zA-Z0-9/_-]{1,50}main\.[a-f0-9]{8}\.chunk\.js)\"", html
            )
        ).group(1)
        script = self.__session.get("https://www.recycleapp.be/" + script_url).text
        return next(re.finditer(r"\"(\w{200,})\"", script)).group(1)

    def __get_access_token(self) -> str:
        self.__ensure_initialization()
        for _ in range(2):
            response = self.__session.get(
                f"{self.__endpoint}/access-token", headers={"x-secret": self.secret}
            )
            if response.status_code == 200:
                return response.json()["accessToken"]
            if response.status_code == 401:
                FostPlusApi.__secret = None

    @property
    def secret(self) -> str:
        if not FostPlusApi.__secret:
            FostPlusApi.__secret = self.__get_secret()
        return FostPlusApi.__secret

    @property
    def access_token(self) -> str:
        if not FostPlusApi.__access_token:
            FostPlusApi.__access_token = self.__get_access_token()

        return FostPlusApi.__access_token

    def __post(self, action: str, data=None):
        self.__ensure_initialization()
        for _ in range(2):
            headers = {"Authorization": self.access_token}
            response = self.__session.post(
                f"{self.__endpoint}/{action}", json=data, headers=headers
            )
            if response.status_code == 200:
                return response.json()

            if response.status_code == 401:
                FostPlusApi.__access_token = None

    def __get(self, action: str):
        self.__ensure_initialization()
        for _ in range(2):
            headers = {"Authorization": self.access_token}
            response = self.__session.get(
                f"{self.__endpoint}/{action}", headers=headers
            )
            if response.status_code == 200:
                return response.json()

            if response.status_code == 401:
                FostPlusApi.__access_token = None

    def get_zip_code(self, zip_code: int, language: str = "fr") -> tuple[str, str]:
        result = self.__get(f"zipcodes?q={zip_code}")
        if result["total"] != 1:
            raise FostPlusApiException("invalid_zipcode")
        item = result["items"][0]
        return (item["id"], f'{item["code"]} - {item["names"][0][language]}')

    def get_street(
        self, street: str, zip_code_id: str, language: str = "fr"
    ) -> tuple[str, str]:
        street = street.strip().lower()
        result = self.__post(f"streets?q={street}&zipcodes={zip_code_id}")
        if result["total"] != 1:
            item = next(
                (
                    i
                    for i in result["items"]
                    if i["names"][language].strip().lower() == street
                ),
                None,
            )
            if not item:
                raise FostPlusApiException("invalid_streetname")
            return (item["id"], item["names"][language])

        return (result["items"][0]["id"], result["items"][0]["names"][language])

    def get_recycling_parks(self, zip_code_id: str, language: str):
        result = {}
        response: dict[str, list[dict]] = self.__get(
            f"collection-points/recycling-parks?zipcode={zip_code_id}&size=100&language={language}"
        )

        for item in response.get("items", []):
            result[item.get("id")] = {
                "name": item["displayName"][language],
                "exceptions": item["exceptionDays"],
                "periods": item["openingPeriods"],
            }
        return result

    def get_fractions(
        self,
        zip_code_id: str,
        street_id: str,
        house_number: int,
        language: str,
        size: int = 100,
    ) -> dict[str, tuple[str, str]]:
        this_year = datetime.now().year
        items = []
        page = 1
        while True:
            response = self.__get(
                f"collections?zipcodeId={zip_code_id}&streetId={street_id}&houseNumber={house_number}&fromDate={this_year}-01-01&untilDate={this_year}-12-31&page={page}&size={size}"
            )
            items += response["items"]
            page += 1
            if page > response["pages"]:
                break
        return {
            f["fraction"]["logo"]["id"]: (
                f["fraction"]["color"],
                f["fraction"]["name"][language],
            )
            for f in items
            if "logo" in f["fraction"]
            and f["fraction"]["logo"]["id"] in COLLECTION_TYPES
        }

    def get_collections(
        self,
        zip_code_id: str,
        street_id: str,
        house_number: int,
        from_date: date = None,
        until_date: date = None,
        size=100,
    ) -> dict[str, list[date]]:
        if not from_date:
            from_date = datetime.now()
        if not until_date:
            until_date = from_date + timedelta(weeks=8)
        result: dict[str, list[date]] = defaultdict(list)
        EMPTY_DICT = {}
        collections: array[dict] = self.__get(
            f'collections?zipcodeId={zip_code_id}&streetId={street_id}&houseNumber={house_number}&fromDate={from_date.strftime("%Y-%m-%d")}&untilDate={until_date.strftime("%Y-%m-%d")}&size={size}'
        )["items"]
        for item in collections:
            if item.get("exception", EMPTY_DICT).get("replacedBy", None):
                continue

            fraction_id = (
                item.get("fraction", EMPTY_DICT).get("logo", EMPTY_DICT).get("id", None)
            )

            if fraction_id not in COLLECTION_TYPES:
                continue

            parts = item.get("timestamp", "").split("T")[0].split("-")
            if not parts[0]:
                continue

            collection_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
            fraction = result[fraction_id]
            if collection_date not in fraction:
                fraction.append(collection_date)

        return result


class FostPlusApiException(Exception):
    def __init__(self, code: str) -> None:
        self.__code = code

    @property
    def code(self) -> str:
        return self.__code
