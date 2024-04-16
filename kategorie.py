import json
from produkty import Produkt

class Kategoria:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.podkategorie = []

    def dodaj_podkategorie(self, podkategoria):
        self.podkategorie.append(podkategoria)

    def znajdz_podkategorie(self, nazwa):
        for podkategoria in self.podkategorie:
            if podkategoria.nazwa == nazwa:
                return podkategoria
        return None

class Podkategoria:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.produkty = []

    def dodaj_produkt(self, produkt):
        self.produkty.append(produkt)

    def usun_produkt(self, produkt):
        self.produkty = [p for p in self.produkty if p.nazwa != produkt.nazwa]

    def znajdz_produkt(self, nazwa):
        for produkt in self.produkty:
            if produkt.nazwa == nazwa:
                return produkt
        return None

def odczytaj_dane(plik):
    try:
        with open(plik, "r") as f:
            dane = json.load(f)
            kategorie = []
            for k in dane:
                kategoria = Kategoria(k["nazwa"])
                podkategorie = [Podkategoria(pk["nazwa"]) for pk in k["podkategorie"]]
                for i, pk in enumerate(k["podkategorie"]):
                    if "produkty" in pk:
                        produkty = [Produkt(p["nazwa"], p["cena"], p["typ"]) for p in pk["produkty"]]
                        podkategorie[i].produkty = produkty
                kategoria.podkategorie = podkategorie
                kategorie.append(kategoria)
            return kategorie
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def zapisz_dane(kategorie, plik):
    dane_do_zapisu = [
        {
            "nazwa": k.nazwa,
            "podkategorie": [
                {
                    "nazwa": pk.nazwa,
                    "produkty": [{"nazwa": p.nazwa, "cena": p.cena, "typ": p.typ} for p in pk.produkty]
                }
                for pk in k.podkategorie
            ]
        }
        for k in kategorie
    ]
    with open(plik, "w") as f:
        json.dump(dane_do_zapisu, f, indent=2)

def dodaj_kategorie(kategoria):
    kategorie = odczytaj_dane("kategorie.json")
    kategorie.append(kategoria)
    zapisz_dane(kategorie, "kategorie.json")

def usun_kategorie(kategoria):
    kategorie = odczytaj_dane("kategorie.json")
    kategorie = [k for k in kategorie if k.nazwa != kategoria.nazwa]
    zapisz_dane(kategorie, "kategorie.json")

def dodaj_podkategorie(kategoria, podkategoria):
    kategorie = odczytaj_dane("kategorie.json")
    for k in kategorie:
        if k.nazwa == kategoria.nazwa:
            k.dodaj_podkategorie(podkategoria)
            break
    zapisz_dane(kategorie, "kategorie.json")

def usun_podkategorie(kategoria, podkategoria):
    kategorie = odczytaj_dane("kategorie.json")
    for k in kategorie:
        if k.nazwa == kategoria.nazwa:
            k.podkategorie = [pk for pk in k.podkategorie if pk.nazwa != podkategoria.nazwa]
            zapisz_dane(kategorie, "kategorie.json")
            return
    print(f"Błąd: Kategoria {kategoria.nazwa} nie została znaleziona.")

def znajdz_kategorie(nazwa):
    kategorie = odczytaj_dane("kategorie.json")
    for kategoria in kategorie:
        if kategoria.nazwa == nazwa:
            return kategoria
    return None

def znajdz_podkategorie(kategoria, nazwa):
    for podkategoria in kategoria.podkategorie:
        if podkategoria.nazwa == nazwa:
            return podkategoria
    return None