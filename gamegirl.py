import openai
from typing import List, Tuple
import json
import argparse
import os
import pickle
from memory import MemoryManager
from base import Choice, Choices, Consequence, Answer
from prompts import initial_options_prompt, choices_prompt, player_question_prompt, consequence_prompt


class GenerativeStoryGame:
    def __init__(self):
        self.client = openai.OpenAI()  # Initialize the OpenAI client
        self.memory_manager = MemoryManager()
        self.memory_manager.write("story_memory", {
            "actions": [],
            "plot": "",
            "user_questions": [],
            "character": "",
            "motivation": "",
            "setting": "",
            "prose": ""
        })

    def generate_initial_options(self, context: str, option: str) -> List[str]:
        prompt = initial_options_prompt(context, option)
        print(f"Initial Choice Prompt length: {len(prompt)}")
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            response_format=Choices,
        )
        choices = json.loads(response.choices[0].message.parsed.model_dump_json()).get("choices", [])
        return choices

    def generate_choices(self) -> List[str]:
        prompt = choices_prompt(self.memory_manager)
        # print(f"Choice Prompt length: {len(prompt)}")
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[{"role": "user", "content": prompt}],
            response_format=Choices
        )
        options = json.loads(response.choices[0].message.content)
        return options

    def handle_player_question(self, question: str) -> str:
        prompt = player_question_prompt(self.memory_manager, question)
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[{"role": "user", "content": prompt}],
            response_format=Answer
        )
        answer = json.loads(response.choices[0].message.content)
        return answer.get("answer", "")

    def simulate_consequence(self, choice: str) -> Tuple[str, str]:
        prompt = consequence_prompt(self.memory_manager, choice)
        # print(f"Consequence Prompt length: {len(prompt)}")
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[{"role": "user", "content": prompt}],
            response_format=Consequence
        )
        consequence = json.loads(response.choices[0].message.content)
        return consequence

    def process_consequence(self, turn: int, chosen_action: str):
        consequence = self.simulate_consequence(chosen_action)
        actions = self.memory_manager.read("actions")
        actions.append({
            "turn_sequence": turn,
            "choice": consequence.get("choice", ""),
            "consequence": consequence.get("consequence", "")
        })
        self.memory_manager.update("actions", actions)
        self.memory_manager.update("prose", consequence.get("prose", ""))
        self.memory_manager.update("plot", consequence.get("plot", ""))
        self.save_story_memory(self.default_filename)

    def save_story_memory(self, filename: str):
        with open(filename, 'wb') as file:
            pickle.dump({
                'memory': self.memory_manager.memory,
                'history': self.memory_manager.history,
                'version': self.memory_manager.version
            }, file, protocol=pickle.HIGHEST_PROTOCOL)

    def load_story_memory(self, filename: str):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            self.memory_manager.memory = data['memory']
            self.memory_manager.history = data['history']
            self.memory_manager.version = data['version']

    def get_user_input(self, prompt: str) -> str:
        user_input = input(prompt)
        if user_input.lower() == 'q':
            print("Thank you for playing GameGirl!")
            exit()
        return user_input

    def choose_option(self, context: str, option_type: str) -> str:
        options = self.generate_initial_options(context, option_type)
        print(f"\nChoose your {option_type}:")
        for i, option in enumerate(options, 1):
            if i > 3:
                break
            print(f"{i}. {option.get('emoji')} - {option.get('name')} - {option.get('choice')}")
        print(f"4. Type your own {option_type}")
        choice = self.get_user_input(f"Pick your {option_type} (1-3) or type your own {option_type}: ")
        if choice in ["1", "2", "3"]:
            chosen_option = Choice(emoji=options[int(choice) - 1].get("emoji", ""),
                                    name=options[int(choice) - 1].get("name", ""),
                                    choice=options[int(choice) - 1].get("choice", ""))
        else:
            chosen_option = Choice(emoji="", name="", choice=choice)
        self.memory_manager.write(option_type, chosen_option)
        return chosen_option

    def get_next_story_number(self):
        existing_files = [f for f in os.listdir() if f.startswith("story_") and f.endswith(".gsg")]
        if not existing_files:
            return 1
        numbers = [int(f.split("_")[1].split(".")[0]) for f in existing_files]
        return max(numbers) + 1

    def play(self, filename: str = None):
        self.default_filename = filename or f"story_{self.get_next_story_number()}.gsg"
        if filename:
            self.load_story_memory(filename)
        else:
            print("Welcome to GameGirl - The stories we tell ourselves!\nPress q to quit.")
            self.memory_manager.write("character", self.choose_option("", "character"))
            self.memory_manager.write("setting", self.choose_option(str(self.memory_manager.memory), "setting"))
            self.memory_manager.write("motivation", self.choose_option(str(self.memory_manager.memory), "motivation"))
            self.memory_manager.write("actions", [])
            self.memory_manager.write("turn", 0)
        turn = self.memory_manager.read("turn")

        while True:
            turn += 1
            if self.memory_manager.read('plot'):
                print(f"\nStory summary so far: \n{self.memory_manager.read('plot')}")
            else:
                print("\nWhat's your next move?\n")
            choices = self.generate_choices().get("choices", [])
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice.get('emoji')} - {choice.get('name')} - {choice.get("choice", "")} ({choice.get("choice_type", "")})")
            print(f"4. Custom event")
            player_choice = self.get_user_input(f"Enter your choice (1-4) or h for help:")
            match player_choice:
                case "h":
                    player_choice = input("\nType for questions\nf for full story\nm for more choices\nq to quit\n")
                    continue
                case "f":
                    print(f"\nStory so far: \n{self.memory_manager.read('prose')}")
                    continue
                case "m" | "":
                    continue
                case "1" | "2" | "3":
                    chosen_action = choices[int(player_choice) - 1].get("choice", "")
                    self.process_consequence(turn, chosen_action)
                case "4":
                    chosen_action = self.get_user_input("Enter your custom action: ")
                    self.process_consequence(turn, chosen_action)
                case _:
                    question = player_choice
                    while True:
                        answer = self.handle_player_question(question)
                        print(f"\nQuestion: {question}\nAnswer: {answer}")
                        user_questions = self.memory_manager.read("user_questions")
                        user_questions.append({"question": question, "answer": answer})
                        self.memory_manager.update("user_questions", user_questions)
                        self.save_story_memory(self.default_filename)
                        question = self.get_user_input("Type your question for analysis\nEnter c to continue:\n")
                        if question == "c":
                            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generative Story Game")
    parser.add_argument('--file', type=str, help='File to load the story memory from')
    args = parser.parse_args()

    game = GenerativeStoryGame()
    game.play(args.file)