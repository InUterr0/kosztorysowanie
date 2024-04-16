import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from produkty import Produkt
from tkinter import simpledialog
from kategorie import Kategoria, dodaj_kategorie, usun_kategorie
from kategorie import Kategoria, Podkategoria, usun_podkategorie
from produkty import Produkt, dodaj_produkt, usun_produkt
from koszyk import dodaj_do_koszyka, usun_z_koszyka, wyczysc_koszyk, pobierz_zawartosc_koszyka, oblicz_wartosc_koszyka
from baza_danych import odczytaj_dane, zapisz_dane
from kategorie import Kategoria, Podkategoria
from dojazdy import OknoDojazdy
import json
from kategorie import znajdz_podkategorie
from kategorie import usun_podkategorie_z_kategorii




class Aplikacja(tk.Tk):
    def __init__(self):
        super().__init__()

        self.wybrana_kategoria = None
        self.wybrana_podkategoria = None
        self.title("Aplikacja do kosztorysowania")
        self.geometry("800x600")

        # Ramka dla kategorii, podkategorii i produktów
        self.ramka_kategorie_produkty = ttk.Frame(self)
        self.ramka_kategorie_produkty.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Odczytaj ostatnio zapisane wartosci z pliku konfiguracyjnego
        self.odczytaj_konfiguracje()

        self.utworz_widgety()

    def utworz_widgety(self):
        # Ramka dla kategorii
        ramka_kategorie = ttk.Frame(self.ramka_kategorie_produkty)
        ramka_kategorie.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=False)

        # Drzewo kategorii
        self.drzewo_kategorie = ttk.Treeview(ramka_kategorie)
        self.drzewo_kategorie.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.drzewo_kategorie.bind("<<TreeviewSelect>>", self.wyswietl_produkty)

        # Przyciski dla kategorii
        ramka_przyciski_kategorie = ttk.Frame(ramka_kategorie)
        ramka_przyciski_kategorie.pack(side=tk.TOP, padx=5, pady=5)

        self.przycisk_dodaj_kategorie = ttk.Button(ramka_przyciski_kategorie, text="Dodaj kategorie", command=self.dodaj_kategorie)
        self.przycisk_dodaj_kategorie.pack(side=tk.LEFT, padx=5)

        self.przycisk_usun_kategorie = ttk.Button(ramka_przyciski_kategorie, text="Usun kategorie", command=self.usun_kategorie)
        self.przycisk_usun_kategorie.pack(side=tk.LEFT, padx=5)

        # Ramka dla podkategorii i produktów
        ramka_produkty = ttk.Frame(self.ramka_kategorie_produkty)
        ramka_produkty.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Drzewo podkategorii
        self.drzewo_podkategorie = ttk.Treeview(ramka_produkty, height=5)
        self.drzewo_podkategorie.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X, expand=False)
        self.drzewo_podkategorie.bind("<<TreeviewSelect>>", self.wyswietl_produkty_podkategorii)

        # Przyciski dla podkategorii
        ramka_przyciski_podkategorie = ttk.Frame(ramka_produkty)
        ramka_przyciski_podkategorie.pack(side=tk.TOP, padx=5, pady=5)

        self.przycisk_dodaj_podkategorie = ttk.Button(ramka_przyciski_podkategorie, text="Dodaj podkategorie", command=self.dodaj_podkategorie)
        self.przycisk_dodaj_podkategorie.pack(side=tk.LEFT, padx=5)

        self.przycisk_usun_podkategorie = ttk.Button(ramka_przyciski_podkategorie, text="Usun podkategorie", command=self.usun_podkategorie)
        self.przycisk_usun_podkategorie.pack(side=tk.LEFT, padx=5)

        # Lista produktów
        self.lista_produkty = tk.Listbox(ramka_produkty)
        self.lista_produkty.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Reszta kodu...

        # Przyciski dla produktów
        ramka_przyciski_produkty = ttk.Frame(ramka_produkty)
        ramka_przyciski_produkty.pack(side=tk.TOP, padx=5, pady=5)

        self.przycisk_dodaj_produkt = ttk.Button(ramka_przyciski_produkty, text="Dodaj produkt", command=self.dodaj_produkt)
        self.przycisk_dodaj_produkt.pack(side=tk.LEFT, padx=5)

        self.przycisk_usun_produkt = ttk.Button(ramka_przyciski_produkty, text="Usun produkt", command=self.usun_produkt)
        self.przycisk_usun_produkt.pack(side=tk.LEFT, padx=5)

        # Ramka dla koszyka i podsumowania
        ramka_koszyk_podsumowanie = ttk.Frame(self)
        ramka_koszyk_podsumowanie.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Lista koszyka
        self.lista_koszyk = tk.Listbox(ramka_koszyk_podsumowanie)
        self.lista_koszyk.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Przyciski dla koszyka
        ramka_przyciski_koszyk = ttk.Frame(ramka_koszyk_podsumowanie)
        ramka_przyciski_koszyk.pack(side=tk.TOP, padx=5, pady=5)

        self.przycisk_dodaj_do_koszyka = ttk.Button(ramka_przyciski_koszyk, text="Dodaj do koszyka", command=self.dodaj_do_koszyka)
        self.przycisk_dodaj_do_koszyka.pack(side=tk.LEFT, padx=5)

        self.przycisk_usun_z_koszyka = ttk.Button(ramka_przyciski_koszyk, text="Usun z koszyka", command=self.usun_z_koszyka)
        self.przycisk_usun_z_koszyka.pack(side=tk.LEFT, padx=5)

        self.przycisk_wyczysc_koszyk = ttk.Button(ramka_przyciski_koszyk, text="Wyczysc koszyk", command=self.wyczysc_koszyk)
        self.przycisk_wyczysc_koszyk.pack(side=tk.LEFT, padx=5)

        # Podsumowanie
        self.podsumowanie = ttk.Label(ramka_koszyk_podsumowanie, text="Podsumowanie: 0.00")
        self.podsumowanie.pack(side=tk.BOTTOM, padx=5, pady=5)

        # Pola do wprowadzania marzy
        ramka_marza = ttk.Frame(ramka_koszyk_podsumowanie)
        ramka_marza.pack(side=tk.TOP, padx=5, pady=5)

        etykieta_marza_robocizna = ttk.Label(ramka_marza, text="Marza na robociznie (%):")
        etykieta_marza_robocizna.pack(side=tk.LEFT)
        self.marza_robocizna_var = tk.StringVar(value=self.ostatnia_marza_robocizna)
        self.marza_robocizna_var.trace("w", self.odswierz_podsumowanie)
        self.pole_marza_robocizna = ttk.Entry(ramka_marza, width=10, textvariable=self.marza_robocizna_var)
        self.pole_marza_robocizna.pack(side=tk.LEFT, padx=5)

        etykieta_marza_material = ttk.Label(ramka_marza, text="Marza na materialach (%):")
        etykieta_marza_material.pack(side=tk.LEFT)
        self.marza_material_var = tk.StringVar(value=self.ostatnia_marza_material)
        self.marza_material_var.trace("w", self.odswierz_podsumowanie)
        self.pole_marza_material = ttk.Entry(ramka_marza, width=10, textvariable=self.marza_material_var)
        self.pole_marza_material.pack(side=tk.LEFT, padx=5)

        etykieta_marza_podwykonawca = ttk.Label(ramka_marza, text="Marza na podwykonawcach (%):")
        etykieta_marza_podwykonawca.pack(side=tk.LEFT)
        self.marza_podwykonawca_var = tk.StringVar(value=self.ostatnia_marza_podwykonawca)
        self.marza_podwykonawca_var.trace("w", self.odswierz_podsumowanie)
        self.pole_marza_podwykonawca = ttk.Entry(ramka_marza, width=10, textvariable=self.marza_podwykonawca_var)
        self.pole_marza_podwykonawca.pack(side=tk.LEFT, padx=5)

        # Pole do wprowadzania dziennej mocy przerobowej
        ramka_moc_przerobowa = ttk.Frame(ramka_koszyk_podsumowanie)
        ramka_moc_przerobowa.pack(side=tk.TOP, padx=5, pady=5)

        etykieta_moc_przerobowa = ttk.Label(ramka_moc_przerobowa, text="Dzienna moc przerobowa (godziny):")
        etykieta_moc_przerobowa.pack(side=tk.LEFT)
        self.moc_przerobowa_var = tk.StringVar(value=self.ostatnia_moc_przerobowa)
        self.moc_przerobowa_var.trace("w", self.odswierz_podsumowanie)
        self.pole_moc_przerobowa = ttk.Entry(ramka_moc_przerobowa, width=10, textvariable=self.moc_przerobowa_var)
        self.pole_moc_przerobowa.pack(side=tk.LEFT, padx=5)

        # Przycisk "Oblicz dojazdy"
        przycisk_oblicz_dojazdy = ttk.Button(ramka_przyciski_koszyk, text="Oblicz dojazdy", command=self.oblicz_dojazdy)
        przycisk_oblicz_dojazdy.pack(side=tk.LEFT, padx=5)

        self.odswierz_widgety()

    def wyswietl_podkategorie(self, event):
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        if zaznaczona_kategoria:
            self.drzewo_podkategorie.delete(*self.drzewo_podkategorie.get_children())
            for podkategoria in zaznaczona_kategoria.podkategorie:
                self.drzewo_podkategorie.insert("", "end", text=podkategoria.nazwa)
        else:
            self.drzewo_podkategorie.delete(*self.drzewo_podkategorie.get_children())

    def zaznacz_podkategorie(self, event):
        zaznaczone = self.drzewo_podkategorie.selection()
        if zaznaczone:
            nazwa_podkategorii = self.drzewo_podkategorie.item(zaznaczone[0], "text")
            self.wybrana_podkategoria = self.znajdz_podkategorie(nazwa_podkategorii)
        else:
            self.wybrana_podkategoria = None

    def usun_podkategorie(self):
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        zaznaczona_podkategoria = self.pobierz_zaznaczona_podkategorie()
        if zaznaczona_kategoria and zaznaczona_podkategoria:
            confirmation = messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunac podkategorie {zaznaczona_podkategoria.nazwa}?")
            if confirmation:
                kategorie = odczytaj_dane("kategorie.json")
                kategoria = next((k for k in kategorie if k.nazwa == zaznaczona_kategoria.nazwa), None)
                if kategoria:
                    usun_podkategorie_z_kategorii(kategoria, zaznaczona_podkategoria)
                    zapisz_dane(kategorie, "kategorie.json")
                    self.wyswietl_podkategorie(zaznaczona_kategoria)  # Odswiez widok podkategorii
                    self.drzewo_kategorie.selection_set(self.drzewo_kategorie.parent(self.drzewo_kategorie.selection()))  # Zaznacz kategorie nadrzedna
                    self.drzewo_kategorie.focus(self.drzewo_kategorie.parent(self.drzewo_kategorie.selection()))  # Ustaw fokus na kategorii nadrzednej
        else:
            messagebox.showinfo("Informacja", "Nie zaznaczono kategorii lub podkategorii.")

    def znajdz_kategorie(self, nazwa_kategorii):
        kategorie = odczytaj_dane("kategorie.json")
        for kategoria in kategorie:
            if kategoria.nazwa == nazwa_kategorii:
                return kategoria
        return None

    def znajdz_podkategorie(self, nazwa_podkategorii):
        kategorie = odczytaj_dane("kategorie.json")
        for kategoria in kategorie:
            for podkategoria in kategoria.podkategorie:
                if podkategoria.nazwa == nazwa_podkategorii:
                    return podkategoria
        return None


    
    def oblicz_dojazdy(self):
        okno_dojazdy = OknoDojazdy(self)
        self.wait_window(okno_dojazdy)



    def odswierz_widgety(self):
        self.odswierz_drzewo_kategorie()
        self.odswierz_liste_produkty()
        self.odswierz_liste_koszyk()
        self.odswierz_podsumowanie()

    def dodaj_koszt_dojazdu(self, koszt):
        self.koszt_dojazdu = koszt
        self.odswierz_podsumowanie()


        
    def odswierz_drzewo_podkategorie(self):
        print("Odswiezanie drzewa podkategorii...")
        
        # Usuniecie wszystkich istniejacych elementów z drzewa podkategorii
        self.drzewo_podkategorie.delete(*self.drzewo_podkategorie.get_children())
        
        # Pobranie zaznaczonej kategorii
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        
        if zaznaczona_kategoria:
            print(f"Zaznaczona kategoria: {zaznaczona_kategoria.nazwa}")
            print(f"Podkategorie zaznaczonej kategorii: {[p.nazwa for p in zaznaczona_kategoria.podkategorie]}")
            
            # Iteracja po podkategoriach zaznaczonej kategorii
            for podkategoria in zaznaczona_kategoria.podkategorie:
                print(f"Dodawanie podkategorii: {podkategoria.nazwa}")
                
                # Dodanie podkategorii do drzewa podkategorii
                self.drzewo_podkategorie.insert("", "end", text=podkategoria.nazwa)
                
                print(f"Podkategoria dodana do drzewa: {podkategoria.nazwa}")
        else:
            print("Brak zaznaczonej kategorii")
        
        print("Zakonczono odswiezanie drzewa podkategorii")


    def dodaj_podkategorie(self):
        print("Dodawanie podkategorii...")
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        if zaznaczona_kategoria:
            print(f"Zaznaczona kategoria: {zaznaczona_kategoria.nazwa}")
            nazwa_podkategorii = simpledialog.askstring("Dodaj podkategorie", "Podaj nazwe podkategorii:")
            if nazwa_podkategorii:
                print(f"Nazwa podkategorii: {nazwa_podkategorii}")
                nowa_podkategoria = Podkategoria(nazwa_podkategorii)
                zaznaczona_kategoria.dodaj_podkategorie(nowa_podkategoria)
                print(f"Podkategorie zaznaczonej kategorii: {[p.nazwa for p in zaznaczona_kategoria.podkategorie]}")
                
                kategorie = odczytaj_dane("kategorie.json")
                for kategoria in kategorie:
                    if kategoria.nazwa == zaznaczona_kategoria.nazwa:
                        kategoria.dodaj_podkategorie(nowa_podkategoria)
                        break
                zapisz_dane(kategorie, "kategorie.json")
                
                self.odswierz_drzewo_kategorie()
                self.wyswietl_produkty(None)
                print("Podkategoria dodana i dane zapisane.")
            else:
                print("Nie podano nazwy podkategorii.")
        else:
            print("Nie zaznaczono kategorii.")


    def pobierz_zaznaczona_kategorie(self):
        zaznaczone = self.drzewo_kategorie.selection()
        if zaznaczone:
            nazwa_kategorii = self.drzewo_kategorie.item(zaznaczone[0], "text")
            kategorie = odczytaj_dane("kategorie.json")
            for kategoria in kategorie:
                if kategoria.nazwa == nazwa_kategorii:
                    print(f"Pobrana zaznaczona kategoria: {kategoria.nazwa}")
                    return kategoria
        return None


    def wyswietl_produkty(self, event):
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        if zaznaczona_kategoria:
            self.drzewo_podkategorie.delete(*self.drzewo_podkategorie.get_children())
            for podkategoria in zaznaczona_kategoria.podkategorie:
                self.drzewo_podkategorie.insert("", "end", text=podkategoria.nazwa)
            self.lista_produkty.delete(0, tk.END)
        else:
            self.drzewo_podkategorie.delete(*self.drzewo_podkategorie.get_children())
            self.lista_produkty.delete(0, tk.END)

    def wyswietl_produkty_podkategorii(self, event):
        zaznaczona_podkategoria = self.pobierz_zaznaczona_podkategorie()
        if zaznaczona_podkategoria:
            self.lista_produkty.delete(0, tk.END)
            for produkt in zaznaczona_podkategoria.produkty:
                self.lista_produkty.insert(tk.END, f"{produkt.nazwa} - {produkt.cena} sek")
        else:
            self.lista_produkty.delete(0, tk.END)

    def wyswietl_produkty_kategoria(self, kategoria):
        self.lista_produkty.delete(0, tk.END)
        for podkategoria in kategoria.podkategorie:
            for produkt in podkategoria.produkty:
                self.lista_produkty.insert(tk.END, f"{produkt.nazwa} - {produkt.cena} - {produkt.typ}")

    def wyswietl_produkty_podkategoria(self, podkategoria):
        self.lista_produkty.delete(0, tk.END)
        for produkt in podkategoria.produkty:
            self.lista_produkty.insert(tk.END, f"{produkt.nazwa} - {produkt.cena} - {produkt.typ}")



    def odswierz_drzewo_kategorie(self):
        self.drzewo_kategorie.delete(*self.drzewo_kategorie.get_children())
        kategorie = odczytaj_dane("kategorie.json")
        for kategoria in kategorie:
            kategoria_item = self.drzewo_kategorie.insert("", "end", text=kategoria.nazwa)
            for podkategoria in kategoria.podkategorie:
                self.drzewo_kategorie.insert(kategoria_item, "end", text=podkategoria.nazwa)


    def odswierz_liste_produkty(self):
        zaznaczony_element = self.drzewo_kategorie.selection()
        if zaznaczony_element:
            nazwa_elementu = self.drzewo_kategorie.item(zaznaczony_element, "text")
            kategoria = self.znajdz_kategorie(nazwa_elementu)
            if kategoria:
                self.wyswietl_produkty_kategoria(kategoria)
            else:
                podkategoria = self.znajdz_podkategorie(nazwa_elementu)
                if podkategoria:
                    self.wyswietl_produkty_podkategoria(podkategoria)
        else:
            self.lista_produkty.delete(0, tk.END)


    def odswierz_liste_koszyk(self):
        koszyk = pobierz_zawartosc_koszyka()
        self.lista_koszyk.delete(0, tk.END)
        for produkt, ilosc in koszyk:
            self.lista_koszyk.insert(tk.END, f"{produkt.nazwa} - {ilosc}")

    def odswierz_podsumowanie(self, *args):
        koszyk = pobierz_zawartosc_koszyka()
        suma_robocizna = sum(p.cena * i for p, i in koszyk if p.typ == "robocizna")
        suma_material = sum(p.cena * i for p, i in koszyk if p.typ == "material")
        suma_podwykonawca = sum(p.cena * i for p, i in koszyk if p.typ == "podwykonawca")

        marza_robocizna = float(self.marza_robocizna_var.get() or 0)
        marza_material = float(self.marza_material_var.get() or 0)
        marza_podwykonawca = float(self.marza_podwykonawca_var.get() or 0)

        suma_robocizna_bez_marzy = suma_robocizna
        suma_robocizna *= (1 + marza_robocizna / 100)
        suma_material *= (1 + marza_material / 100)
        suma_material_bez_vat = suma_material * 0.8
        suma_podwykonawca *= (1 + marza_podwykonawca / 100)

        suma_calkowita = suma_robocizna + suma_material_bez_vat + suma_podwykonawca

        ilosc_godzin = suma_robocizna_bez_marzy / 400

        moc_przerobowa = float(self.moc_przerobowa_var.get() or 0)
        if moc_przerobowa > 0:
            ilosc_dni_roboczych = ilosc_godzin / moc_przerobowa
        else:
            ilosc_dni_roboczych = 0

        self.ilosc_dni_roboczych = ilosc_dni_roboczych

        koszt_dojazdu = 0
        if hasattr(self, 'koszt_dojazdu'):
            koszt_dojazdu = self.koszt_dojazdu
            suma_calkowita += koszt_dojazdu

        # Obliczanie marz
        marza_robocizna_wartosc = suma_robocizna - suma_robocizna_bez_marzy
        marza_material_wartosc = suma_material - suma_material / (1 + marza_material / 100)
        marza_podwykonawca_wartosc = suma_podwykonawca - suma_podwykonawca / (1 + marza_podwykonawca / 100)
        marza_dojazdy_wartosc = koszt_dojazdu * (marza_robocizna / 100)

        # Obliczanie caskowitej marzy za projekt
        calkowita_marza = marza_robocizna_wartosc + marza_material_wartosc + marza_podwykonawca_wartosc + marza_dojazdy_wartosc

        # Obliczanie dziennego zysku z projektu na podstawie marz
        dzienny_zysk_z_projektu = calkowita_marza / ilosc_dni_roboczych if ilosc_dni_roboczych > 0 else 0

        # Odczytywanie dziennych kosztów prowadzenia firmy z pliku JSON
        try:
            with open("koszty_firmowe.json", "r") as plik:
                koszty_firmowe = json.load(plik)
                dzienne_koszty_firmy = koszty_firmowe["dzienne_koszty"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            dzienne_koszty_firmy = 0

        # Obliczanie dziennego zysku po kosztach
        dzienny_zysk_po_kosztach = dzienny_zysk_z_projektu - dzienne_koszty_firmy

        self.podsumowanie.config(text=f"Podsumowanie:\n"
                                    f"Robocizna: {suma_robocizna:.2f}\n"
                                    f"Ilosc godzin: {ilosc_godzin:.2f}\n"
                                    f"Ilosc dni roboczych: {ilosc_dni_roboczych:.2f}\n"
                                    f"Material: {suma_material:.2f} (z VAT), {suma_material_bez_vat:.2f} (bez VAT)\n"
                                    f"Podwykonawca: {suma_podwykonawca:.2f}\n"
                                    f"Koszt dojazdu: {koszt_dojazdu:.2f}\n"
                                    f"Marza na robociznie: {marza_robocizna_wartosc:.2f}\n"
                                    f"Marza na materiale: {marza_material_wartosc:.2f}\n"
                                    f"Marza na podwykonawcach: {marza_podwykonawca_wartosc:.2f}\n"
                                    f"Marza na dojazdach: {marza_dojazdy_wartosc:.2f}\n"
                                    f"calkowita marza za projekt: {calkowita_marza:.2f}\n"
                                    f"Dzienne koszty firmowe: {int(dzienne_koszty_firmy)}\n"
                                    f"Dzienny zysk z projektu: {int(dzienny_zysk_z_projektu)}\n"
                                    f"Dzienny zysk po kosztach: {int(dzienny_zysk_po_kosztach)}\n"
                                    f"Suma calkowita: {suma_calkowita:.2f}")

        self.zapisz_konfiguracje()


    def odczytaj_dzienne_koszty(self):
        try:
            with open("dzienne_koszty.json", "r") as plik:
                dane = json.load(plik)
                return dane["dzienne_koszty"]
        except FileNotFoundError:
            return 0.0


    def dodaj_kategorie(self):
        nazwa_kategorii = simpledialog.askstring("Dodaj kategorie", "Podaj nazwe kategorii:")
        if nazwa_kategorii:
            nowa_kategoria = Kategoria(nazwa_kategorii)
            dodaj_kategorie(nowa_kategoria)
            self.odswierz_drzewo_kategorie()
            zapisz_dane(odczytaj_dane("kategorie.json"), "kategorie.json")
            
            # Ustawienie pozycji okienka dialogowego
            dialog_window = self.winfo_children()[-1]
            self.center_window(dialog_window, screen_number=0)  # Wysrodkowanie okna dialogowego na glównym ekranie


    def usun_kategorie(self):
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        if zaznaczona_kategoria:
            usun_kategorie(zaznaczona_kategoria)
            self.odswierz_drzewo_kategorie()
            zapisz_dane(odczytaj_dane("kategorie.json"), "kategorie.json")

    def dodaj_produkt(self):
        zaznaczony_element = self.drzewo_kategorie.selection()
        if zaznaczony_element:
            nazwa_elementu = self.drzewo_kategorie.item(zaznaczony_element, "text")
            podkategoria = self.znajdz_podkategorie(nazwa_elementu)
            if podkategoria:
                okno_dodaj_produkt = tk.Toplevel(self)
                okno_dodaj_produkt.title("Dodaj produkt")
                self.center_window(okno_dodaj_produkt, screen_number=0)  # Wysrodkowanie okna dialogowego

                ramka_nazwa = ttk.Frame(okno_dodaj_produkt)
                ramka_nazwa.pack(fill=tk.X, padx=5, pady=5)
                etykieta_nazwa = ttk.Label(ramka_nazwa, text="Nazwa produktu:")
                etykieta_nazwa.pack(side=tk.LEFT)
                pole_nazwa = ttk.Entry(ramka_nazwa)
                pole_nazwa.pack(side=tk.LEFT, fill=tk.X, expand=True)

                ramka_typ = ttk.Frame(okno_dodaj_produkt)
                ramka_typ.pack(fill=tk.X, padx=5, pady=5)
                etykieta_typ = ttk.Label(ramka_typ, text="Typ produktu:")
                etykieta_typ.pack(side=tk.LEFT)
                typy_produktow = ["robocizna", "material", "podwykonawca"]
                pole_typ = ttk.Combobox(ramka_typ, values=typy_produktow, state="readonly")
                pole_typ.pack(side=tk.LEFT, fill=tk.X, expand=True)

                def dodaj():
                    nazwa_produktu = pole_nazwa.get()
                    typ_produktu = pole_typ.get()
                    
                    if nazwa_produktu and typ_produktu:
                        if typ_produktu == "robocizna":
                            ilosc_godzin = simpledialog.askfloat("Ilosc godzin", "Podaj ilosc godzin:")
                            if ilosc_godzin:
                                cena_produktu = ilosc_godzin * 400  # Stawka 400 sek/h
                                nowy_produkt = Produkt(nazwa_produktu, cena_produktu, typ_produktu, ilosc_godzin)
                                podkategoria.dodaj_produkt(nowy_produkt)
                                
                                kategorie = odczytaj_dane("kategorie.json")
                                for kategoria in kategorie:
                                    pk = self.znajdz_podkategorie_po_nazwie(kategoria, podkategoria.nazwa)
                                    if pk:
                                        pk.dodaj_produkt(nowy_produkt)
                                        break
                                zapisz_dane(kategorie, "kategorie.json")
                                
                                self.odswierz_liste_produkty()
                                okno_dodaj_produkt.destroy()
                        else:
                            cena_produktu = simpledialog.askfloat("Cena produktu", "Podaj cene produktu:")
                            if cena_produktu:
                                nowy_produkt = Produkt(nazwa_produktu, cena_produktu, typ_produktu)
                                podkategoria.dodaj_produkt(nowy_produkt)
                                
                                kategorie = odczytaj_dane("kategorie.json")
                                for kategoria in kategorie:
                                    pk = self.znajdz_podkategorie_po_nazwie(kategoria, podkategoria.nazwa)
                                    if pk:
                                        pk.dodaj_produkt(nowy_produkt)
                                        break
                                zapisz_dane(kategorie, "kategorie.json")
                                
                                self.odswierz_liste_produkty()
                                okno_dodaj_produkt.destroy()
                    else:
                        messagebox.showerror("Blad", "Wypelnij wszystkie pola!")

                przycisk_dodaj = ttk.Button(okno_dodaj_produkt, text="Dodaj", command=dodaj)
                przycisk_dodaj.pack(pady=5)
            else:
                messagebox.showerror("Blad", "Nie wybrano podkategorii!")
        else:
            messagebox.showerror("Blad", "Nie wybrano podkategorii!")


    def znajdz_podkategorie_po_nazwie(self, kategoria, nazwa_podkategorii):
        for podkategoria in kategoria.podkategorie:
            if podkategoria.nazwa == nazwa_podkategorii:
                return podkategoria
        return None

    def usun_produkt(self):
        zaznaczony_element = self.drzewo_kategorie.selection()
        if zaznaczony_element:
            nazwa_elementu = self.drzewo_kategorie.item(zaznaczony_element, "text")
            podkategoria = self.znajdz_podkategorie(nazwa_elementu)
            if podkategoria:
                zaznaczony_indeks = self.lista_produkty.curselection()
                if zaznaczony_indeks:
                    nazwa_produktu = self.lista_produkty.get(zaznaczony_indeks).split(" - ")[0]
                    produkt = podkategoria.znajdz_produkt(nazwa_produktu)
                    if produkt:
                        kategorie = odczytaj_dane("kategorie.json")
                        for kategoria in kategorie:
                            for pk in kategoria.podkategorie:
                                if pk.nazwa == podkategoria.nazwa:
                                    pk.produkty = [p for p in pk.produkty if p.nazwa != produkt.nazwa]
                                    break
                        zapisz_dane(kategorie, "kategorie.json")
                        self.odswierz_liste_produkty()
                    else:
                        print(f"Produkt {nazwa_produktu} nie znajduje sie w podkategorii {podkategoria.nazwa}")
                else:
                    print("Nie wybrano produktu.")
            else:
                print("Nie wybrano podkategorii.")
        else:
            print("Nie wybrano elementu w drzewie kategorii.")



    def dodaj_do_koszyka(self):
        zaznaczony_indeks = self.lista_produkty.curselection()
        if zaznaczony_indeks:
            produkt_info = self.lista_produkty.get(zaznaczony_indeks)
            produkt_info_parts = produkt_info.split(" - ")
            if len(produkt_info_parts) >= 3:
                nazwa_produktu = " - ".join(produkt_info_parts[:-2])
                cena_produktu = float(produkt_info_parts[-2])
                typ_produktu = produkt_info_parts[-1]
                
                ilosc = simpledialog.askinteger("Dodaj do koszyka", "Podaj ilosc:")
                if ilosc:
                    zaznaczony_element = self.drzewo_kategorie.selection()
                    if zaznaczony_element:
                        nazwa_elementu = self.drzewo_kategorie.item(zaznaczony_element, "text")
                        kategoria = self.znajdz_kategorie(nazwa_elementu)
                        if kategoria:
                            for podkategoria in kategoria.podkategorie:
                                produkt = podkategoria.znajdz_produkt(nazwa_produktu)
                                if produkt:
                                    dodaj_do_koszyka(produkt, ilosc)
                                    self.odswierz_liste_koszyk()
                                    self.odswierz_podsumowanie()
                                    zapisz_dane(pobierz_zawartosc_koszyka(), "koszyk.json")
                                    break
                            else:
                                print(f"Produkt {nazwa_produktu} nie znajduje sie w kategorii {nazwa_elementu}")
                        else:
                            podkategoria = self.znajdz_podkategorie(nazwa_elementu)
                            if podkategoria:
                                produkt = podkategoria.znajdz_produkt(nazwa_produktu)
                                if produkt:
                                    dodaj_do_koszyka(produkt, ilosc)
                                    self.odswierz_liste_koszyk()
                                    self.odswierz_podsumowanie()
                                    zapisz_dane(pobierz_zawartosc_koszyka(), "koszyk.json")
                                else:
                                    print(f"Produkt {nazwa_produktu} nie znajduje sie w podkategorii {nazwa_elementu}")
                            else:
                                print(f"Nie znaleziono podkategorii {nazwa_elementu}")
                    else:
                        print("Nie wybrano elementu w drzewie kategorii.")
            else:
                print(f"Nieprawidlowy format informacji o produkcie: {produkt_info}")


    def usun_z_koszyka(self):
        zaznaczony_produkt = self.pobierz_zaznaczony_produkt_z_koszyka()
        if zaznaczony_produkt:
            usun_z_koszyka(zaznaczony_produkt)
            self.odswierz_liste_koszyk()
            self.odswierz_podsumowanie()
            zapisz_dane(pobierz_zawartosc_koszyka(), "koszyk.json")

    def wyczysc_koszyk(self):
        wyczysc_koszyk()
        self.odswierz_liste_koszyk()
        self.odswierz_podsumowanie()
        zapisz_dane([], "koszyk.json")

    def pobierz_zaznaczona_kategorie(self):
        zaznaczony_element = self.drzewo_kategorie.selection()
        if zaznaczony_element:
            nazwa_kategorii = self.drzewo_kategorie.item(zaznaczony_element, "text")
            kategorie = odczytaj_dane("kategorie.json")
            for kategoria in kategorie:
                if kategoria.nazwa == nazwa_kategorii:
                    return kategoria
        return None


    def pobierz_zaznaczony_produkt(self):
        zaznaczony_indeks = self.lista_produkty.curselection()
        if zaznaczony_indeks:
            nazwa_produktu = self.lista_produkty.get(zaznaczony_indeks).split(" - ")[0]
            zaznaczona_podkategoria = self.pobierz_zaznaczona_podkategorie()
            if zaznaczona_podkategoria:
                for produkt in zaznaczona_podkategoria.produkty:
                    if produkt.nazwa == nazwa_produktu:
                        return produkt
        return None



    def pobierz_zaznaczony_produkt_z_koszyka(self):
        zaznaczony_indeks = self.lista_koszyk.curselection()
        if zaznaczony_indeks:
            nazwa_produktu = self.lista_koszyk.get(zaznaczony_indeks).split(" - ")[0]
            koszyk = pobierz_zawartosc_koszyka()
            for produkt, _ in koszyk:
                if produkt.nazwa == nazwa_produktu:
                    return produkt
        return None



    def center_window(self, window, screen_number=0):
        if hasattr(window, 'geometry'):
            window.update_idletasks()
            width = window.winfo_width()
            height = window.winfo_height()
            
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            
            if screen_number == 0:
                # Glówny ekran
                screen_x = 0
                screen_y = 0
            else:
                # Dodatkowy ekran
                screen_x = screen_width
                screen_y = 0
            
            x = screen_x + (screen_width // 2) - (width // 2)
            y = screen_y + (screen_height // 2) - (height // 2)
            window.geometry(f"+{x}+{y}")

    def pobierz_zaznaczona_podkategorie(self):
        zaznaczony_element = self.drzewo_podkategorie.focus()
        if zaznaczony_element:
            zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
            nazwa_elementu = self.drzewo_podkategorie.item(zaznaczony_element)['text']
            podkategoria = znajdz_podkategorie(zaznaczona_kategoria, nazwa_elementu)
            return podkategoria
        return None



    
    def odczytaj_konfiguracje(self):
        try:
            with open("konfiguracja_gui.json", "r") as plik:
                konfiguracja = json.load(plik)
                self.ostatnia_marza_robocizna = konfiguracja.get("marza_robocizna", "")
                self.ostatnia_marza_material = konfiguracja.get("marza_material", "")
                self.ostatnia_marza_podwykonawca = konfiguracja.get("marza_podwykonawca", "")
                self.ostatnia_moc_przerobowa = konfiguracja.get("moc_przerobowa", "")
        except FileNotFoundError:
            self.ostatnia_marza_robocizna = ""
            self.ostatnia_marza_material = ""
            self.ostatnia_marza_podwykonawca = ""
            self.ostatnia_moc_przerobowa = ""

    def zapisz_konfiguracje(self):
        konfiguracja = {
            "marza_robocizna": self.marza_robocizna_var.get(),
            "marza_material": self.marza_material_var.get(),
            "marza_podwykonawca": self.marza_podwykonawca_var.get(),
            "moc_przerobowa": self.moc_przerobowa_var.get()
        }
        with open("konfiguracja_gui.json", "w") as plik:
            json.dump(konfiguracja, plik)

    def dodaj_koszt_dojazdu(self, koszt):
        self.koszt_dojazdu = koszt
        self.odswierz_podsumowanie()

if __name__ == "__main__":
    app = Aplikacja()
    app.mainloop()
