# prompts.py

def initial_options_prompt(context: str, option: str) -> str:
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
    return f"""
    **Given the following story summary: {memory_manager.read("plot")}

    Character: {memory_manager.read("plot")}
    Setting: {memory_manager.read("plot")}
    Motivation: {memory_manager.read("plot")}
    Prose: {memory_manager.read("prose")}

    **Generate 3 interesting and unique choices for the next stage of the story game. Each choice should:**

    - **Next event is randomly selected from one of these types:**
     1. Introduce a new conflict or complication
     2. Character decision or turning point
     3. Reveal key information
     4. Dialogue that drives action
     5. Change in setting or environment
     6. Character encounter
     7. Moment of crisis
     8. Twist or unexpected event
     9. Character development
     10. Resolution of a conflict
     11. Character's emotion
     12. Character's perspective

    - **Consider the reader as a college student and write accordingly.**
    - **Be relatable, realistic, and contextually consistent with the given story details.**
    - **Keep fantastical elements plausible and integrated into the story.**
    - **Enrich the narrative with specific details like names, adjectives, and natural occurrences that add depth and are not easily predicted by the player.**
    - **Include only existing elements from the story memory, or thoroughly explain any new elements within the choice.**
    - **Be creative and consistent with the current story and past actions, realistically incorporating emojis as cues.**
    - **Be less than 15  words and start with a relevant emoji.**
    - **Suggest possibilities that could lead to a satisfying conclusion of the story.**
    - **Write in concrete and draw subtle inspiration from philosophical ideas of authors like Franz Kafka, Isaac Asimov, Ursula K. Le Guin, Michael Crichton, Albert Camus, Gilles Deleuze, Fyodor Dostoevsky, Jonathan Haidt, and Jorge Luis Borges—without mentioning their names or exact concepts.**
    - **Focus on engaging the user with creative and consistent choices that encourage continued interaction.**
    - **Be very clear if the choice is an environment change or an action by the character and frame the choice accordingly.**
    - **Use the character, setting, plot, and motivation to create choices that are coherent with the story.**
    - **If there are new elements being introduced, explain properly for the user**
    - **Use simple language and always aim to be under 50 on Flesch-Kincaid Readability Tests score.**
    **Final result should be a list of 3 choices.**
    """


def player_question_prompt(memory_manager, question: str) -> str:
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
    return f"""
    Generate a consequence for the following action in the story game:
    Action: {choice}
    character: {memory_manager.read("character")}
    setting: {memory_manager.read("setting")}
    plot: {memory_manager.read("plot")}
    motivation: {memory_manager.read("motivation")}
    Story so far: {memory_manager.read('prose')}
    Be creative and consider the past actions when generating the consequence, keep it causal and realistic.
    Provide the consequence with 4 elements:
    1. choice - A string description of the choice user made
    2. consequence - A string describing what happens next less than 100 words
    3. prose - A detailed description of the story so far including this new consequence structured as a short story.  Be consistent with past actions and consequences and add more detail to the plot to make the story coherent. Keep all key information.
    4. plot - A short summary describing the plot of the story based on the prose.
    """
