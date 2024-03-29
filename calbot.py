#Import necessary modules
import json #Dictionary, dito naka-save yung user input at responses nung calbot
import random #Random na output ang ibibigay ni calbot dun sa responses array sa json
import time #Delay ito nung pag-output ni calbot. Para bang nag-iisip like chatgpt
from difflib import get_close_matches #Mahanap ni calbot yung close matches sa user input para ma-output naka-designated doon sa responses

#This is the function to load course base data from a file
def load_course_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

#This is the function to save course base data to a file
def save_course_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

#This is the function to find the best match for a user's question in a list of conversation strings
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

#This is the function to get a random response for a user's question from the course base
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

#This is the Main Function of the CalBot
def calbot():

    time.sleep(0.5) #Added a time delay of 0.5 seconds at the beginning

    #Getting the user's name
    user_name = input("CalBot: Kumusta! Ako si CalBot. Isang Chatbot na handang tumulong sa pagkilatis ng iyong tatahaking kurso sa kolehiyo. Ang iyong mga katanungan ay aking sasagutin hinggil sa kursong iyong gustong lakarin. Bago ang lahat, ano ang iyong ngalan?\n\nYou: ")

    time.sleep(0.5) #Added a time delay of 0.5 seconds after each user input for a realistic chatbot

    #Getting the user's grade level
    grade_level = input(f"\nCalBot: Magandang araw, {user_name}! Sa ngayon, ano ang iyong antas (grade) sa pinapasukan mong paaralan? (I-tayp kung \u002211\u0022 o \u002212\u0022)\n\n{user_name}: ")

    #This loop validates and responds based on the user's grade level
    while grade_level not in ['11', '12']:
        time.sleep(0.5)
        grade_level = input(f"\nCalBot: Mali ang iyong na-ilagay na antas. I-tayp lamang ang \u002211\u0022 o \u002212\u0022.\n\n{user_name}: ")

    time.sleep(0.5)
    responses = {
        '11': f"Ikaw pala, {user_name}, ay isang estudyante mula sa ika-11 na baitang. Sa panahon ng pagiging estudyante ng Senior High ay dito na tayo magkakaroon ng mas malalim na interes kung ano ba ang tatahakin nating kurso sa kolehiyo. Maaari na ba tayong magpatuloy ukol sa paghahanap ng kurso? (I-tayp ang \u0022Sige\u0022 o \u0022Ayoko\u0022)\n",
        '12': f"Ikaw pala, {user_name}, ay isang estudyante mula sa ika-12 na baitang. Sa panahon ng pagiging estudyante ng Senior High ay dito na tayo magkakaroon ng mas malalim na interes kung ano ba ang tatahakin nating kurso sa kolehiyo lalo na't ikaw ay magtatapos na ngayong taon. Maaari na ba tayong magpatuloy ukol sa paghahanap ng kurso? (I-tayp ang \u0022Sige\u0022 o \u0022Ayoko\u0022)\n"
    }

    time.sleep(0.5)
    print(f'\nCalBot: {responses[grade_level]}')

    #This loads the course base data from a file
    course_base: dict = load_course_base('course_base.json')

    #This is the main interaction loop
    while True:

        #This gets the user input with the user name
        user_input: str = input(f'{user_name}: ').lower()

        #Handle special commands
        if user_input.lower() == 'tapusin':
            time.sleep(0.5)
            response = input(f'\nCalBot: Sigurado ka na bang gusto mong tapusin? (Oo/Hindi)\n\n{user_name}: ')
            if response.lower() == 'oo':
                time.sleep(0.5)
                print('\nCalBot: Paalam! Salamat sa pag-usap. Hanggang sa muli!')
                break
            elif response.lower() == 'hindi':
                time.sleep(0.5)
                print('\nCalBot: Mabuti! Maaari na ba tayong magpatuloy ukol sa paghahanap ng kurso? (Sige/Ayoko)\n')
                continue

        if user_input.lower() == 'wala na':
            time.sleep(0.5)
            response = input('\nCalBot: Maraming salamat sa iyong oras! Hanggang sa muli!')
            break

         #Find the best match in the course base and get a response
        best_match: str | None = find_best_match(user_input, [q["user"] for q in course_base["conversation"]])

        if best_match:
            answer: str = get_answer_for_question_course_base(best_match, course_base)
            time.sleep(0.5)
            print(f'\nCalBot: {answer}\n')
        else:
            time.sleep(0.5)
            print('\nCalBot: Paumanhin ngunit hindi ko alam ang iyong sinabi o itinanong dahil limitado lamang ang aking kaalaman sa ngayon. Maaari mo ba itong ituro sa akin?\n')
            
            #This is to add a new user input and response to the course base
            new_answer: str = input('I-tayp ang sagot o ligtangan na lang: ')

            if new_answer.lower() != 'skip':
                course_base["conversation"].append({"user": [user_input], "responses": [new_answer]})
                save_course_base('course_base.json', course_base)
                time.sleep(0.5)
                print('\nCalBot: Salamat! May bago akong natutunan!\n')


#Run the CalBot script if it's the main program
if __name__ == '__main__':
    calbot()

#Hi