from pydantic import BaseModel


class InputData(BaseModel):
    list_1: list[str]
    list_2: list[str]
