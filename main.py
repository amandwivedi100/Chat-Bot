from difflib import SequenceMatcher
from datetime import datetime
import smtplib
import requests

class Chatbot:
    def __init__(self, name: str, responses: dict[str, str]) -> None:
       self.name = name
       self.responses = responses
       self.weather_api_key = "2286338a207126953e27da67fb258381"


    @staticmethod
    def calculate_similarity(input_sentence: str, response_sentence: str) -> float:
        sequence: SequenceMatcher = SequenceMatcher(a=input_sentence, b=response_sentence)
        return sequence.ratio()


    def get_best_response(self, user_input: str) -> tuple[str, float]:
        highest_similarity: float = 0.0
        best_match: str = "sorry, I didn't understand that"

        for response in self.responses:
            similarity: float = self.calculate_similarity(user_input, response)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match: str = self.responses[response]

        return best_match, highest_similarity


    def get_weather(self, city: str) -> str :
        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric'
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                weather_desc = data['weather'][0]['description']
                temperature = data['main']['temp']
                return f"The weather in {city} is currently {weather_desc} with a temperature of {temperature}°C"
            else:
                return f"Sorry, I couldn't fetch the weather for {city}. Please try again."
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {e}"

    @staticmethod
    def send_email(name: str, sender: str, password: str, receiver: str, subject: str, body: str):
        server = None
        try:
            message: str = f"From: {name} {sender}\nTo: {receiver}\nSubject: {subject}\n\n{body}"

            # Connect to the SMPT server and send the email
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(sender, password)
            print("Logged in to you account, and...")
            server.sendmail(sender, receiver, message)
            print("Email has been sent!")
        except smtplib.SMTPAuthenticationError:
            print("Failed to authenticate. Please check your email and password")
        except smtplib.SMTPException as e:
            print("Failed to send email: ", e)
        finally:
            if server:
                server.quit()
                pass

    def run(self) -> None:
        print(f'Hello! My name is {self.name}, how can I help you today?')
        while True:

                user_input: str = input('You: ')
                response, similarity = self.get_best_response(user_input)

                if similarity < 0.5:
                    response = "Sorry didn't understand that."

                if response == "GET_TIME":
                    response = f'The time is: {datetime.now():%H:%M}'

                if response == "GOODBYES":
                    print(f"{self.name}: Goodbye! have a great Day!")
                    break
                if response == 'EMAIL':
                    name: str = input('Please enter your name: ')
                    sender: str = input('Please enter your email address: ')
                    print(sender)
                    password: str = input('Please enter your password: ')
                    receiver: str = input('Please enter receiver\'s email address: ')
                    subject: str = input('Subject: ')
                    body: str = input('body: ')

                    self.send_email(name=name, sender=sender, password=password, receiver=receiver, subject=subject, body=body)

                if response == 'WEATHER':
                    city: str = input("Please enter the city name: ")
                    response = self.get_weather(city=city)




                print(f'{self.name}: {response} (Similarity: {similarity:.2%})')


def main() -> None:
    response: dict[str, str] = {
        'hello': 'Hello! How are you doing today?',
        'good morning': 'Good morning! Hope you have a great day!',
        'good evening': 'Good evening! How’s your night going?',
        'how are you': 'I’m great, thanks for asking! What about you?',
        'what’s up': 'Not much, just chatting with you!',
        'tell me a joke': 'Why did the computer go to the doctor? It caught a virus!',
        'what’s your name': 'My name is Bob, your friendly chatbot!',
        'who made you': 'I was created by a A-man who loves coding.',
        'what can you do': 'I can chat, tell jokes, give information, and more!',
        'tell me a fun fact': 'Did you know octopuses have three hearts?',
        'do you know about space': 'Yes! Space is vast, mysterious, and full of wonders.',
        'tell me about python': 'Python is a powerful programming language loved by developers.',
        'what time is it': 'GET_TIME',
        'what’s today’s date': f'Today’s date is: {datetime.now():%Y-%m-%d}',
        'set a reminder': 'I can’t do that yet, but maybe in a future update!',
        'what’s the weather': 'Sorry, I can’t check the weather right now.',
        'play some music': 'I’m not a DJ, but I can suggest some songs!',
        'bye': 'GOODBYES',
        'see you later': 'GOODBYES',
        'goodnight': 'GOODBYES',
        'exit': 'GOODBYES',
        'quit': 'GOODBYES',
        'what’s your favorite color': 'I like blue. It’s calming, don’t you think?',
        'what do you eat': 'I survive on binary data!',
        'how do I make a chatbot': 'Start with Python, learn some basics of AI, and build your bot!',
        'what’s AI': 'AI stands for Artificial Intelligence, the science of making machines smart.',
        'send an email': 'EMAIL',
        'thank you': 'Most welcome',
        'weather': 'WEATHER',
    }
    chatbot: Chatbot = Chatbot(name='Bob', responses=response)
    chatbot.run()

if __name__ == '__main__':
    main()
