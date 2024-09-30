from pydantic import BaseModel


class Choice(BaseModel):
    """
    Represents a choice in the game.

    Attributes:
        emoji (str): The emoji representing the choice.
        name (str): The name of the choice.
        choice (str): The description of the choice.
        choice_type (str): The type of the choice.
    """
    emoji: str
    name: str
    choice: str
    choice_type: str


class Choices(BaseModel):
    """
    Represents a list of choices.

    Attributes:
        choices (list[Choice]): A list of `Choice` objects.
    """
    choices: list[Choice]


class Consequence(BaseModel):
    """
    Represents the consequence of a choice.

    Attributes:
        choice (str): The description of the choice.
        consequence (str): The description of the consequence.
        plot (str): A short summary of the plot.
        prose (str): A detailed description of the story so far.
    """
    choice: str
    consequence: str
    plot: str
    prose: str


class Answer(BaseModel):
    """
    Represents an answer to a player's question.

    Attributes:
        answer (str): The answer to the player's question.
    """
    answer: str