import json
import tkinter as tk
from tkinter import ttk

# Wczytanie danych z pliku JSON
with open('kategorie.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Zapisanie danych do pliku JSON
def save_data():
    with open('kategorie.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# Odświeżenie listy podkategorii
def refresh_subcategories():
    subcategory_listbox.delete(0, tk.END)
    for subcategory in selected_category['podkategorie']:
        subcategory_listbox.insert(tk.END, subcategory['nazwa'])

# Usunięcie wybranej podkategorii
def delete_subcategory():
    selected_subcategory = subcategory_listbox.get(subcategory_listbox.curselection())
    for subcategory in selected_category['podkategorie']:
        if subcategory['nazwa'] == selected_subcategory:
            selected_category['podkategorie'].remove(subcategory)
            break
    refresh_subcategories()
    save_data()

# Dodanie nowej podkategorii
def add_subcategory():
    new_subcategory_name = new_subcategory_entry.get()
    if new_subcategory_name:
        new_subcategory = {'nazwa': new_subcategory_name, 'produkty': []}
        selected_category['podkategorie'].append(new_subcategory)
        refresh_subcategories()
        save_data()
        new_subcategory_entry.delete(0, tk.END)

# Tworzenie okna głównego
window = tk.Tk()
window.title('Kategorie i Podkategorie')

# Tworzenie ramki dla kategorii
category_frame = ttk.Frame(window)
category_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Tworzenie listboxa dla kategorii
category_listbox = tk.Listbox(category_frame)
category_listbox.pack()

# Wypełnienie listboxa kategoriami
for category in data:
    category_listbox.insert(tk.END, category['nazwa'])

# Tworzenie ramki dla podkategorii
subcategory_frame = ttk.Frame(window)
subcategory_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Tworzenie listboxa dla podkategorii
subcategory_listbox = tk.Listbox(subcategory_frame)
subcategory_listbox.pack()

# Tworzenie przycisku usuwania podkategorii
delete_button = ttk.Button(subcategory_frame, text='Usuń podkategorię', command=delete_subcategory)
delete_button.pack(pady=5)

# Tworzenie pola wprowadzania i przycisku dodawania nowej podkategorii
new_subcategory_entry = ttk.Entry(subcategory_frame)
new_subcategory_entry.pack(pady=5)
add_button = ttk.Button(subcategory_frame, text='Dodaj podkategorię', command=add_subcategory)
add_button.pack()

# Funkcja wywoływana po wybraniu kategorii
def on_category_select(event):
    global selected_category
    selected_category_name = category_listbox.get(category_listbox.curselection())
    for category in data:
        if category['nazwa'] == selected_category_name:
            selected_category = category
            break
    refresh_subcategories()

# Przypisanie funkcji do zdarzenia wyboru kategorii
category_listbox.bind('<<ListboxSelect>>', on_category_select)

# Uruchomienie pętli głównej okna
window.mainloop()
