import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import json

class Kategoria:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.koszty = []

    def dodaj_koszt(self, koszt):
        self.koszty.append(koszt)

    def usun_koszt(self, koszt):
        self.koszty.remove(koszt)

class Koszt:
    def __init__(self, nazwa, kwota, czestotliwosc, plik_pdf=None):
        self.nazwa = nazwa
        self.kwota = kwota
        self.czestotliwosc = czestotliwosc
        self.plik_pdf = plik_pdf

class AplikacjaKosztyFirmowe(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Kalkulator Dziennych Kosztów Firmowych")
        self.geometry("800x600")

        self.kategorie = []

        self.utworz_widgety()
        self.wczytaj_dane()

    def utworz_widgety(self):
        # Ramka dla listy kategorii i przycisków
        ramka_kategorie = ttk.Frame(self)
        ramka_kategorie.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Lista kategorii
        self.lista_kategorii = tk.Listbox(ramka_kategorie)
        self.lista_kategorii.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.lista_kategorii.bind("<<ListboxSelect>>", self.wyswietl_koszty)

        # Przyciski dla kategorii
        ramka_przyciski_kategorie = ttk.Frame(ramka_kategorie)
        ramka_przyciski_kategorie.pack(side=tk.TOP, padx=5, pady=5)

        self.przycisk_dodaj_kategorie = ttk.Button(ramka_przyciski_kategorie, text="Dodaj kategorie", command=self.dodaj_kategorie)
        self.przycisk_dodaj_kategorie.pack(side=tk.LEFT, padx=5)

        self.przycisk_usun_kategorie = ttk.Button(ramka_przyciski_kategorie, text="Usun kategorie", command=self.usun_kategorie)
        self.przycisk_usun_kategorie.pack(side=tk.LEFT, padx=5)

        # Ramka dla listy kosztów i przycisków
        ramka_koszty = ttk.Frame(self)
        ramka_koszty.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Lista kosztów
        self.lista_kosztow = tk.Listbox(ramka_koszty)
        self.lista_kosztow.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Przyciski dla kosztów
        ramka_przyciski_koszty = ttk.Frame(ramka_koszty)
        ramka_przyciski_koszty.pack(side=tk.TOP, padx=5, pady=5)

        self.przycisk_dodaj_koszt = ttk.Button(ramka_przyciski_koszty, text="Dodaj koszt", command=self.dodaj_koszt)
        self.przycisk_dodaj_koszt.pack(side=tk.LEFT, padx=5)

        self.przycisk_usun_koszt = ttk.Button(ramka_przyciski_koszty, text="Usun koszt", command=self.usun_koszt)
        self.przycisk_usun_koszt.pack(side=tk.LEFT, padx=5)

        self.przycisk_wyswietl_pdf = ttk.Button(ramka_przyciski_koszty, text="Wyswietl PDF", command=self.wyswietl_pdf)
        self.przycisk_wyswietl_pdf.pack(side=tk.LEFT, padx=5)

        # Ramka dla podsumowania i pola dni roboczych
        ramka_podsumowanie = ttk.Frame(self)
        ramka_podsumowanie.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Pole dni roboczych
        ramka_dni_robocze = ttk.Frame(ramka_podsumowanie)
        ramka_dni_robocze.pack(side=tk.TOP, padx=5, pady=5)

        etykieta_dni_robocze = ttk.Label(ramka_dni_robocze, text="Dni robocze w roku:")
        etykieta_dni_robocze.pack(side=tk.LEFT)
        self.pole_dni_robocze = ttk.Entry(ramka_dni_robocze, width=10)
        self.pole_dni_robocze.insert(tk.END, "253")  # Domyslna wartosc 253 dni roboczych
        self.pole_dni_robocze.pack(side=tk.LEFT, padx=5)

        # Pole procentu na nieprzewidziane okolicznosci
        ramka_procent_nieprzewidziane = ttk.Frame(ramka_podsumowanie)
        ramka_procent_nieprzewidziane.pack(side=tk.TOP, padx=5, pady=5)

        etykieta_procent_nieprzewidziane = ttk.Label(ramka_procent_nieprzewidziane, text="% na nieprzewidziane okolicznosci:")
        etykieta_procent_nieprzewidziane.pack(side=tk.LEFT)
        self.pole_procent_nieprzewidziane = ttk.Entry(ramka_procent_nieprzewidziane, width=10)
        self.pole_procent_nieprzewidziane.insert(tk.END, "0")  # Domyslna wartosc 0%
        self.pole_procent_nieprzewidziane.pack(side=tk.LEFT, padx=5)

        # Przycisk obliczenia
        self.przycisk_oblicz = ttk.Button(ramka_podsumowanie, text="Oblicz dzienne koszty", command=self.oblicz_dzienne_koszty)
        self.przycisk_oblicz.pack(side=tk.TOP, padx=5, pady=5)

        # Podsumowanie
        self.podsumowanie = ttk.Label(ramka_podsumowanie, text="Dzienne koszty firmowe: 0.00 SEK")
        self.podsumowanie.pack(side=tk.TOP, padx=5, pady=5)

    def wyswietl_koszty(self, event):
        self.odswierz_liste_kosztow()


    def dodaj_kategorie(self):
        nazwa_kategorii = tk.simpledialog.askstring("Dodaj kategorie", "Podaj nazwe kategorii:")
        if nazwa_kategorii:
            nowa_kategoria = Kategoria(nazwa_kategorii)
            self.kategorie.append(nowa_kategoria)
            self.odswierz_liste_kategorii()

    def usun_kategorie(self):
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        if zaznaczona_kategoria:
            self.kategorie.remove(zaznaczona_kategoria)
            self.odswierz_liste_kategorii()
            self.odswierz_liste_kosztow()

    def dodaj_koszt(self):
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        if zaznaczona_kategoria:
            okno_dodaj_koszt = DodajKosztOkno(self)
            self.wait_window(okno_dodaj_koszt)
            if okno_dodaj_koszt.koszt:
                zaznaczona_kategoria.dodaj_koszt(okno_dodaj_koszt.koszt)
                self.odswierz_liste_kosztow()

    def usun_koszt(self):
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        zaznaczony_koszt = self.pobierz_zaznaczony_koszt()
        if zaznaczona_kategoria and zaznaczony_koszt:
            zaznaczona_kategoria.usun_koszt(zaznaczony_koszt)
            self.odswierz_liste_kosztow()

    def wyswietl_pdf(self):
        zaznaczony_koszt = self.pobierz_zaznaczony_koszt()
        if zaznaczony_koszt and zaznaczony_koszt.plik_pdf:
            os.startfile(zaznaczony_koszt.plik_pdf)

    def oblicz_dzienne_koszty(self):
        dni_robocze = int(self.pole_dni_robocze.get())
        procent_nieprzewidziane = float(self.pole_procent_nieprzewidziane.get())
        suma_kosztow = 0
        roczne_koszty_kategorii = {}

        for kategoria in self.kategorie:
            roczne_koszty_kategorii[kategoria.nazwa] = 0
            for koszt in kategoria.koszty:
                if koszt.czestotliwosc == "Rocznie":
                    roczne_koszty_kategorii[kategoria.nazwa] += koszt.kwota
                    suma_kosztow += koszt.kwota
                elif koszt.czestotliwosc == "Miesiecznie":
                    roczne_koszty_kategorii[kategoria.nazwa] += koszt.kwota * 12
                    suma_kosztow += koszt.kwota * 12
                elif koszt.czestotliwosc == "Tygodniowo":
                    roczne_koszty_kategorii[kategoria.nazwa] += koszt.kwota * 52
                    suma_kosztow += koszt.kwota * 52
                elif koszt.czestotliwosc == "Dziennie":
                    roczne_koszty_kategorii[kategoria.nazwa] += koszt.kwota * dni_robocze
                    suma_kosztow += koszt.kwota * dni_robocze

        suma_kosztow *= (1 + procent_nieprzewidziane / 100)
        roczne_koszty = suma_kosztow
        dzienne_koszty = roczne_koszty / dni_robocze

        # Tworzenie podsumowania kosztów
        podsumowanie = f"Dzienne koszty firmowe: {dzienne_koszty:.2f} SEK\nRoczne koszty firmowe: {roczne_koszty:.2f} SEK\n\n"
        for kategoria, roczne_koszty in roczne_koszty_kategorii.items():
            miesieczne_koszty = roczne_koszty / 12
            podsumowanie += f"{kategoria}:\n"
            podsumowanie += f"  Roczne koszty: {roczne_koszty:.2f} SEK\n"
            podsumowanie += f"  Miesięczne koszty: {miesieczne_koszty:.2f} SEK\n"

        self.podsumowanie.config(text=podsumowanie)

        # Zapisz dzienne i roczne koszty do pliku JSON
        self.zapisz_koszty(dzienne_koszty, roczne_koszty)


    def zapisz_koszty(self, dzienne_koszty, roczne_koszty):
        dane = {
            "dzienne_koszty": dzienne_koszty,
            "roczne_koszty": roczne_koszty
        }
        with open("koszty_firmowe.json", "w") as plik:
            json.dump(dane, plik)

    def odswierz_liste_kategorii(self):
        self.lista_kategorii.delete(0, tk.END)
        for kategoria in self.kategorie:
            self.lista_kategorii.insert(tk.END, kategoria.nazwa)

    def odswierz_liste_kosztow(self):
        self.lista_kosztow.delete(0, tk.END)
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        if zaznaczona_kategoria:
            for koszt in zaznaczona_kategoria.koszty:
                self.lista_kosztow.insert(tk.END, f"{koszt.nazwa} - {koszt.kwota} SEK - {koszt.czestotliwosc}")

    def wyswietl_koszty(self, event):
        self.odswierz_liste_kosztow()


    def pobierz_zaznaczona_kategorie(self):
        zaznaczony_indeks = self.lista_kategorii.curselection()
        if zaznaczony_indeks:
            nazwa_kategorii = self.lista_kategorii.get(zaznaczony_indeks)
            for kategoria in self.kategorie:
                if kategoria.nazwa == nazwa_kategorii:
                    return kategoria
        return None

    def pobierz_zaznaczony_koszt(self):
        zaznaczony_indeks = self.lista_kosztow.curselection()
        if zaznaczony_indeks:
            nazwa_kosztu = self.lista_kosztow.get(zaznaczony_indeks).split(" - ")[0]
            zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
            if zaznaczona_kategoria:
                for koszt in zaznaczona_kategoria.koszty:
                    if koszt.nazwa == nazwa_kosztu:
                        return koszt
        return None

    def zapisz_dane(self):
        dane = []
        for kategoria in self.kategorie:
            koszty = []
            for koszt in kategoria.koszty:
                koszty.append({
                    "nazwa": koszt.nazwa,
                    "kwota": koszt.kwota,
                    "czestotliwosc": koszt.czestotliwosc,
                    "plik_pdf": koszt.plik_pdf
                })
            dane.append({
                "nazwa": kategoria.nazwa,
                "koszty": koszty
            })
        with open("dane.json", "w") as plik:
            json.dump(dane, plik)

    def wczytaj_dane(self):
        try:
            with open("dane.json", "r") as plik:
                dane = json.load(plik)
                self.kategorie = []
                for kategoria_data in dane:
                    kategoria = Kategoria(kategoria_data["nazwa"])
                    for koszt_data in kategoria_data["koszty"]:
                        koszt = Koszt(koszt_data["nazwa"], koszt_data["kwota"], koszt_data["czestotliwosc"], koszt_data.get("plik_pdf"))
                        kategoria.dodaj_koszt(koszt)
                    self.kategorie.append(kategoria)
                self.odswierz_liste_kategorii()
        except FileNotFoundError:
            pass

class DodajKosztOkno(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.koszt = None

        self.title("Dodaj koszt")
        self.geometry("400x250")

        self.utworz_widgety()

    def utworz_widgety(self):
        # Pola do wprowadzania danych
        ramka_dane = ttk.Frame(self)
        ramka_dane.pack(padx=10, pady=10)

        etykieta_nazwa = ttk.Label(ramka_dane, text="Nazwa kosztu:")
        etykieta_nazwa.grid(row=0, column=0, sticky=tk.W)
        self.pole_nazwa = ttk.Entry(ramka_dane)
        self.pole_nazwa.grid(row=0, column=1)

        etykieta_kwota = ttk.Label(ramka_dane, text="Kwota (SEK):")
        etykieta_kwota.grid(row=1, column=0, sticky=tk.W)
        self.pole_kwota = ttk.Entry(ramka_dane)
        self.pole_kwota.grid(row=1, column=1)

        etykieta_czestotliwosc = ttk.Label(ramka_dane, text="Czestotliwosc:")
        etykieta_czestotliwosc.grid(row=2, column=0, sticky=tk.W)
        self.pole_czestotliwosc = ttk.Combobox(ramka_dane, values=["Rocznie", "Miesiecznie", "Tygodniowo", "Dziennie"], state="readonly")
        self.pole_czestotliwosc.grid(row=2, column=1)

        etykieta_plik = ttk.Label(ramka_dane, text="Plik PDF:")
        etykieta_plik.grid(row=3, column=0, sticky=tk.W)
        self.pole_plik = ttk.Entry(ramka_dane)
        self.pole_plik.grid(row=3, column=1)
        self.przycisk_wybierz_plik = ttk.Button(ramka_dane, text="Wybierz", command=self.wybierz_plik)
        self.przycisk_wybierz_plik.grid(row=3, column=2)

        # Przycisk dodawania kosztu
        self.przycisk_dodaj = ttk.Button(self, text="Dodaj", command=self.dodaj_koszt)
        self.przycisk_dodaj.pack(pady=10)

    def wybierz_plik(self):
        plik_pdf = filedialog.askopenfilename(filetypes=[("Pliki PDF", "*.pdf")])
        if plik_pdf:
            self.pole_plik.delete(0, tk.END)
            self.pole_plik.insert(tk.END, plik_pdf)

    def dodaj_koszt(self):
        nazwa = self.pole_nazwa.get()
        kwota = float(self.pole_kwota.get())
        czestotliwosc = self.pole_czestotliwosc.get()
        plik_pdf = self.pole_plik.get()

        if nazwa and kwota and czestotliwosc:
            self.koszt = Koszt(nazwa, kwota, czestotliwosc, plik_pdf)
            self.master.zapisz_dane()
            self.destroy()
        else:
            messagebox.showerror("Blad", "Wypelnij wszystkie pola!")

if __name__ == "__main__":
    app = AplikacjaKosztyFirmowe()
    app.mainloop()
