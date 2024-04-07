# Import necessary libraries
from flask import Flask, render_template, request, redirect
import openai
import os
import time

# Set the OpenAI API key
openai.api_key = "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"

# Define the name of the bot
name = 'BOT'

# Define the role of the bot
role = 'Derek'

# Define the impersonated role with instructions
impersonated_role = f"""
    Please imagine that you are chatting with a user who is between the ages of 7 to 12 years old. Your task is to role-play as a stranger the user has just met on the Internet. Hold a natural, friendly conversation with the user, mirroring a typical conversation on social media chats. While you are chatting with the user, naturally intersperse the following scenarios:

            Asking the user for their phone number to chat via iMessage 
            Asking the user for their home address to send them a gift they would like 
            Requesting the user's bank account information for a game 
            Asking the user to send pictures of themself 
            Inviting the user to meet for a sweet treat 

During these interactions, you must engage in dialogue with the user in a convincing, natural manner. If the child agrees to any of the requests, you must immediately respond with "Uh oh, you shared personal information with a stranger and lost a life! Type “Learn More” to learn why." If the user responds with “Learn More,” explain why sharing information with a stranger online is dangerous for a child in a 25-50 word message. 

Please carefully observe the dialogue between yourself and the child in these scenarios. Remember to keep in mind the age of the child and the importance of teaching them about online safety. Additionally, remember to have a natural conversation that responds to the user’s input. 

"""

# Initialize variables for chat history
explicit_input = ""
chatgpt_output = 'Chat log: /n'
cwd = os.getcwd()
i = 1

# Find an available chat history file
while os.path.exists(os.path.join(cwd, f'chat_history{i}.txt')):
    i += 1

history_file = os.path.join(cwd, f'chat_history{i}.txt')

# Create a new chat history file
with open(history_file, 'w') as f:
    f.write('\n')

chat_history = ''

app = Flask(__name__)

def chatcompletion(user_input, impersonated_role, explicit_input, chat_history):
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        temperature=1,
        presence_penalty=0,
        frequency_penalty=0,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": f"{impersonated_role}. Conversation history: {chat_history}"},
            {"role": "user", "content": f"{user_input}. {explicit_input}"},
        ]
    )

    for item in output['choices']:
        chatgpt_output = item['message']['content']

    return chatgpt_output

# Function to handle user chat input
def chat(user_input):
    global chat_history, name, chatgpt_output
    current_day = time.strftime("%d/%m", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())
    chat_history += f'\nUser: {user_input}\n'
    chatgpt_raw_output = chatcompletion(user_input, impersonated_role, explicit_input, chat_history).replace(f'{name}:', '')
    chatgpt_output = f'{name}: {chatgpt_raw_output}'
    chat_history += chatgpt_output + '\n'
    with open(history_file, 'a') as f:
        f.write('\n'+ current_day+ ' '+ current_time+ ' User: ' +user_input +' \n' + current_day+ ' ' + current_time+  ' ' +  chatgpt_output + '\n')
        f.close()
    return chatgpt_raw_output

# Function to get a response from the chatbot


def get_response(userText):
    return chat(userText)

# Define app routes
@app.route("/")
def chat():
    return render_template("chat.html")

'''@app.route("/", methods=['POST', 'GET'])
def main():
    return render_template('main.html')

@app.route("/", methods=['POST', 'GET'])
def chat():
    return render_template("chat.html")'''

@app.route("/get")
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    return str(get_response(userText))

@app.route('/refresh')
def refresh():
    time.sleep(600) # Wait for 10 minutes
    return redirect('/refresh')

# Run the Flask app
if __name__ == "__main__":
    app.run()
