from array import array
from datetime import date, datetime, timedelta
from typing import Dict, List, Tuple
from requests import Session
import re

from custom_components.recycle_app.const import COLLECTION_TYPES

_secret: str = "8eTFgy3AQH0mzAcj3xMwaKnNyNnijEFIEegjgNpBHifqtQ4IEyWqmJGFz3ggKQ7B4vwUYS8xz8KwACZihCmboGb6brtVB3rpne2Ww5uUM2n3i4SKNUg6Vp7lhAS8INDUNH8Ll7WPhWRsQOXBCjVz5H8fr0q6fqZCosXdndbNeiNy73FqJBn794qKuUAPTFj8CuAbwI6Wom98g72Px1MPRYHwyrlHUbCijmDmA2zoWikn34LNTUZPd7kS0uuFkibkLxCc1PeOVYVHeh1xVxxwGBsMINWJEUiIBqZt9VybcHpUJTYzureqfund1aeJvmsUjwyOMhLSxj9MLQ07iTbvzQa6vbJdC0hTsqTlndccBRm9lkxzNpzJBPw8VpYSyS3AhaR2U1n4COZaJyFfUQ3LUBzdj5gV8QGVGCHMlvGJM0ThnRKENSWZLVZoHHeCBOkfgzp0xl0qnDtR8eJF0vLkFiKwjX7DImGoA8IjqOYygV3W9i9rIOfK"
_accessToken: str = None


class FostPlusApi:
    __session: Session
    __endpoint: str

    def __init__(self) -> None:
        self.__session = Session()
        self.__session.headers.update(
            {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "HomeAssistant-RecycleApp",
                "x-consumer": "recycleapp.be"
            })
        self.__endpoint = "https://api.fostplus.be/recycle-public/app/v1"
        # self.__session.get(
        #     "https://recycleapp.be/config/app.settings.json").json()["API"]

    def __getSecret(self) -> str:
        html = self.__session.get("https://www.recycleapp.be/").text
        scriptUrl = next(re.finditer(
            r"src=\"([^\"]+main\.[^\"]+\.js)\"", html)).group(1)
        script = self.__session.get("https://www.recycleapp.be/" + scriptUrl).text
        return next(re.finditer(r"\"(\w{200,})\"", script)).group(1)

    def __getAccessToken(self) -> str:
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
            _secret = self.__getSecret()
        return _secret

    @property
    def accessToken(self) -> str:
        global _accessToken
        if (not _accessToken):
            _accessToken = self.__getAccessToken()

        return _accessToken

    def __post(self, action: str, data=None):
        for _ in range(2):
            headers = {"Authorization": self.accessToken}
            response = self.__session.post(
                f"{self.__endpoint}/{action}", json=data, headers=headers)
            if response.status_code == 200:
                return response.json()

            if response.status_code == 401:
                global _accessToken
                _accessToken = None

    def __get(self, action: str):
        for _ in range(2):
            headers = {"Authorization": self.accessToken}
            response = self.__session.get(
                f"{self.__endpoint}/{action}", headers=headers)
            if response.status_code == 200:
                return response.json()

            if response.status_code == 401:
                global _accessToken
                _accessToken = None

    def getZipCode(self, zipCode: int, language: str = "fr") -> str:
        result = self.__get(f"zipcodes?q={zipCode}")
        if result["total"] != 1:
            raise FostPlusApiException("invalid_zipcode")
        item = result["items"][0]
        return (item["id"], f'{item["code"]} - {item["names"][0][language]}')

    def getStreet(self, street: str, zipCodeId: str, language: str = "fr") -> Tuple[str, str]:
        result = self.__post(f"streets?q={street}&zipcodes={zipCodeId}")
        if result["total"] != 1:
            raise FostPlusApiException("invalid_streetname")
        return (result["items"][0]["id"], result["items"][0]["names"][language])

    def getFractions(self, zipCodeId: str, streetId: str, houseNumber: int, size=50) -> List[str]:
        fractions: List[Dict[str, Dict[str, str]]] = self.__get(f"fractions?zipcodeId={zipCodeId}&streetId={streetId}&houseNumber={houseNumber}&size={size}")["items"]
        return [f["logo"]["id"] for f in fractions if f["logo"]["id"] in COLLECTION_TYPES]

    def getCollections(self, zipCodeId: str, streetId: str, houseNumber: int, fromDate: date = None, untilDate: date = None, size=100) -> dict[str, date]:
        if (not fromDate):
            fromDate = datetime.now()
        if (not untilDate):
            untilDate = fromDate + timedelta(weeks=8)
        result = {}
        EMPTY_DICT = {}
        collections: array[dict] = self.__get(
            f'collections?zipcodeId={zipCodeId}&streetId={streetId}&houseNumber={houseNumber}&fromDate={fromDate.strftime("%Y-%m-%d")}&untilDate={untilDate.strftime("%Y-%m-%d")}&size={size}')["items"]
        for item in collections:
            if item.get("exception", EMPTY_DICT).get("replacedBy", None):
                continue
            id = item.get("fraction", EMPTY_DICT).get(
                "logo", EMPTY_DICT).get("id", None)
            if id not in COLLECTION_TYPES:
                continue
            parts = item.get(
                "timestamp", "2999-12-31T").split('T')[0].split('-')
            collectionDate = date(int(parts[0]), int(parts[1]), int(parts[2]))
            currentDate = result.get(id, date.max)
            if collectionDate < currentDate:
                result[id] = collectionDate

        return result


class FostPlusApiException(Exception):
    def __init__(self, code: str) -> None:
        self.__code = code
        pass
    @property
    def code(self) -> str:
        return self.__code
