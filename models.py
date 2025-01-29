from sqlmodel import SQLModel, Field


class CachedTransformation(SQLModel, table=True):
    input_text: str = Field(primary_key=True)
    output_text: str


class Payload(SQLModel, table=True):
    payload_id: str = Field(primary_key=True)
    content: str
