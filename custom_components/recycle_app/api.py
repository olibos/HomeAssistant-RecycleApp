"""FostPlus API."""

from array import array
from collections import defaultdict
from datetime import date, datetime, timedelta

from requests import Session

from .const import COLLECTION_TYPES


class FostPlusApi:
    """FostPlus API client for interacting with the RecycleApp.be API.

    This client provides methods to fetch recycling information including:
    - Zip code and street validation
    - Recycling park locations and schedules
    - Collection fractions and dates

    The client automatically handles endpoint discovery via the app settings.
    """

    __session: Session | None = None
    __endpoint: str

    def initialize(self) -> None:
        """Ensure the API client is initialized.

        This method is idempotent.
        """
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
        self.__endpoint = f"{base_url}/public/v1"

    def __post(self, action: str, data=None):
        self.__ensure_initialization()
        for _ in range(2):
            response = self.__session.post(f"{self.__endpoint}/{action}", json=data)
            if response.status_code == 200:
                return response.json()
        return None

    def __get(self, action: str):
        self.__ensure_initialization()
        for _ in range(2):
            response = self.__session.get(f"{self.__endpoint}/{action}")
            if response.status_code == 200:
                return response.json()
        return None

    def get_zip_code(self, zip_code: int, language: str = "fr") -> tuple[str, str]:
        """Get a zip code details.

        Args:
            zip_code: The zip code (int).
            language: The user language (str, default "fr").

        Returns:
            A tuple of (id, name) where id is the unique id of the zip code and name is the name of the zip code in the given language.

        Raises:
            FostPlusApiException: When the zip code is not found.

        """
        result = self.__get(f"zipcodes?q={zip_code}")
        if result["total"] != 1:
            raise FostPlusApiException("invalid_zipcode")
        item = result["items"][0]
        return (item["id"], f'{item["code"]} - {item["names"][0][language]}')

    def get_street(
        self, street: str, zip_code_id: str, language: str = "fr"
    ) -> tuple[str, str]:
        """Get a street details.

        Args:
            street: The street name (str).
            zip_code_id: The zip code id (str).
            language: The user language (str, default "fr").

        Returns:
            A tuple of (id, name) where id is the unique id of the street and name is the name of the street in the given language.

        Raises:
            FostPlusApiException: When the street is not found.

        """
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
        """Get the recycling parks for the given zip code id.

        Args:
            zip_code_id: The zip code id (str).
            language: The user language (str).

        Returns:
            A dictionary where the key is the unique id of the recycling park and the value is a dictionary with the following keys:
                - name: The name of the recycling park in the given language.
                - exceptions: A list of exceptions.
                - periods: A list of periods.

        """
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
        """Get the collection fractions for the specified address.

        Args:
            zip_code_id: The zip code id (str) of the address.
            street_id: The street id (str) of the address.
            house_number: The house number (int) of the address.
            language: The user language (str) for the fraction names.
            size: The number of items per page (int), default is 100.

        Returns:
            A dictionary where the key is the unique id of the fraction's logo and
            the value is a tuple containing the fraction's color and name in the
            specified language.

        """
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
        from_date: date | None = None,
        until_date: date | None = None,
        size=100,
    ) -> dict[str, list[date]]:
        """Get a dictionary where the key is the fraction id and the value is a list of dates on which the fraction is collected.

        Args:
            zip_code_id: The id of the zip code (str).
            street_id: The id of the street (str).
            house_number: The house number (int) of the address.
            from_date: The start date of the period (date), default is the current date.
            until_date: The end date of the period (date), default is 8 weeks from the current date.
            size: The number of items per page (int), default is 100.

        Returns:
            A dictionary where the key is the fraction id and the value is a list
            of dates on which the fraction is collected.

        """
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
    """Base class for all FostPlus API related exceptions.

    Error Codes:
    - invalid_zipcode: The provided zip code was not found or had multiple matches
    - invalid_streetname: The provided street name was not found
    """

    def __init__(self: "FostPlusApiException", code: str) -> None:
        """Initialize FostPlus API exception.

        Args:
            code: The code of the exception (str).
                 See class docstring for possible values.

        """
        self.__code = code

    @property
    def code(self: "FostPlusApiException") -> str:
        """Return the code of the exception."""
        return self.__code
