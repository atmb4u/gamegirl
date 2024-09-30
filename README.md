# GameGirl
## The stories we tell ourselves!


This project is a generative story game that uses OpenAI's GPT-4o to create an interactive storytelling experience. The game allows players to make choices that influence the story, ask questions, and see the consequences of their actions.

## Demo
![](demo/gamegirl_demo.mov)

## Basics

- Generate initial options for characters, settings, and motivations.
- Generate choices for the next stage of the story.
- Handle player questions and generate answers.
- Simulate the consequences of player choices.
- Save and load the story memory.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/atmb4u/gamegirl.git
    cd gamegirl
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the  application:
    ```sh
    python gamegirl.py
    ```

## Project Structure

- `base.py`: Contains the Pydantic models for the game.
- `gamegirl.py`: Contains the main class `GenerativeStoryGame` which manages the game flow, interactions with the OpenAI API, and memory management.
- `memory.py`: Contains the `MemoryManager` class which manages the game memory.
- `prompts.py`: Contains functions that generate prompts for the OpenAI API based on the current state of the game.
- `requirements.txt`: Lists the required Python packages.
- `README.md`: This file.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.