from enum import Enum

from pydantic import BaseModel


class Genre(Enum):
    metal = 'metal'
    folk = 'folk'
    jazz_and_blues = 'jazz and blues'
    soul_and_reggae = 'soul and reggae'
    classic_pop_and_rock = 'classic pop and rock'
    punk = 'punk'
    dance_and_electronica = 'dance and electronica'
    pop = 'pop'


class TitleListArgs(BaseModel):
    genre: Genre
