from typing import Dict, List
from dataclasses_json import dataclass_json
from dataclasses import dataclass, field

from src.data_model.custom_decorators import dict_behavior, ToJson
from src.rating.confidence_rating import confidence_rating_by_population


@dataclass_json
@dataclass
class Location(ToJson):
    """Class representing location

    Attributes:
    :param latitude: float - latitude
    :param longitude: float - longitude
    """

    latitude: float = 0.0
    longitude: float = 0.0

    def __init__(self, latitude=0.0, longitude=0.0):
        self.latitude = latitude
        self.longitude = longitude

    def get(self, key, default=None):
        if key == 'latitude':
            return self.latitude
        if key == 'longitude':
            return self.longitude
        return default

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        if key == 'latitude':
            self.latitude = value
        if key == 'longitude':
            self.longitude = value

    def __iter__(self):
        return iter({'latitude': self.latitude, 'longitude': self.longitude})

    def __len__(self):
        return 2

    def to_dict(self):
        return {'latitude': self.latitude, 'longitude': self.longitude}

    def to_json(self):
        return self.to_dict()


@dict_behavior
@dataclass_json
@dataclass
class TimePoint(ToJson):
    """Class representing time point

    Attributes:
    :param hour: int - hour of the day (0-23)
    :param minute: int - minute of the hour (0-59)
    :param sum_minutes: int - sum of minutes from midnight
    """

    hour: int = 0
    minute: int = 0
    sum_minutes: int = 0

    def __init__(self, hour=None, minute=None, **kwargs):
        if hour is None:
            self.hour = 0
        else:
            self.hour = hour
        if minute is None:
            self.minute = 0
        else:
            self.minute = minute
        self.sum_minutes = self.hour * 60 + self.minute

    def get(self, key, default=None):
        if key == 'hour':
            return self.hour
        if key == 'minute':
            return self.minute
        if key == 'sum_minutes':
            return self.sum_minutes
        return default


@dict_behavior
@dataclass_json
@dataclass
class Period(ToJson):
    """Class representing period of time

    Attributes:
    :param open: TimePoint - time when the place opens
    :param close: TimePoint - time when the place closes
    """

    open: TimePoint = field(default_factory=TimePoint)
    close: TimePoint = field(default_factory=TimePoint)

    def __init__(self, open: TimePoint | dict = {}, close: TimePoint | dict = {}):
        if open.get('day', 0) != close.get('day', 0):
            close['hour'] += 24
        if not open:
            self.open = TimePoint()
        else:
            self.open = TimePoint(**open)
        if isinstance(close, TimePoint):
            self.close = close
        elif not close:
            self.close = TimePoint(hour=24)
        else:
            self.close = TimePoint(**close)

    @property
    def open_today(self):
        return self.open.sum_minutes < self.close.sum_minutes

    @property
    def open_in_minutes(self):
        return self.open.sum_minutes

    @property
    def close_in_minutes(self):
        
        
        return self.close.sum_minutes

    @open_in_minutes.setter
    def open_in_minutes(self, value):
        self._open_in_minutes = value

    @close_in_minutes.setter
    def close_in_minutes(self, value):
        self._close_in_minutes = value


@dataclass_json
@dataclass()
class RegularOpeningHours(ToJson):
    """Class representing regular opening hours

    Attributes:
    :param periods: List[Period] - list of periods
    :param weekdayDescriptions: List[str] - list of weekday descriptions
    """

    periods: List[Period]
    weekdayDescriptions: List[str] = field(default_factory=list)

    def __init__(self, periods=[], weekdayDescriptions=[]):
        self.weekdayDescriptions = weekdayDescriptions
        if (not periods
                or len(periods) == 1
                and isinstance(periods[0], dict)
                and periods[0]['open']['day'] == 0
                and periods[0]['open']['hour'] == 0
                and periods[0]['open']['minute'] == 0):
            self.periods = [Period() for _ in range(7)]
            return
        else:
            self.periods = [Period(close=TimePoint(0)) for _ in range(7)]
        for i, period in enumerate(periods):
            day_num = period['open']['day'] if period['open'].get('day') else i
            self.periods[day_num] = Period(**period)


@dataclass_json
@dataclass
class TextWithLang(ToJson):
    """Class representing text with language

    Attributes:
    :param text: str - text
    :param languageCode: str - language code
    """

    text: str = ""
    languageCode: str = ""


@dataclass_json
@dataclass
class Review(ToJson):
    """Class representing review

    Attributes:
    :param name: str - name of the reviewer
    :param relativePublishTimeDescription: str - relative publish time description
    :param rating: int - rating
    :param text: Dict[str, str] - text
    :param originalText: Dict[str, str] - original text
    :param publishTime: str - publish time
    """

    name: str = ""
    relativePublishTimeDescription: str = ""
    rating: int = 0
    text: Dict[str, str] = None
    originalText: Dict[str, str] = None
    publishTime: str = ""


@dataclass_json
@dataclass
class Photo(ToJson):
    """Class representing photo

    Attributes:
    :param photoReference: str - photo reference
    :param widthPx: int - width in pixels
    :param heightPx: int - height in pixels
    """

    name: str = ""
    widthPx: int = 0
    heightPx: int = 0


@dataclass_json
@dataclass
class AccessibilityOptions(ToJson):
    """Class representing accessibility options

    Attributes:

    :param wheelchairAccessibleParking: bool - if the place has wheelchair accessible parking
    :param wheelchairAccessibleEntrance: bool - if the place has wheelchair accessible entrance
    :param wheelchairAccessibleRestroom: bool - if the place has wheelchair accessible restroom
    :param wheelchairAccessibleSeating: bool - if the place has wheelchair accessible seating
    """

    wheelchairAccessibleParking: bool = False
    wheelchairAccessibleEntrance: bool = False
    wheelchairAccessibleRestroom: bool = False
    wheelchairAccessibleSeating: bool = False


@dataclass_json
@dataclass
class Dining(ToJson):
    """Class representing dining options

    Attributes:
    :param reservable: bool - if the place is reservable
    :param takeout: bool - if the place has takeout option
    :param dineIn: bool - if the place has dine-in option
    :param delivery: bool - if the place has delivery option
    :param servesBreakfast: bool - if the place serves breakfast
    :param servesLunch: bool - if the place serves lunch
    :param servesDinner: bool - if the place serves dinner
    :param servesBrunch: bool - if the place serves brunch
    :param outdoorSeating: bool - if the place has outdoor seating
    :param servesDessert: bool - if the place serves dessert
    :param servesCoffee: bool - if the place serves coffee
    :param goodForWatchingSports: bool - if the place is good for watching sports
    """

    reservable: bool = False
    takeout: bool = False
    dineIn: bool = False
    delivery: bool = False
    servesBreakfast: bool = False
    servesLunch: bool = False
    servesDinner: bool = False
    servesBrunch: bool = False
    outdoorSeating: bool = False
    servesDessert: bool = False
    servesCoffee: bool = False
    goodForWatchingSports: bool = False


@dataclass_json
@dataclass
class Children(ToJson):
    """Class representing children options

    Attributes:
    :param goodForChildren: bool - if the place is good for children
    :param menuForChildren: bool - if the place has a menu for children
    """

    goodForChildren: bool = False
    menuForChildren: bool = False


@dataclass_json
@dataclass
class Alcohol(ToJson):
    """Class representing alcohol options

    Attributes:
    :param servesBeer: bool - if the place serves beer
    :param servesWine: bool - if the place serves wine
    :param servesCocktails: bool - if the place serves cocktails
    """

    servesBeer: bool = False
    servesWine: bool = False
    servesCocktails: bool = False


@dataclass_json
@dataclass
class PlaceInfo(ToJson):
    """Class representing place info

    Attributes:
    :param name: str - name of the place
    :param id: str - id of the place
    :param formattedAddress: str - formatted address
    :param googleMapsUri: str - Google Maps URI
    :param websiteUri: str - website URI
    :param iconMaskBaseUri: str - icon mask base URI
    :param displayName: str - display name
    :param businessStatus: str - business status
    """

    name: str = ""
    id: str = ""
    formattedAddress: str = ""
    googleMapsUri: str = ""
    websiteUri: str = ""
    iconMaskBaseUri: str = ""
    displayName: str = ""
    businessStatus: str = ""


@dataclass_json
@dataclass
class PlaceRating(ToJson):
    """
    Class representing place rating

    Attributes:
    rating: float - rating
    confidenceRating: float - confidence rating
    cumulative_rating: float - cumulative rating
    userRatingCount: int - user rating count
    statisticalRating: float - statistical rating
    """
    rating: float = 0.0
    confidenceRating: float = 0.0
    cumulative_rating: float = 0.0
    userRatingCount: int = 0.0
    statisticalRating: float = 0.0
    type_rating: float = 0.0 

    def __post_init__(self):
        if self.confidenceRating <= 0:
            self.confidenceRating = confidence_rating_by_population(self.rating, self.userRatingCount)
