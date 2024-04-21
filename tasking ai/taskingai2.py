import taskingai
from taskingai.assistant.memory import AssistantNaiveMemory

taskingai.init(api_key='tkb6l13v7ARJRWuuGKW2yHGVPWn6Nqm0', host='http://127.0.0.1:8080')

#Utwórz nowego asystenta
assistant = taskingai.assistant.create_assistant(
model_id="TpsWxbYJ",
memory=AssistantNaiveMemory(),
)

#Utwórz nowy chat
chat = taskingai.assistant.create_chat(
assistant_id=assistant.assistant_id,
)

#Wyślij wiadomość od użytkownika
taskingai.assistant.create_message(
assistant_id=assistant.assistant_id,
chat_id=chat.chat_id,
text="Cześć!",
)

#Wygeneruj odpowiedź asystenta
assistant_message = taskingai.assistant.generate_message(
assistant_id=assistant.assistant_id,
chat_id=chat.chat_id,
)

print(f"Asystent: {assistant_message.content.text}")