from typing import Optional, List, Union, Tuple
from string import ascii_lowercase, digits

Filter = Union[List[str], str]

VALID_TIMESPAN_UNITS = ["min", "h", "hours", "d", "days", "w", "weeks", "m", "months"]

def near(n: int, *args) -> str:
    if len(args) < 2:
        raise ValueError("At least two words must be provided")

    return f"near{str(n)}:" + '"' + " ".join([a for a in args]) + '" '


def repeat(n: int, keyword: str) -> str:
    if " " in keyword:
        raise ValueError("Only single words can be repeated")

    return f'repeat{str(n)}:"{keyword}" '


def multi_repeat(repeats: List[Tuple[int, str]], method: str) -> str:

    if method not in ["AND", "OR"]:
        raise ValueError(f"method must be one of AND or OR, not {method}")

    to_repeat = [repeat(n, keyword) for (n, keyword) in repeats]

    if method == "AND":
        return f"{method} ".join(to_repeat)
    elif method == "OR":
        return "(" + f"{method} ".join(to_repeat) + ")"


class Filters:
    def __init__(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        timespan: Optional[str] = None,
        num_records: int = 250,
        keyword: Optional[Filter] = None,
        domain: Optional[Filter] = None,
        domain_exact: Optional[Filter] = None,
        near: Optional[str] = None,
        repeat: Optional[str] = None,
        country: Optional[Filter] = None,
        lang: Optional[Filter] = None,
        theme: Optional[Filter] = None,
    ) -> None:

        self.query_params: List[str] = []
        self._valid_countries: List[str] = []
        self._valid_themes: List[str] = []

        if not start_date and not end_date and not timespan:
            raise ValueError("Must provide either start_date and end_date, or timespan")

        if start_date and end_date and timespan:
            raise ValueError(
                "Can only provide either start_date and end_date, or timespan"
            )

        if keyword:
            self.query_params.append(self._keyword_to_string(keyword))

        if domain:
            self.query_params.append(self._filter_to_string("domain", domain))

        if domain_exact:
            self.query_params.append(self._filter_to_string("domainis", domain_exact))

        if country:
            self.query_params.append(self._filter_to_string("sourcecountry", country))

        if lang:
            self.query_params.append(self._filter_to_string("sourcelang", lang))

        if theme:
            self.query_params.append(self._filter_to_string("theme", theme))

        if near:
            self.query_params.append(near)

        if repeat:
            self.query_params.append(repeat)

        if start_date:
            self.query_params.append(
                f'&startdatetime={start_date.replace("-", "")}000000'
            )
            self.query_params.append(f'&enddatetime={end_date.replace("-", "")}000000')
        else:
            # Use timespan
            self._validate_timespan(timespan)
            self.query_params.append(f"&timespan={timespan}")

        if num_records > 250:
            raise ValueError(f"num_records must 250 or less, not {num_records}")

        self.query_params.append(f"&maxrecords={str(num_records)}")

    @property
    def query_string(self) -> str:
        return "".join(self.query_params)

    @staticmethod
    def _filter_to_string(name: str, f: Filter) -> str:

        if type(f) == str:
            return f"{name}:{f} "

        else:
            # Build an OR statement
            return "(" + " OR ".join([f"{name}:{clause}" for clause in f]) + ") "

    @staticmethod
    def _keyword_to_string(keywords: Filter) -> str:

        if type(keywords) == str:
            return f'"{keywords}" '

        else:
            return (
                "("
                + " OR ".join(
                    [f'"{word}"' if " " in word else word for word in keywords]
                )
                + ") "
            )

    @staticmethod
    def _validate_timespan(timespan: str) -> None:
        value = timespan.rstrip(ascii_lowercase)
        unit = timespan[len(value):]

        if unit not in VALID_TIMESPAN_UNITS:
            raise ValueError(f"Timespan {timespan} is invalid. {unit} is not a supported unit, must be one of {' '.join(VALID_TIMESPAN_UNITS)}")

        if not all(d in digits for d in value):
            raise ValueError(f"Timespan {timespan} is invalid. {value} could not be converted into an integer")

        if unit == "min" and int(value) < 60:
            raise ValueError(f"Timespan {timespan} is invalid. Period must be at least 60 minutes")
