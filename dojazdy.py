import tkinter as tk
from tkinter import ttk
from math import ceil
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import json


class OknoDojazdy(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Oblicz dojazdy")
        self.geometry("400x500")

        self.samochody = [
            {"nazwa": "Samochod 1", "kierowca": "Mateusz", "lokalizacja": "Hasselstigen 3 Älvsjö"},
            {"nazwa": "Samochod 2", "kierowca": "Bronek", "lokalizacja": "Estövägen 5b Nynäshamn"}
        ]
        self.biuro = "Hasselstigen 3 Älvsjö"

        # Odczytaj ostatnio zapisane wartości z pliku konfiguracyjnego
        self.odczytaj_konfiguracje()

        self.utworz_widgety()

    def utworz_widgety(self):
        # Pola do wprowadzania danych
        ramka_dane = ttk.Frame(self)
        ramka_dane.pack(padx=10, pady=10)

        etykieta_adres_klienta = ttk.Label(ramka_dane, text="Adres klienta:")
        etykieta_adres_klienta.grid(row=0, column=0, sticky=tk.W)
        self.pole_adres_klienta = ttk.Entry(ramka_dane)
        self.pole_adres_klienta.grid(row=0, column=1)

        etykieta_stawka_km = ttk.Label(ramka_dane, text="Stawka za km:")
        etykieta_stawka_km.grid(row=1, column=0, sticky=tk.W)
        self.pole_stawka_km = ttk.Entry(ramka_dane)
        self.pole_stawka_km.insert(tk.END, self.ostatnia_stawka_km)
        self.pole_stawka_km.grid(row=1, column=1)

        etykieta_marza = ttk.Label(ramka_dane, text="Marza (%):")
        etykieta_marza.grid(row=2, column=0, sticky=tk.W)
        self.pole_marza = ttk.Entry(ramka_dane)
        self.pole_marza.insert(tk.END, self.ostatnia_marza)
        self.pole_marza.grid(row=2, column=1)

        # Przyciski
        ramka_przyciski = ttk.Frame(self)
        ramka_przyciski.pack(pady=10)

        przycisk_oblicz_opcja1 = ttk.Button(ramka_przyciski, text="Oblicz - kazdy jedzie z domu", command=self.oblicz_opcja1)
        przycisk_oblicz_opcja1.pack(side=tk.LEFT, padx=5)

        przycisk_oblicz_opcja2 = ttk.Button(ramka_przyciski, text="Oblicz - jedziemy razem z biura", command=self.oblicz_opcja2)
        przycisk_oblicz_opcja2.pack(side=tk.LEFT, padx=5)

        przycisk_akceptuj = ttk.Button(ramka_przyciski, text="Akceptuj", command=self.akceptuj_koszt_dojazdu)
        przycisk_akceptuj.pack(side=tk.LEFT, padx=5)

        # Pole wynikowe
        ramka_wynik = ttk.Frame(self)
        ramka_wynik.pack(padx=10, pady=10)

        self.etykieta_wynik = ttk.Label(ramka_wynik, text="")
        self.etykieta_wynik.pack()

        self.etykieta_ilosc_dni = ttk.Label(ramka_wynik, text="")
        self.etykieta_ilosc_dni.pack()

        self.etykieta_dystans_mateusz = ttk.Label(ramka_wynik, text="")
        self.etykieta_dystans_mateusz.pack()

        self.etykieta_dystans_bronek = ttk.Label(ramka_wynik, text="")
        self.etykieta_dystans_bronek.pack()

    def oblicz_opcja1(self):
        adres_klienta = self.pole_adres_klienta.get()
        stawka_km = float(self.pole_stawka_km.get())
        marza = float(self.pole_marza.get())
        
        ilosc_dni = self.master.ilosc_dni_roboczych

        koszt_calkowity = 0
        for samochod in self.samochody:
            lokalizacja = samochod["lokalizacja"]
            dystans = self.oblicz_dystans(lokalizacja, adres_klienta) * 2
            koszt_calkowity += dystans

        koszt_calkowity *= ilosc_dni
        koszt_calkowity *= stawka_km
        koszt_calkowity *= (1 + marza / 100)

        self.etykieta_wynik.config(text=f"Koszt calkowity (kazdy jedzie z domu): {koszt_calkowity:.2f}")
        self.etykieta_ilosc_dni.config(text=f"Ilosc dni (przejazdow): {ilosc_dni:.0f}")

        dystans_mateusz = self.oblicz_dystans(self.samochody[0]["lokalizacja"], adres_klienta)
        self.etykieta_dystans_mateusz.config(text=f"Dystans od Mateusz do klienta: {dystans_mateusz:.2f} km")

        dystans_bronek = self.oblicz_dystans(self.samochody[1]["lokalizacja"], adres_klienta)
        self.etykieta_dystans_bronek.config(text=f"Dystans od Bronek do klienta: {dystans_bronek:.2f} km")

        self.zapisz_konfiguracje()


    def oblicz_opcja2(self):
        adres_klienta = self.pole_adres_klienta.get()
        stawka_km = float(self.pole_stawka_km.get())
        marza = float(self.pole_marza.get())
        
        ilosc_dni = self.master.ilosc_dni_roboczych

        koszt_calkowity = 0
        for samochod in self.samochody:
            lokalizacja = samochod["lokalizacja"]
            dystans_do_biura = self.oblicz_dystans(lokalizacja, self.biuro) * 2
            koszt_calkowity += dystans_do_biura

        dystans_do_klienta = self.oblicz_dystans(self.biuro, adres_klienta) * 2
        koszt_calkowity += dystans_do_klienta

        koszt_calkowity *= ilosc_dni
        koszt_calkowity *= stawka_km
        koszt_calkowity *= (1 + marza / 100)

        self.etykieta_wynik.config(text=f"Koszt calkowity (jedziemy razem z biura): {koszt_calkowity:.2f}")
        self.etykieta_ilosc_dni.config(text=f"Ilosc dni (przejazdow): {ilosc_dni:.0f}")

        dystans_mateusz = self.oblicz_dystans(self.samochody[0]["lokalizacja"], self.biuro)
        self.etykieta_dystans_mateusz.config(text=f"Dystans od Mateusz do biura: {dystans_mateusz:.2f} km")

        dystans_bronek = self.oblicz_dystans(self.samochody[1]["lokalizacja"], self.biuro)
        self.etykieta_dystans_bronek.config(text=f"Dystans od Bronek do biura: {dystans_bronek:.2f} km")

        self.zapisz_konfiguracje()


    def oblicz_dystans(self, adres1, adres2):
        geolocator = Nominatim(user_agent="my-app")
        location1 = geolocator.geocode(adres1)
        location2 = geolocator.geocode(adres2)

        if location1 and location2:
            coords1 = (location1.latitude, location1.longitude)
            coords2 = (location2.latitude, location2.longitude)
            dystans = geodesic(coords1, coords2).kilometers
            return dystans
        else:
            return 0

    def potwierdz_obliczenia(self):
        koszt_calkowity = float(self.etykieta_wynik.cget("text").split(":")[1])
        self.master.dodaj_koszt_dojazdu(koszt_calkowity)
        self.destroy()


    def odczytaj_konfiguracje(self):
        try:
            with open("konfiguracja_dojazdy.json", "r") as plik:
                konfiguracja = json.load(plik)
                self.ostatnia_stawka_km = konfiguracja.get("stawka_km", "")
                self.ostatnia_marza = konfiguracja.get("marza", "")
        except FileNotFoundError:
            self.ostatnia_stawka_km = ""
            self.ostatnia_marza = ""

    def zapisz_konfiguracje(self):
        konfiguracja = {
            "stawka_km": self.pole_stawka_km.get(),
            "marza": self.pole_marza.get()
        }
        with open("konfiguracja_dojazdy.json", "w") as plik:
            json.dump(konfiguracja, plik)

    def akceptuj_koszt_dojazdu(self):
        koszt_calkowity = float(self.etykieta_wynik.cget("text").split(":")[1])
        self.master.dodaj_koszt_dojazdu(koszt_calkowity)
        self.destroy()

