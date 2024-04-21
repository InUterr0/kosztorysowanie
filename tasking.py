import tkinter as tk
from tkinter import scrolledtext
import taskingai
from taskingai.inference import chat_completion, SystemMessage, UserMessage

# Inicjalizacja Tasking AI
taskingai.init(api_key='taMbvJes5N8Xu6sd3F0IWM9KCGWlf7XU')

# ID modelu
MODEL_ID = 'your_model_id'

# Funkcja do wysyłania wiadomości i otrzymywania odpowiedzi
def send_message():
    message = user_input.get()
    chat_history.insert(tk.END, "You: " + message + "\n")
    user_input.delete(0, tk.END)

    response = chat_completion(
        model_id=MODEL_ID,
        messages=[
            SystemMessage("You are a professional assistant."),
            UserMessage(message),
        ]
    )
    chat_history.insert(tk.END, "Assistant: " + response.response + "\n")

# Tworzenie głównego okna
window = tk.Tk()
window.title("Chat with TaskingAI Assistant")

# Tworzenie pola tekstowego do wyświetlania historii czatu
chat_history = scrolledtext.ScrolledText(window, width=50, height=20)
chat_history.pack(pady=10)

# Tworzenie pola do wprowadzania wiadomości
user_input = tk.Entry(window, width=50)
user_input.pack(pady=5)

# Tworzenie przycisku do wysyłania wiadomości
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# Uruchomienie pętli głównej interfejsu
window.mainloop()