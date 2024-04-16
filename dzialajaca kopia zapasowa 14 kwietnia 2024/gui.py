import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from produkty import Produkt
from tkinter import simpledialog
from kategorie import Kategoria, dodaj_kategorie, usun_kategorie
from produkty import Produkt, dodaj_produkt, usun_produkt
from koszyk import dodaj_do_koszyka, usun_z_koszyka, wyczysc_koszyk, pobierz_zawartosc_koszyka, oblicz_wartosc_koszyka
from baza_danych import odczytaj_dane, zapisz_dane
from kategorie import Kategoria, Podkategoria


class Aplikacja(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Aplikacja do kosztorysowania")
        self.geometry("800x600")

        # Ramka dla kategorii, podkategorii i produktów
        self.ramka_kategorie_produkty = ttk.Frame(self)
        self.ramka_kategorie_produkty.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.utworz_widgety()

    def utworz_widgety(self):
        # Ramka dla kategorii, podkategorii i przycisków
        ramka_kategorie = ttk.Frame(self.ramka_kategorie_produkty)
        ramka_kategorie.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Drzewo kategorii i podkategorii
        self.drzewo_kategorie = ttk.Treeview(ramka_kategorie)
        self.drzewo_kategorie.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.drzewo_kategorie.bind("<<TreeviewSelect>>", self.wyswietl_produkty)

        # Przyciski dla kategorii i podkategorii
        ramka_przyciski = ttk.Frame(ramka_kategorie)
        ramka_przyciski.pack(side=tk.TOP, padx=5, pady=5)

        self.przycisk_dodaj_kategorie = ttk.Button(ramka_przyciski, text="Dodaj kategorie", command=self.dodaj_kategorie)
        self.przycisk_dodaj_kategorie.pack(side=tk.LEFT, padx=5)

        self.przycisk_usun_kategorie = ttk.Button(ramka_przyciski, text="Usun kategorie", command=self.usun_kategorie)
        self.przycisk_usun_kategorie.pack(side=tk.LEFT, padx=5)

        self.przycisk_dodaj_podkategorie = ttk.Button(ramka_przyciski, text="Dodaj podkategorie", command=self.dodaj_podkategorie)
        self.przycisk_dodaj_podkategorie.pack(side=tk.LEFT, padx=5)

        self.przycisk_usun_podkategorie = ttk.Button(ramka_przyciski, text="Usun podkategorie", command=self.usun_podkategorie)
        self.przycisk_usun_podkategorie.pack(side=tk.LEFT, padx=5)

        # Ramka dla listy produktów i przycisków
        ramka_produkty = ttk.Frame(self.ramka_kategorie_produkty)
        ramka_produkty.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Lista produktów
        self.lista_produkty = tk.Listbox(ramka_produkty)
        self.lista_produkty.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)

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

        self.odswierz_widgety()

    def wyswietl_podkategorie(self, event):
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        if zaznaczona_kategoria:
            self.drzewo_podkategorie.delete(*self.drzewo_podkategorie.get_children())
            for podkategoria in zaznaczona_kategoria.podkategorie:
                self.drzewo_podkategorie.insert("", "end", text=podkategoria.nazwa)
        else:
            self.drzewo_podkategorie.delete(*self.drzewo_podkategorie.get_children())

    def usun_podkategorie(self):
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        zaznaczona_podkategoria = self.pobierz_zaznaczona_podkategorie()

        if zaznaczona_kategoria and zaznaczona_podkategoria:
            zaznaczona_kategoria.usun_podkategorie(zaznaczona_podkategoria)
            self.drzewo_podkategorie.delete(self.drzewo_podkategorie.selection())
            self.odswierz_widgety()
            zapisz_dane(odczytaj_dane("kategorie.json"), "kategorie.json")

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




    def odswierz_widgety(self):
        self.odswierz_drzewo_kategorie()
        self.odswierz_liste_produkty()
        self.odswierz_liste_koszyk()
        self.odswierz_podsumowanie()
        
    def odswierz_drzewo_podkategorie(self):
        print("Odświeżanie drzewa podkategorii...")
        
        # Usunięcie wszystkich istniejących elementów z drzewa podkategorii
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
        
        print("Zakończono odświeżanie drzewa podkategorii")



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

    def odswierz_podsumowanie(self):
        koszyk = pobierz_zawartosc_koszyka()
        suma_robocizna = sum(p.cena * i for p, i in koszyk if p.typ == "robocizna")
        suma_material = sum(p.cena * i for p, i in koszyk if p.typ == "material")
        suma_podwykonawca = sum(p.cena * i for p, i in koszyk if p.typ == "podwykonawca")
        suma_calkowita = suma_robocizna + suma_material + suma_podwykonawca

        self.podsumowanie.config(text=f"Podsumowanie:\nRobocizna: {suma_robocizna:.2f}\nMaterial: {suma_material:.2f}\nPodwykonawca: {suma_podwykonawca:.2f}\nSuma calkowita: {suma_calkowita:.2f}")


    def dodaj_kategorie(self):
        nazwa_kategorii = simpledialog.askstring("Dodaj kategorie", "Podaj nazwe kategorii:")
        if nazwa_kategorii:
            nowa_kategoria = Kategoria(nazwa_kategorii)
            dodaj_kategorie(nowa_kategoria)
            self.odswierz_drzewo_kategorie()
            zapisz_dane(odczytaj_dane("kategorie.json"), "kategorie.json")
            
            # Ustawienie pozycji okienka dialogowego
            dialog_window = self.winfo_children()[-1]
            self.center_window(dialog_window, screen_number=0)  # Wyśrodkowanie okna dialogowego na głównym ekranie


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
                self.center_window(okno_dodaj_produkt, screen_number=0)  # Wyśrodkowanie okna dialogowego

                ramka_nazwa = ttk.Frame(okno_dodaj_produkt)
                ramka_nazwa.pack(fill=tk.X, padx=5, pady=5)
                etykieta_nazwa = ttk.Label(ramka_nazwa, text="Nazwa produktu:")
                etykieta_nazwa.pack(side=tk.LEFT)
                pole_nazwa = ttk.Entry(ramka_nazwa)
                pole_nazwa.pack(side=tk.LEFT, fill=tk.X, expand=True)

                ramka_cena = ttk.Frame(okno_dodaj_produkt)
                ramka_cena.pack(fill=tk.X, padx=5, pady=5)
                etykieta_cena = ttk.Label(ramka_cena, text="Cena produktu:")
                etykieta_cena.pack(side=tk.LEFT)
                pole_cena = ttk.Entry(ramka_cena)
                pole_cena.pack(side=tk.LEFT, fill=tk.X, expand=True)

                ramka_typ = ttk.Frame(okno_dodaj_produkt)
                ramka_typ.pack(fill=tk.X, padx=5, pady=5)
                etykieta_typ = ttk.Label(ramka_typ, text="Typ produktu:")
                etykieta_typ.pack(side=tk.LEFT)
                typy_produktow = ["robocizna", "material", "podwykonawca"]
                pole_typ = ttk.Combobox(ramka_typ, values=typy_produktow, state="readonly")
                pole_typ.pack(side=tk.LEFT, fill=tk.X, expand=True)

                def dodaj():
                    nazwa_produktu = pole_nazwa.get()
                    cena_produktu = float(pole_cena.get())
                    typ_produktu = pole_typ.get()
                    
                    if nazwa_produktu and cena_produktu and typ_produktu:
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
                        messagebox.showerror("Błąd", "Wypełnij wszystkie pola!")

                przycisk_dodaj = ttk.Button(okno_dodaj_produkt, text="Dodaj", command=dodaj)
                przycisk_dodaj.pack(pady=5)
            else:
                messagebox.showerror("Błąd", "Nie wybrano podkategorii!")
        else:
            messagebox.showerror("Błąd", "Nie wybrano podkategorii!")

    def znajdz_podkategorie_po_nazwie(self, kategoria, nazwa_podkategorii):
        for podkategoria in kategoria.podkategorie:
            if podkategoria.nazwa == nazwa_podkategorii:
                return podkategoria
        return None



    def usun_produkt(self):
        zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
        zaznaczony_produkt = self.pobierz_zaznaczony_produkt()
        print(f"Zaznaczona kategoria: {zaznaczona_kategoria}")
        print(f"Zaznaczony produkt: {zaznaczony_produkt}")
        if zaznaczona_kategoria and zaznaczony_produkt:
            if zaznaczony_produkt in zaznaczona_kategoria.produkty:
                print(f"Usuwanie produktu: {zaznaczony_produkt}")
                zaznaczona_kategoria.usun_produkt(zaznaczony_produkt)
                self.odswierz_liste_produkty()
                zapisz_dane(odczytaj_dane("kategorie.json"), "kategorie.json")
        else:
            print("Nie wybrano kategorii lub produktu.")




    def dodaj_do_koszyka(self):
        zaznaczony_indeks = self.lista_produkty.curselection()
        if zaznaczony_indeks:
            produkt_info = self.lista_produkty.get(zaznaczony_indeks)
            nazwa_produktu, cena_produktu, typ_produktu = produkt_info.split(" - ")
            cena_produktu = float(cena_produktu)
            
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
                        podkategoria = self.znajdz_podkategorie(nazwa_elementu)
                        if podkategoria:
                            produkt = podkategoria.znajdz_produkt(nazwa_produktu)
                            if produkt:
                                dodaj_do_koszyka(produkt, ilosc)
                                self.odswierz_liste_koszyk()
                                self.odswierz_podsumowanie()
                                zapisz_dane(pobierz_zawartosc_koszyka(), "koszyk.json")
                
                dialog_window = self.master.winfo_children()[-1]
                self.center_window(dialog_window, screen_number=0)  # Wyśrodkowanie okna dialogowego na głównym ekranie



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
        zaznaczone = self.drzewo_kategorie.selection()
        if zaznaczone:
            nazwa_kategorii = self.drzewo_kategorie.item(zaznaczone[0], "text")
            kategorie = odczytaj_dane("kategorie.json")
            for kategoria in kategorie:
                if kategoria.nazwa == nazwa_kategorii:
                    return kategoria
        return None


    def pobierz_zaznaczony_produkt(self):
        zaznaczony_indeks = self.lista_produkty.curselection()
        if zaznaczony_indeks:
            nazwa_produktu = self.lista_produkty.get(zaznaczony_indeks).split(" - ")[0]
            zaznaczona_kategoria = self.pobierz_zaznaczona_kategorie()
            if zaznaczona_kategoria:
                for produkt in zaznaczona_kategoria.produkty:
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
                # Główny ekran
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
        zaznaczony_element = self.drzewo_kategorie.selection()
        if zaznaczony_element:
            nazwa_elementu = self.drzewo_kategorie.item(zaznaczony_element, "text")
            podkategoria = self.znajdz_podkategorie(nazwa_elementu)
            if podkategoria:
                return podkategoria
        return None







if __name__ == "__main__":
    app = Aplikacja()
    app.mainloop()
