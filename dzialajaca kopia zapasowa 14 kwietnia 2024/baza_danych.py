import json
from kategorie import Kategoria
from produkty import Produkt
from kategorie import Kategoria, Podkategoria


def odczytaj_dane(plik):
    try:
        with open(plik, "r") as f:
            dane = json.load(f)
            if plik == "kategorie.json":
                kategorie = []
                for k in dane:
                    kategoria = Kategoria(k["nazwa"])
                    if "podkategorie" in k:
                        podkategorie = [Podkategoria(pk["nazwa"]) for pk in k["podkategorie"]]
                        for i, pk in enumerate(k["podkategorie"]):
                            if "produkty" in pk:
                                produkty = [Produkt(p["nazwa"], p["cena"], p["typ"]) for p in pk["produkty"]]
                                podkategorie[i].produkty = produkty
                        kategoria.podkategorie = podkategorie
                    kategorie.append(kategoria)
                return kategorie
            elif plik == "koszyk.json":
                return [(Produkt(p["nazwa"], p["cena"], p["typ"]), p["ilosc"]) for p in dane]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def zapisz_dane(dane, plik):
    if plik == "kategorie.json":
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
            for k in dane
        ]
    elif plik == "koszyk.json":
        dane_do_zapisu = [{"nazwa": p.nazwa, "cena": p.cena, "typ": p.typ, "ilosc": i} for p, i in dane]
    else:
        raise ValueError("Nieznany plik")

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

def dodaj_produkt(produkt):
    produkty = odczytaj_dane("produkty.json")
    produkty.append(produkt)
    zapisz_dane(produkty, "produkty.json")

def usun_produkt(produkt):
    produkty = odczytaj_dane("produkty.json")
    produkty = [p for p in produkty if p.nazwa != produkt.nazwa]
    zapisz_dane(produkty, "produkty.json")

def pobierz_kategorie():
    return odczytaj_dane("kategorie.json")

def pobierz_produkty():
    return odczytaj_dane("produkty.json")

def pobierz_produkty_z_kategorii(kategoria):
    produkty = odczytaj_dane("produkty.json")
    return [p for p in produkty if p.kategoria == kategoria]

def zmien_nazwe_kategorii(stara_kategoria, nowa_kategoria):
    kategorie = odczytaj_dane("kategorie.json")
    for i, k in enumerate(kategorie):
        if k.nazwa == stara_kategoria.nazwa:
            kategorie[i] = nowa_kategoria
            break
    zapisz_dane(kategorie, "kategorie.json")

def zmien_nazwe_produktu(stary_produkt, nowy_produkt):
    produkty = odczytaj_dane("produkty.json")
    for i, p in enumerate(produkty):
        if p.nazwa == stary_produkt.nazwa:
            produkty[i] = nowy_produkt
            break
    zapisz_dane(produkty, "produkty.json")

def zmien_cene_produktu(produkt, nowa_cena):
    produkty = odczytaj_dane("produkty.json")
    for i, p in enumerate(produkty):
        if p.nazwa == produkt.nazwa:
            produkty[i].cena = nowa_cena
            break
    zapisz_dane(produkty, "produkty.json")
