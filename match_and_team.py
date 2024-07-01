import json
import os
from datetime import date, datetime

from euro_2024_api_handler import Euro2024ApiHandler
from stadium import Stadium


class Team:
    """Represents a team."""

    def __init__(self, id, code, name, group):
        """Construct a new Team.

        Args:
            id (str): the id of the team.
            code (str): the code of the team.
            name (str): the name of the team.
            group (str): the group of the team.

        Raises:
            TypeError: if id is not a str.
            TypeError: if code is not a str.
            TypeError: if name is not a str.
            TypeError: if group is not a str.
        """
        if not isinstance(id, str):
            raise TypeError("id must be a str.")
        self.id = id
        if not isinstance(code, str):
            raise TypeError("code must be a str.")
        self.code = code
        if not isinstance(name, str):
            raise TypeError("name must be a str.")
        self.name = name
        if not isinstance(group, str):
            raise TypeError("group must be a str.")
        self.group = group

    def __repr__(self):
        return f"Team({self.id}, {self.code}, {self.name}, {self.group})"


class TeamManager:
    DATA_FILENAME = "teams.json"

    def __init__(self, teams=None):
        """Initialize the manager."""
        if not teams:
            teams = []
        if not isinstance(teams, list):
            raise TypeError("teams must be a list.")
        self.teams = teams
        self.api_handler = Euro2024ApiHandler()

    def add_team(self, team):
        """Add a team to the manager."""
        if not isinstance(team, Team):
            raise TypeError("team must be a Team.")
        self.teams.append(team)

    def remove_team(self, team):
        """Remove a team from the manager."""
        if not isinstance(team, Team):
            raise TypeError("team must be a Team.")
        self.teams.remove(team)

    def get_team_by_id(self, id):
        """Get a team by its id."""
        if not isinstance(id, str):
            raise TypeError("id must be a str.")
        for team in self.teams:
            if team.id.lower() == id.lower():
                return team
        return None

    def get_team_by_name(self, name):
        """Get a team by its name."""
        if not isinstance(name, str):
            raise TypeError("name must be a str.")
        for team in self.teams:
            if team.name.lower() == name.lower():
                return team
        return None

    def get_team_by_code(self, code):
        """Get a team by its code."""
        if not isinstance(code, str):
            raise TypeError("code must be a str.")
        for team in self.teams:
            if team.code.lower() == code.lower():
                return team
        return None

    def load_teams_data(self):
        if not os.path.exists(self.DATA_FILENAME):
            teams_data = self.api_handler.get_teams()
        else:
            with open(self.DATA_FILENAME, "r", encoding="utf-8") as fh:
                teams_data = json.load(fh)
        for item in teams_data:
            team = Team(id=item["id"], code=item["code"], name=item["name"], group=item["group"])
            self.add_team(team)

    def save_teams_data(self):
        teams_data = []
        for team in self.teams:
            team_data = {
                "id": team.id,
                "code": team.code,
                "name": team.name,
                "group": team.group,
            }
            teams_data.append(team_data)
        with open(self.DATA_FILENAME, "w", encoding="utf-8") as fh:
            json.dump(teams_data, fh, indent=4)

    def del_data_file(self):
        if os.path.exists(self.DATA_FILENAME):
            os.remove(self.DATA_FILENAME)


class Match:
    """Representation of a match."""

    def __init__(self, id, number, home, away, match_date, group, stadium):
        """Constructor.

        Args:
            id (str): the id of the match.
            number (int): the number of the match.
            home (Team): the home team.
            away (Team): the visitor team.
            match_date (date): the date of the match.
            group (str): the group of the match.
            stadium (Stadium): the stadium of the match.

        Raises:
            TypeError: if id is not a str.
            TypeError: if number is not a int.
            ValueError: if number <= 0.
            TypeError: if home is not a Team obj.
            TypeError: if away is not a Team obj.
            TypeError: if match_date is not a str or date.
            ValueError: if match_date is an invalid str.
            TypeError: if group is not a str.
            TypeError: if stadium is not a Stadium obj.
        """
        if not isinstance(id, str):
            raise TypeError("id must be a str.")
        self.id = id
        if not isinstance(number, int):
            raise TypeError("number must be an int.")
        if number <= 0:
            raise ValueError("number must be a positive integer.")
        self.number = number
        if not isinstance(home, Team):
            raise TypeError("home must be a Team.")
        self.home = home
        if not isinstance(away, Team):
            raise TypeError("away must be a Team.")
        self.away = away
        if not isinstance(match_date, (date | str)):
            raise TypeError("match_date must be a date or a str in the format 'YYYY-MM-DD'.")
        if isinstance(match_date, str):
            try:
                match_date = datetime.strptime(match_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Expected 'YYYY-MM-DD'.")
        self.date = match_date
        if not isinstance(group, str):
            raise TypeError("group must be a str.")
        self.group = group
        if not isinstance(stadium, Stadium):
            raise TypeError("stadium must be a Stadium.")
        self.stadium = stadium

    def __repr__(self):
        return f"Match({self.id}, {self.number}, {self.home}, {self.away}, {self.date}, {self.group}, {self.stadium})"

    def code(self):
        match_text = f"{self.home.code} vs {self.away.code}"
        return match_text

    def team_vs_team(self):
        match_text = f"{self.home.name} vs {self.away.name}"
        return match_text


class MatchManager:
    DATA_FILENAME = "matches.json"

    def __init__(self, matches=None):
        """Initialize the manager."""
        if not matches:
            matches = []
        if not isinstance(matches, list):
            raise TypeError("matches must be a list.")
        self.matches = matches
        self.api_handler = Euro2024ApiHandler()

    def add_match(self, match):
        """Add a match to the manager."""
        if not isinstance(match, Match):
            raise TypeError("match must be a Match.")
        self.matches.append(match)

    def remove_match(self, match):
        """Remove a match from the manager."""
        if not isinstance(match, Match):
            raise TypeError("match must be a Match.")
        self.matches.remove(match)

    def get_match_by_id(self, id):
        """Get a match by its id."""
        if not isinstance(id, str):
            raise TypeError("id must be a str.")
        for match in self.matches:
            if match.id.lower() == id.lower():
                return match
        return None

    def get_match_by_number(self, number):
        """Get a match by its number."""
        if not isinstance(number, int):
            raise TypeError("number must be an int.")
        for match in self.matches:
            if match.number == number:
                return match
        return None

    def get_matches_by_team(self, team):
        if not isinstance(team, Team):
            raise TypeError("team must be a Team.")
        matches_by_team = []
        for match in self.matches:
            if match.away == team or match.home == team:
                matches_by_team.append(match)
        return matches_by_team

    def get_matches_by_stadium(self, stadium):
        if not isinstance(stadium, Stadium):
            raise TypeError("stadium must be a Stadium.")
        matches_by_stadium = []
        for match in self.matches:
            if match.stadium == stadium:
                matches_by_stadium.append(match)
        return matches_by_stadium

    def get_matches_by_date(self, match_date):
        if not isinstance(match_date, (date | str)):
            raise TypeError("date must be a date.")
        if isinstance(match_date, str):
            try:
                match_date = datetime.strptime(match_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Expected 'YYYY-MM-DD'.")
        matches_by_date = []
        for match in self.matches:
            if match.date == match_date:
                matches_by_date.append(match)
        return matches_by_date

    def load_matches_data(self, team_manager, stadium_manager):
        if not os.path.exists(self.DATA_FILENAME):
            matches_data = self.api_handler.get_matches()
        else:
            with open(self.DATA_FILENAME, "r", encoding="utf-8") as fh:
                matches_data = json.load(fh)
        self.matches = []
        for item in matches_data:
            raw_home_team = item["home"]
            raw_away_team = item["away"]
            home_team = team_manager.get_team_by_id(raw_home_team["id"])
            away_team = team_manager.get_team_by_id(raw_away_team["id"])
            group = item["group"].split(" ")[1].strip()
            stadium = stadium_manager.get_stadium_by_id(item["stadium_id"])
            match = Match(
                id=item["id"],
                number=item["number"],
                home=home_team,
                away=away_team,
                match_date=item["date"],
                group=group,
                stadium=stadium,
            )
            self.add_match(match)

    def save_matches_data(self, team_manager, stadium_manager):
        matches_data = []
        for match in self.matches:
            match_data = {}
            match_data["id"] = match.id
            match_data["number"] = match.number
            match_data["date"] = match.date.strftime("%Y-%m-%d")
            match_data["group"] = f"Group {match.group}"
            match_data["stadium_id"] = match.stadium.id
            home_data = {}
            home_data["id"] = match.home.id
            home_data["code"] = match.home.code
            home_data["name"] = match.home.name
            home_data["group"] = match.home.group
            away_data = {}
            away_data["id"] = match.away.id
            away_data["code"] = match.away.code
            away_data["name"] = match.away.name
            away_data["group"] = match.away.group

            match_data["home"] = home_data
            match_data["away"] = away_data

            matches_data.append(match_data)
        with open(self.DATA_FILENAME, "w", encoding="utf-8") as fh:
            json.dump(matches_data, fh, indent=4)

    def del_data_file(self):
        if os.path.exists(self.DATA_FILENAME):
            os.remove(self.DATA_FILENAME)
