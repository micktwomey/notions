import datetime
import typing

import pydantic


class DateRange(pydantic.BaseModel):
    start: typing.Union[datetime.datetime, datetime.date]
    end: typing.Optional[typing.Union[datetime.datetime, datetime.date]]

    # TODO: decide if a dict or a dataclass or the daterange is a good return value
    def get_value(self):
        return {"start": self.start, "end": self.end}
