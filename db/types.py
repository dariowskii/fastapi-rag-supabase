from datetime import datetime
from typing import Annotated
from pydantic import WrapSerializer

def convert_to_utc(value: datetime, handler, info):
    if info.mode == 'json':
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')
    return value

UTCDatetime = Annotated[datetime, WrapSerializer(convert_to_utc)]