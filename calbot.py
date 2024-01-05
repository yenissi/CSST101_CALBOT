import json
import random
from difflib import get_close_matches

def load_course_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_course_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, conversation: list[str]) -> str | None:
    for users in conversation:
        if isinstance(users, list):
            for user in users:
                match = get_close_matches(user_question, [user], n=1, cutoff=0.6)
                if match:
                    return user
        else:
            match = get_close_matches(user_question, [users], n=1, cutoff=0.6)
            if match:
                return users
    return None

def get_answer_for_question_course_base(question: str, course_base: dict) -> str | None:
    for entry in course_base["conversation"]:
        users = entry.get("user", [])
        if isinstance(users, list):
            if any(user.lower() == question.lower() for user in users):
                responses = entry.get("responses", [])
                return random.choice(responses) if responses else None
        else:
            if users.lower() == question.lower():
                responses = entry.get("responses", [])
                return random.choice(responses) if responses else None
    return None

def calbot():
    user_name = input('''CalBot: Kumusta! Ako si CalBot. Isang Chatbot na handang tumulong sa pagkilatis ng iyong tatahaking kurso sa kolehiyo.
                      \nAng iyong mga katanungan ay aking sasagutin hinggil sa kursong iyong gustong lakarin. 
                      \nBago ang lahat, ano ang iyong ngalan?\n\nYou: ''')
    print(f'''\nCalBot: Magandang araw, {user_name}! Sa ngayon, ano ang iyong antas (grade) sa pinapasukan mong paaralan?\n''')

    course_base: dict = load_course_base('course_base.json')

    while True:
        user_input: str = input(f'{user_name}: ').lower()

        if user_input == 'tapusin':
            response = input('\nCalBot: Sigurado ka na bang gusto mong tapusin? (Oo/Hindi): ')
            if response.lower() == 'oo':
                print('\nCalBot: Paalam! Salamat sa pag-usap. Hanggang sa muli!')
                break
            elif response.lower() == 'hindi':
                print('\nCalBot: Mabuti! Maaari na ba tayong magpatuloy ukol sa paghahanap ng kurso?')
                continue

        best_match: str | None = find_best_match(user_input, [q["user"] for q in course_base["conversation"]])

        if best_match:
            answer: str = get_answer_for_question_course_base(best_match, course_base)
            print(f'\nCalBot: {answer}\n')
        else:
            print('\nCalBot: Hindi ko alam ang iyong sinabi o itinanong. Maaari mo ba itong ituro sa akin?\n')
            new_answer: str = input('I-tayp ang sagot o ligtangan na lang: ')

            if new_answer.lower() != 'skip':
                course_base["conversation"].append({"user": [user_input], "responses": [new_answer]})
                save_course_base('course_base.json', course_base)
                print('\nCalBot: Salamat! May bago akong natutunan!\n')
                
if __name__ == '__main__':
    calbot()