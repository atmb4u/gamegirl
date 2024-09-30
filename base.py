from pydantic import BaseModel


class Choice(BaseModel):
    emoji: str
    name: str
    choice: str
    choice_type: str


class Choices(BaseModel):
    choices: list[Choice]


class Consequence(BaseModel):
    choice: str
    consequence: str
    plot: str
    prose: str


class Answer(BaseModel):
    answer: str
