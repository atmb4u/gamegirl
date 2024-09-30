# prompts.py

"""
prompts.py

This file contains functions that generate prompts for the OpenAI API based on the current state of the game.

Functions:
    - initial_options_prompt: Generates a prompt for initial options based on context and option type.
    - choices_prompt: Generates a prompt for choices based on the current state of the game.
    - player_question_prompt: Generates a prompt for answering a player's question based on the current state of the game.
    - consequence_prompt: Generates a prompt for simulating the consequence of a player's choice based on the current state of the game.
"""

def initial_options_prompt(context: str, option: str) -> str:
    """
    Generates a prompt for initial options based on context and option type.

    Args:
        context (str): The context for generating options.
        option (str): The type of option to generate (e.g., character, setting).

    Returns:
        str: The generated prompt.
    """
    return f"""
    Given the context:
    {context}
    Using an emoji as inspiration, generate 3 compelling and addictive options for {option} to create a fun, relatable, coherent and thought-provoking storytelling game.
    Infuse deep and inspiring elements drawn from philosophical ideas, but avoid mentioning authors or using exact concepts from their works.
    Embrace a modern, dynamic style that resonates with today's audience, adding life to the choices with vivid details like character names, traits, ideologies,  expressive adjectives etc
    Each option should be concise, with a maximum length of 20 words.
    - **Be relatable, realistic, and grounded in the real world.**
    - **Use simple language and always aim to be under 50 on Flesch-Kincaid Readability Tests score.**
    """


def choices_prompt(memory_manager) -> str:
    """
    Generates a prompt for choices based on the current state of the game.

    Args:
        memory_manager (MemoryManager): The memory manager containing the current state of the game.

    Returns:
        str: The generated prompt.
    """
    return f"""
    **Given the following story summary: {memory_manager.read("plot")}

    Character: {memory_manager.read("character")}
    Setting: {memory_manager.read("setting")}
    Motivation: {memory_manager.read("motivation")}
    Prose: {memory_manager.read("prose")}

    **Generate 3 interesting and unique choices for the next stage of the story game. Each choice should:**

    - **Next event is randomly selected from one of these types, but prefer the ones that are most relevant and interesting to the story:**
     1. Character development
     2. Character's emotion or mental model
     3. Reveal key information
     4. Dialogue that drives action
     5. Change in setting or environment
     6. Character encounter
     7. Moment of crisis
     8. Twist or unexpected event
     9. Introduce a new conflict or complication
     10. Resolution of a conflict
     11. Character decision or turning point
     12. Character's perspective

    - **Consider the reader as a college student and write accordingly.**
    - **Be relatable, realistic, and contextually consistent with the given story details.**
    - **Keep fantastical elements plausible and integrated into the story.**
    - **Enrich the narrative with specific details like names, adjectives, and natural occurrences that add depth and are not easily predicted by the player.**
    - **Include only existing elements from the story memory, or thoroughly explain any new elements within the choice.**
    - **Be creative and consistent with the current story and past actions, realistically incorporating emojis as cues.**
    - **Be less than 15 words and start with a relevant emoji.**
    - **Suggest possibilities that could lead to a satisfying conclusion of the story.**
    - **Write in concrete and draw subtle inspiration from philosophical ideas of authors like Franz Kafka, Isaac Asimov, Ursula K. Le Guin, Michael Crichton, Albert Camus, Gilles Deleuze, Fyodor Dostoevsky, Jonathan Haidt, and Jorge Luis Borges—without mentioning their names or exact concepts.**
    - **Focus on engaging the user with creative and consistent choices that encourage continued interaction.**
    - **Be very clear if the choice is an environment change or an action by the character and frame the choice accordingly.**
    - **Use the character, setting, plot, and motivation to create choices that are coherent with the story.**
    - **If there are new elements being introduced, explain properly for the user.**
    - **Use simple language and always aim to be under 50 on Flesch-Kincaid Readability Tests score.**
    **Final result should be a list of 3 choices.**
    Each choice should be an instance of the Choice class with the following attributes:
    - emoji (str): The emoji representing the choice.
    - name (str): The name of the choice.
    - choice (str): The description of the choice.
    - choice_type (str): The type of the choice.
    """


def player_question_prompt(memory_manager, question: str) -> str:
    """
    Generates a prompt for answering a player's question based on the current state of the game.

    Args:
        memory_manager (MemoryManager): The memory manager containing the current state of the game.
        question (str): The player's question.

    Returns:
        str: The generated prompt.
    """
    return f"""
    Story so far: {memory_manager.read("prose")}
    Motivation: {memory_manager.read("motivation")}
    Plot: {memory_manager.read("plot")}
    Character: {memory_manager.read("character")}
    Setting: {memory_manager.read("setting")}

    Answer the following question based on the above story under 150 words:
    Question: {question}
    """


def consequence_prompt(memory_manager, choice: str) -> str:
    """
    Generates a prompt for simulating the consequence of a player's choice based on the current state of the game.

    Args:
        memory_manager (MemoryManager): The memory manager containing the current state of the game.
        choice (str): The player's choice.

    Returns:
        str: The generated prompt.
    """
    return f"""
    Generate a consequence for the following action in the story game:
    Action: {choice}
    Character: {memory_manager.read("character")}
    Setting: {memory_manager.read("setting")}
    Plot: {memory_manager.read("plot")}
    Motivation: {memory_manager.read("motivation")}
    Story so far: {memory_manager.read('prose')}
    Be creative and consider the past actions when generating the consequence, keep it causal and realistic.
    Provide the consequence with 4 elements:
    1. choice - A string description of the choice user made
    2. consequence - A string describing what happens next less than 100 words
    3. prose - A detailed description of the story so far including this new consequence structured as a short story. Be consistent with past actions and consequences and add more detail to the plot to make the story coherent. Keep all key information.
    4. plot - A short summary describing the plot of the story based on the prose.
    """