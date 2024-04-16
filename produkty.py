import json

class Produkt:
    def __init__(self, nazwa, cena, typ, ilosc_godzin=None):
        self.nazwa = nazwa
        self.cena = cena
        self.typ = typ
        self.ilosc_godzin = ilosc_godzin
    
    def __repr__(self):
        return f"Produkt(nazwa='{self.nazwa}', cena={self.cena}, typ='{self.typ}', ilosc_godzin={self.ilosc_godzin})"





def dodaj_produkt(produkt):
    try:
        produkty = odczytaj_dane("produkty.json")
    except FileNotFoundError:
        produkty = []
    produkty.append(produkt)
    zapisz_dane(produkty, "produkty.json")

def usun_produkt(produkt):
    try:
        produkty = odczytaj_dane("produkty.json")
    except FileNotFoundError:
        produkty = []
    produkty = [p for p in produkty if p.nazwa != produkt.nazwa]
    zapisz_dane(produkty, "produkty.json")


def odczytaj_dane(plik):
    try:
        with open(plik, "r") as f:
            dane = json.load(f)
            produkty = [Produkt(p["nazwa"], p["cena"], p["typ"]) for p in dane]
            return produkty
    except (FileNotFoundError, json.JSONDecodeError):
        return []




def zapisz_dane(produkty, plik):
    dane_do_zapisu = [{"nazwa": p.nazwa, "cena": p.cena, "typ": p.typ} for p in produkty]
    with open(plik, "w") as f:
        json.dump(dane_do_zapisu, f, indent=2)


