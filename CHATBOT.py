from flask import Flask, send_file, request
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import urllib.request
import re
import datetime
import webbrowser
import time
import google.generativeai as genai

genai.configure(api_key= "AIzaSyDCI6bpd_aCkG5uSW82lh1VK8WpDKpjoVs")
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name,padding_side='left')
model = AutoModelForCausalLM.from_pretrained(model_name)
def NLP(prompt):
    for step in range(1):
        input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors="pt")
        bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 0 else input_ids
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            do_sample=True,
            top_p=0.95,
            top_k=0,
            temperature=0.75,
            pad_token_id=tokenizer.eos_token_id
        )
        output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"DialoGPT: {output}")
    return output

def youtubePlay(song_name):
    song_split = song_name.split()
    song_link = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + "+".join(song_split))
    videos = re.findall(r"watch\?v=(\S{11})", song_link.read().decode())
    link = "https://www.youtube.com/watch?v=" + videos[0]
    webbrowser.open(link)

def wantToContinue():
    while True:
        return ("Do you want to continue using this program?")
        ask = takeCommand().lower()
        ask = ask.split()
        if "yes" in ask:
            break
        elif "no" in ask:
            return ("Ok I will end the program now.")
            exit()

def googleSearch(search):
        words = search.split()
        search = ""
        for i in words:
            search += i + "+"
        link = f"https://www.google.com/search?q={search}&oq={search}&aqs=chrome..69i57j69i60l3.8525j0j1&sourceid=chrome&ie=UTF-8"

        time.sleep(1)
        webbrowser.open(link)
def openingWebsite(prompt):
    website = prompt.removeprefix("open ")
    link2 = website + ".com"
    webbrowser.open(link2)
    return (f"opening {website}")

def tellingTime(prompt):
    hour = int(datetime.datetime.now().hour)
    minutes = int(datetime.datetime.now().minute)
    return (f"The time is {hour}:{minutes}")


def BARD(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Answer in Short as an assistant." + prompt)
    return response.text

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    data = request.get_json()
    if 'text' in data:
        input_text = data['text']
        query = input_text
        if query == "surprise me":
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            wantToContinue()
        elif "open " in query:
            openingWebsite()
            response = wantToContinue()
        if "weather" in query:
            webbrowser.open("https://www.google.com/search?q=weather+today&sca_esv=587470601&rlz=1C1ONGR_enIN1060IN1060&sxsrf=AM9HkKlVaNZIJhiCo0uDXmTurT-w63ObwA%3A1701611905088&ei=gYlsZbj5BISSseMPwe-9sAk&ved=0ahUKEwj4vZeptvOCAxUESWwGHcF3D5YQ4dUDCBA&uact=5&oq=weather+today&gs_lp=Egxnd3Mtd2l6LXNlcnAiDXdlYXRoZXIgdG9kYXkyChAAGEcY1gQYsAMyChAAGEcY1gQYsAMyChAAGEcY1gQYsAMyChAAGEcY1gQYsAMyChAAGEcY1gQYsAMyChAAGEcY1gQYsAMyChAAGEcY1gQYsAMyChAAGEcY1gQYsAMyDRAAGIAEGIoFGEMYsAMyDRAAGIAEGIoFGEMYsANIgU5QlQ1YpTVwBXgBkAEBmAG0BKABwhOqAQgwLjE0LjUtMbgBA8gBAPgBAagCFMICBxAjGOoCGCfCAhMQABiABBiKBRhDGOoCGLQC2AEBwgIUEAAYgAQY4wQY6QQY6gIYtALYAQHCAg0QIxiABBiKBRgnGJ0CwgIKECMYgAQYigUYJ8ICEBAAGIAEGIoFGEMYsQMYgwHCAg0QABiABBiKBRhDGLEDwgIKEAAYgAQYigUYQ8ICBRAAGIAEwgITEAAYgAQYigUYQxixAxiDARjJA8ICCxAAGIAEGIoFGJIDwgIIEAAYgAQYsQPCAhIQIxiABBiKBRgnGJ0CGEYYgALCAhwQABiABBiKBRidAhhGGIACGJcFGIwFGN0E2AECwgIUEAAYgAQYigUYkQIYsQMYgwEYyQPCAg8QIxixAhgnGJ0CGEYYgALCAg4QABiABBiKBRiRAhixA8ICERAAGIAEGIoFGJECGLEDGIMBwgIKEAAYgAQYsQMYCsICBxAAGIAEGArCAhkQABixAhidAhhGGIACGJcFGIwFGN0E2AECwgILEAAYgAQYigUYkQLCAggQABiABBiSA8ICChAAGIAEGJIDGAriAwQYACBBiAYBkAYKugYGCAEQARgBugYGCAIQARgT&sclient=gws-wiz-serp")
            response = "Here's the weather for today"
        elif "search " in query:
            search = query.removeprefix("search ")
            response = (f"Now searching {search}")
            googleSearch(search)
            wantToContinue()
        elif "play" in query:
            song_name = query.removeprefix("play ")
            youtubePlay(song_name)
            response = (f"Now playing {song_name}")
            wantToContinue()
        elif "stop" in query:
            response = ("Thank you for using me.")
            exit()
        elif "time" in query:
            response = tellingTime()
        elif "what" in query:
            response = BARD(query)
        elif "why" in query:
            print("Wait a few seconds please...")
            response = BARD(query)
        elif "when" in query:
            response = BARD(query)
        elif "where" in query:
            response = BARD(query)
        elif "how" in query:
            response = BARD(query)
        elif "who" in query:
            response = BARD(query)
        elif "which" in query:
            response = BARD(query)
        else:
            response = NLP(query)

        return response
    else:
        return "Sorry, could not understand audio."

if __name__ == '__main__':
    app.run(debug=True)
