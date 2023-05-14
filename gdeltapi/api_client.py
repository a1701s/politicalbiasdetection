import requests
import pandas as pd
from gdeltapi.filters import Filters
from typing import Dict
from gdeltapi.helpers import load_json
from gdeltapi._version import version

class GdeltDoc:

    def __init__(self, json_parsing_max_depth: int = 100) -> None:
        self.max_depth_json_parsing = json_parsing_max_depth

    def article_search(self, filters: Filters) -> pd.DataFrame:
        articles = self._query("artlist", filters.query_string)
        if "articles" in articles:
            return pd.DataFrame(articles["articles"])
        else:
            return pd.DataFrame()

    def timeline_search(self, mode: str, filters: Filters) -> pd.DataFrame:
        timeline = self._query(mode, filters.query_string)
        results = {"datetime": [entry["date"] for entry in timeline["timeline"][0]["data"]]}
        for series in timeline["timeline"]:
            results[series["series"]] = [entry["value"] for entry in series["data"]]
        if mode == "timelinevolraw":
            results["All Articles"] = [
                entry["norm"] for entry in timeline["timeline"][0]["data"]
            ]
        formatted = pd.DataFrame(results)
        formatted["datetime"] = pd.to_datetime(formatted["datetime"])
        return formatted

    def _query(self, mode: str, query_string: str) -> Dict:
        if mode not in [
            "artlist",
            "timelinevol",
            "timelinevolraw",
            "timelinetone",
            "timelinelang",
            "timelinesourcecountry",
        ]:
            raise ValueError(f"Mode {mode} not in supported API modes")
        headers = {
            "User-Agent": f"GDELT DOC Python API client {version} - https://github.com/alex9smith/gdelt-doc-api"
        }

        response = requests.get(
            f"https://api.gdeltproject.org/api/v2/doc/doc?query={query_string}&mode={mode}&format=json",
            headers=headers
        )

        if response.status_code not in [200, 202]:
            raise ValueError("The gdelt api returned a non-successful statuscode. This is the response message: {}".
                             format(response.text))

        if "text/html" in response.headers["content-type"]:
            raise ValueError(f"The query was not valid. The API error message was: {response.text.strip()}")

        return load_json(response.content, self.max_depth_json_parsing)
