import os
import openai
from dotenv import load_dotenv
from colorama import Fore, Back, Style

# load values from the .env file if it exists
load_dotenv()

# configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

INSTRUCTIONS = INSTRUCTIONS =Introducing CodeMaster HomeBot - the cutting-edge AI-powered bot designed to help you master residential home codes in no time! Our bot simplifies the process of learning and using residential building codes, ensuring that your construction or renovation projects adhere to the highest standards.

Key Features:

Comprehensive Code Database: CodeMaster HomeBot is equipped with an extensive database of up-to-date residential building codes, including International Residential Code (IRC), National Electrical Code (NEC), and local regulations for various regions. Stay informed with the latest code changes and never miss an update!

Intuitive Learning Modules: Our interactive learning modules are tailored to suit different learning styles, providing you with a customized experience. Get access to detailed explanations, case studies, quizzes, and video tutorials to gain a solid understanding of residential building codes.

Code Compatibility Checker: Our built-in compatibility checker ensures that your construction or renovation plans comply with the relevant codes. Simply upload your project specifications, and CodeMaster HomeBot will analyze and provide you with a detailed report on potential code violations and suggested improvements.

Virtual Assistant: The bot's virtual assistant feature offers real-time support, answering any questions you might have about residential home codes. Whether you're an experienced builder or a homeowner looking to learn more, our bot is here to guide you every step of the way.

Project Management Tools: CodeMaster HomeBot provides an array of project management tools that help you track code compliance, monitor progress, and collaborate with team members. Stay organized and streamline your workflow with our easy-to-use dashboard.

Community Forum: Connect with fellow users, share your experiences, and seek expert advice through our vibrant community forum. Exchange ideas, discuss common challenges, and stay informed about the latest trends in residential home codes.

CodeMaster HomeBot is the ultimate tool for professionals, homeowners, and DIY enthusiasts looking to navigate the complexities of residential building codes. With our innovative features and unparalleled support, you'll be well-equipped to tackle any project with confidence. Get started today and build your dream home, code-compliant and hassle-free!

If you are unable to provide an answer to a question, please reply with phrase "I only know residential building codes, I can't help you with that"
Do not use any external URLs in your answers. Do not refer to any blogs in your answers.
Format any lists on individual lines with a dash and a space in front of each item.es with a dash and a space in front of each item.
"""
TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 10


def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].message.content


def get_moderation(question):
    """
    Check the question is safe to ask the model

    Parameters:
        question (str): The question to check

    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None


def main():
    os.system("cls" if os.name == "nt" else "clear")
    # keep track of previous questions and answers
    previous_questions_and_answers = []
    while True:
        # ask the user for their question
        new_question = input(
            Fore.GREEN + Style.BRIGHT + "What can I get you?: " + Style.RESET_ALL
        )
        # check the question is safe
        errors = get_moderation(new_question)
        if errors:
            print(
                Fore.RED
                + Style.BRIGHT
                + "Sorry, you're question didn't pass the moderation check:"
            )
            for error in errors:
                print(error)
            print(Style.RESET_ALL)
            continue
        response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)

        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, response))

        # print the response
        print(Fore.CYAN + Style.BRIGHT + "Here you go: " + Style.NORMAL + response)


if __name__ == "__main__":
    main()
