# generated by datamodel-codegen:
#   filename:  genre_list.json
#   timestamp: 2021-08-22T07:25:22+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Model(BaseModel):
    status: str
    status_code: int
    genre: List[str]
