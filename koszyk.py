import json
from produkty import Produkt

def dodaj_do_koszyka(produkt, ilosc):
    koszyk = odczytaj_dane("koszyk.json")
    znaleziony = False
    for i, (p, _) in enumerate(koszyk):
        if p.nazwa == produkt.nazwa:
            koszyk[i] = (p, koszyk[i][1] + ilosc)
            znaleziony = True
            break
    if not znaleziony:
        koszyk.append((produkt, ilosc))
    zapisz_dane(koszyk, "koszyk.json")


def usun_z_koszyka(produkt):
    koszyk = odczytaj_dane("koszyk.json")
    koszyk = [(p, i) for p, i in koszyk if p.nazwa != produkt.nazwa]
    zapisz_dane(koszyk, "koszyk.json")

def zmien_ilosc_produktu(produkt, nowa_ilosc):
    koszyk = odczytaj_dane("koszyk.json")
    for i, (p, _) in enumerate(koszyk):
        if p.nazwa == produkt.nazwa:
            koszyk[i] = (p, nowa_ilosc)
            break
    zapisz_dane(koszyk, "koszyk.json")

def wyczysc_koszyk():
    zapisz_dane([], "koszyk.json")

def odczytaj_dane(plik):
    try:
        with open(plik, "r") as f:
            try:
                dane = json.load(f)
                koszyk = [(Produkt(p["nazwa"], p["cena"], p.get("typ", "")), p["ilosc"]) for p in dane]
                return koszyk
            except json.JSONDecodeError:
                return []
    except FileNotFoundError:
        return []






def zapisz_dane(koszyk, plik):
    with open(plik, "w") as f:
        json.dump([{"nazwa": p.nazwa, "cena": p.cena, "typ": p.typ, "ilosc": i} for p, i in koszyk], f, indent=2)



def pobierz_zawartosc_koszyka():
    return odczytaj_dane("koszyk.json")

def oblicz_wartosc_koszyka():
    koszyk = odczytaj_dane("koszyk.json")
    wartosc = sum(p.cena * i for p, i in koszyk)
    return wartosc

def pobierz_ilosc_produktu(produkt):
    koszyk = odczytaj_dane("koszyk.json")
    for p, i in koszyk:
        if p.nazwa == produkt.nazwa:
            return i
    return 0

def czy_produkt_w_koszyku(produkt):
    koszyk = odczytaj_dane("koszyk.json")
    for p, _ in koszyk:
        if p.nazwa == produkt.nazwa:
            return True
    return False
