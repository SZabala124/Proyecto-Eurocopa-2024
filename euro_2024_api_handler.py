import requests


class Euro2024ApiHandler:
    """Euro 2024 API handler."""

    API_TEAMS_URL = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json"
    API_STADIUMS_URL = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json"
    API_MATCHES_URL = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json"

    def __init__(self):
        """Initialize the object"""
        # These are used for debugging purposes
        self._url = None  # Last request url used
        self._type = None  # last request type ("teams", "matches", "stadiums")
        self._response = None  # last request response (object)

    def _get_raw_info(self, url):
        """Return a raw answer from the api request.

        Args:
            url (str): the url of the API.

        Returns:
            list: a list of dicts with the raw content response for the request.
        """
        self._response = requests.get(url)
        if self._response.status_code == requests.codes.ok and self._response.headers["Content-Type"] in [
            "application/json",
            "text/plain; charset=utf-8",
        ]:
            return self._response.json()
        else:
            self._response.raise_for_status()

    def get_teams(self):
        """Returns the answer from the teams api request.

        Returns:
            list: a list of dicts with the response for the teams request.
        """
        self._url = self.API_TEAMS_URL
        self._type = "teams"
        return self._get_raw_info(self.API_TEAMS_URL)

    def get_matches(self):
        """Returns the answer from the matches api request.

        Returns:
            list: a list of dicts with the response for the matches request.
        """
        self._url = self.API_TEAMS_URL
        self._type = "matches"
        return self._get_raw_info(self.API_MATCHES_URL)

    def get_stadiums(self):
        """Returns the answer from the stadiums api request.

        Returns:
            list: a list of dicts with the response for the stadiums request.
        """
        self._url = self.API_TEAMS_URL
        self._type = "stadiums"
        return self._get_raw_info(self.API_STADIUMS_URL)


def main():
    euro_api = Euro2024ApiHandler()
    # print("Teams:")
    # print(euro_api.get_teams())
    # print("Matches:")
    # print(euro_api.get_matches())
    # print("Stadiums:")
    # print(euro_api.get_stadiums())

    # print(type(euro_api._response))
    # print(euro_api._response.headers)

    import pprint

    pp = pprint.PrettyPrinter()
    pp.pprint(euro_api.get_stadiums())


if __name__ == "__main__":
    main()
