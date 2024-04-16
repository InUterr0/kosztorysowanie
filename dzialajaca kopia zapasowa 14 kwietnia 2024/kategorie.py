import json
from produkty import Produkt


class Kategoria:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.podkategorie = []

    def dodaj_podkategorie(self, podkategoria):
        self.podkategorie.append(podkategoria)

    def usun_podkategorie(self, podkategoria):
        self.podkategorie.remove(podkategoria)

    def znajdz_podkategorie(self, nazwa):
        for podkategoria in self.podkategorie:
            if podkategoria.nazwa == nazwa:
                return podkategoria
        return None

    def dodaj_produkt(self, produkt):
        for podkategoria in self.podkategorie:
            podkategoria.dodaj_produkt(produkt)


class Podkategoria:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.produkty = []

    def dodaj_produkt(self, produkt):
        self.produkty.append(produkt)

    def usun_produkt(self, produkt):
        self.produkty.remove(produkt)

    def znajdz_produkt(self, nazwa):
        for produkt in self.produkty:
            if produkt.nazwa == nazwa:
                return produkt
        return None





    def __repr__(self):
        return f"Kategoria(nazwa='{self.nazwa}', produkty={self.produkty})"


def dodaj_kategorie(kategoria):
    kategorie = odczytaj_dane("kategorie.json")
    kategorie.append(kategoria)
    zapisz_dane(kategorie, "kategorie.json")

def usun_kategorie(kategoria):
    kategorie = odczytaj_dane("kategorie.json")
    kategorie = [k for k in kategorie if k.nazwa != kategoria.nazwa]
    zapisz_dane(kategorie, "kategorie.json")

def odczytaj_dane(plik):
    try:
        with open(plik, "r") as f:
            dane = json.load(f)
            kategorie = []
            for k in dane:
                kategoria = Kategoria(k["nazwa"])
                podkategorie = [Podkategoria(pk["nazwa"]) for pk in k["podkategorie"]]
                kategoria.podkategorie = podkategorie
                kategorie.append(kategoria)
            return kategorie
    except (FileNotFoundError, json.JSONDecodeError):
        return []





def zapisz_dane(kategorie, plik):
    print(f"Zapisywanie danych do pliku '{plik}'")
    print(f"Kategorie do zapisu: {kategorie}")
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
    print(f"Dane do zapisu: {dane_do_zapisu}")
    with open(plik, "w") as f:
        json.dump(dane_do_zapisu, f, indent=2)
    print(f"Dane zapisane do pliku '{plik}'")


class Podkategoria:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.produkty = []

    def dodaj_produkt(self, produkt):
        self.produkty.append(produkt)

    def usun_produkt(self, produkt):
        self.produkty.remove(produkt)

    def znajdz_produkt(self, nazwa):
        for produkt in self.produkty:
            if produkt.nazwa == nazwa:
                return produkt
        return None

def utworz_kategorie(nazwa):
    return Kategoria(nazwa)

def utworz_podkategorie(nazwa):
    return Podkategoria(nazwa)

def dodaj_podkategorie_do_kategorii(kategoria, podkategoria):
    kategoria.dodaj_podkategorie(podkategoria)

def usun_podkategorie_z_kategorii(kategoria, podkategoria):
    kategoria.usun_podkategorie(podkategoria)

def wyswietl_kategorie(kategorie):
    print("Kategorie:")
    for kategoria in kategorie:
        print(f"- {kategoria.nazwa}")
        kategoria.wyswietl_podkategorie()
        print()

def znajdz_kategorie(kategorie, nazwa):
    for kategoria in kategorie:
        if kategoria.nazwa == nazwa:
            return kategoria
    return None

def znajdz_podkategorie(kategoria, nazwa):
    return kategoria.znajdz_podkategorie(nazwa)

def zmien_nazwe_kategorii(kategoria, nowa_nazwa):
    kategoria.zmien_nazwe(nowa_nazwa)

def zmien_nazwe_podkategorii(podkategoria, nowa_nazwa):
    podkategoria.zmien_nazwe(nowa_nazwa)

