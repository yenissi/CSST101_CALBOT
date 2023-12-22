import json
import random
from difflib import get_close_matches

def load_course_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def load_secondary_level_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_course_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def save_secondary_level_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, conversation: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, conversation, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, course_base: dict) -> str | None:
    for entry in course_base["conversation"]:
        if entry["user"].lower() == question.lower():
            responses = entry.get("responses", [])
            return random.choice(responses) if responses else None
        
def get_answer_for_question(question: str, secondary_level_base: dict) -> str | None:
    for entry in secondary_level_base["conversation"]:
        if entry["user"].lower() == question.lower():
            responses = entry.get("responses", [])
            return random.choice(responses) if responses else None

def calbot():
    user_name = input('''CalBot: Kumusta! Ako si CalBot. Isang Chatbot na handang tumulong sa pagkilatis ng iyong tatahaking kurso sa kolehiyo.
                      \nAng iyong mga katanungan ay aking sasagutin hinggil sa kursong iyong gustong lakarin. 
                      \nBago ang lahat, ano ang iyong ngalan?\n\nYou: ''')
    print(f'''\nCalBot: Magandang araw, {user_name}! Sa ngayon, ano ang iyong antas (grade) sa pinapasukan mong paaralan?\n''')

    course_base: dict = load_course_base('course_base.json')
    secondary_level_base: dict = load_secondary_level_base('secondary_level_base.json')

    # Start with knowledge_base.json
    current_dictionary = course_base  

    while True:
        user_input: str = input(f'{user_name}: ').lower()

        if user_input == 'quit':
            response = input('\nCalBot: Sigurado ka na bang gusto mong tapusin? (Oo/Hindi): ')
            if response.lower() == 'oo':
                print('\nCalBot: Paalam! Salamat sa pag-usap. Hanggang sa muli!')
                break
            else:
                continue

        # Check if the user wants to switch to the secondary level
        if user_input and any(str(i) in user_input for i in range(7, 11)):
            current_dictionary = secondary_level_base
            print(f'''\nCalBot: Ikaw pala ay isang studyante mula sa ika-{user_input.lower()} na baitang.\n
        Sa panahon ng pagiging studyante ng sekondaraya ay dito na tayo magkakaroon ng kaisipan kung ano ba ang nais nating maging kurso pagdating ng kolehiyo na may koneksyon sa ating trabahong tatahakin.\n
        Sa buong taon ng iyong pag-aaral, anong asignatura ang iyong kinahihiligan?
        ''')
            continue

        best_match: str | None = find_best_match(user_input, [q["user"] for q in current_dictionary["conversation"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, current_dictionary)
            print(f'\nCalBot: {answer}\n')
        else:
            print('\nCalBot: Hindi ko alam ang iyong sinabi o itinanong. Maaari mo ba itong ituro sa akin?\n')
            new_answer: str = input('I-tayp ang sagot o ligtangan na lang: ')

            if new_answer.lower() != 'skip':
                current_dictionary["conversation"].append({"user": user_input, "responses": [new_answer]})
                save_course_base('course_base.json', course_base)
                save_course_base('secondary_level_base.json', secondary_level_base)
                print('\nCalBot: Salamat! May bago akong natutunan!\n')

if __name__ == '__main__':
    calbot()