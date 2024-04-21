import tkinter as tk
from tkinter import messagebox

def dodaj_koszt(nazwa_kosztu, kwota_kosztu, listbox_koszty):
    koszt = f"{nazwa_kosztu}: {kwota_kosztu:.2f} sek"
    listbox_koszty.insert(tk.END, koszt)

def dodaj_koszt_osobowy(nazwa_kosztu, kwota_kosztu, listbox_koszty, osoba):
    koszt = f"{nazwa_kosztu}: {kwota_kosztu:.2f} sek"
    listbox_koszty.insert(tk.END, koszt)

def usun_koszt(listbox_koszty):
    selected_index = listbox_koszty.curselection()
    if selected_index:
        listbox_koszty.delete(selected_index)

def oblicz_wynagrodzenie(kwota_faktury, stawka_godzinowa, koszty_projektu, koszty_bronek, koszty_mateusz,
                         label_wynik_projekt, label_wynik_bronek, label_wynik_mateusz):
    try:
        kwota_faktury = float(kwota_faktury)
        stawka_godzinowa = float(stawka_godzinowa)

        koszty_projektu_suma = sum(koszty_projektu)
        koszty_bronek_suma = sum(koszty_bronek)
        koszty_mateusz_suma = sum(koszty_mateusz)
        koszty_calkowite = koszty_projektu_suma + koszty_bronek_suma + koszty_mateusz_suma

        moms_kosztow_projektu = koszty_projektu_suma * 0.25
        moms_kosztow_osobowych = (koszty_bronek_suma + koszty_mateusz_suma) * 0.25
        moms_faktury = kwota_faktury * 0.25
        moms_do_zaplaty = moms_faktury - moms_kosztow_projektu - moms_kosztow_osobowych

        zysk_projektu = kwota_faktury - koszty_projektu_suma - moms_do_zaplaty
        ilosc_godzin = zysk_projektu / stawka_godzinowa
        zysk_firmowy = zysk_projektu - ilosc_godzin * 400
        zysk_prywatny = ilosc_godzin * 400

        zysk_bronek = zysk_prywatny / 2 - koszty_bronek_suma
        zysk_mateusz = zysk_prywatny / 2 - koszty_mateusz_suma

        podatek_bronek = zysk_bronek * 0.32
        podatek_mateusz = zysk_mateusz * 0.32

        label_wynik_projekt.config(text=f"Zysk z projektu: {zysk_projektu:.2f} sek\n"
                                        f"Ilość godzin: {ilosc_godzin:.2f} h\n"
                                        f"Zysk firmowy: {zysk_firmowy:.2f} sek\n"
                                        f"MOMS do zapłaty: {moms_do_zaplaty:.2f} sek")
        label_wynik_bronek.config(text=f"Zysk Bronek: {zysk_bronek:.2f} sek\n"
                                       f"Podatek Bronek: {podatek_bronek:.2f} sek")
        label_wynik_mateusz.config(text=f"Zysk Mateusz: {zysk_mateusz:.2f} sek\n"
                                        f"Podatek Mateusz: {podatek_mateusz:.2f} sek")
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź poprawne wartości liczbowe.")

def create_gui(window):
    window.geometry("800x600")
    window.title("Kalkulator wynagrodzen")

    frame_faktura = tk.Frame(window)
    frame_faktura.pack(pady=5)
    label_faktura = tk.Label(frame_faktura, text="Kwota faktury (sek):")
    label_faktura.pack(side=tk.LEFT)
    entry_faktura = tk.Entry(frame_faktura)
    entry_faktura.pack(side=tk.LEFT)

    frame_stawka_godzinowa = tk.Frame(window)
    frame_stawka_godzinowa.pack(pady=5)
    label_stawka_godzinowa = tk.Label(frame_stawka_godzinowa, text="Stawka godzinowa (sek):")
    label_stawka_godzinowa.pack(side=tk.LEFT)
    entry_stawka_godzinowa = tk.Entry(frame_stawka_godzinowa)
    entry_stawka_godzinowa.pack(side=tk.LEFT)

    frame_koszty = tk.Frame(window)
    frame_koszty.pack(pady=10)
    label_koszty = tk.Label(frame_koszty, text="Koszty projektu:")
    label_koszty.pack()
    listbox_koszty = tk.Listbox(frame_koszty, width=50)
    listbox_koszty.pack(side=tk.LEFT)
    button_usun_koszt = tk.Button(frame_koszty, text="Usun koszt projektu",
                                  command=lambda: [usun_koszt(listbox_koszty), update_wynagrodzenie()])
    button_usun_koszt.pack(side=tk.LEFT, padx=10)

    frame_koszty_osobowe = tk.Frame(window)
    frame_koszty_osobowe.pack(pady=10)
    frame_koszty_bronek = tk.Frame(frame_koszty_osobowe)
    frame_koszty_bronek.pack(side=tk.LEFT, padx=10)
    label_koszty_bronek = tk.Label(frame_koszty_bronek, text="Koszty Bronek:")
    label_koszty_bronek.pack()
    listbox_koszty_bronek = tk.Listbox(frame_koszty_bronek, width=40)
    listbox_koszty_bronek.pack(side=tk.LEFT)
    button_usun_koszt_bronek = tk.Button(frame_koszty_bronek, text="Usun koszt Bronek",
                                         command=lambda: [usun_koszt(listbox_koszty_bronek), update_wynagrodzenie()])
    button_usun_koszt_bronek.pack(side=tk.LEFT, padx=10)
    frame_koszty_mateusz = tk.Frame(frame_koszty_osobowe)
    frame_koszty_mateusz.pack(side=tk.LEFT, padx=10)
    label_koszty_mateusz = tk.Label(frame_koszty_mateusz, text="Koszty Mateusz:")
    label_koszty_mateusz.pack()
    listbox_koszty_mateusz = tk.Listbox(frame_koszty_mateusz, width=40)
    listbox_koszty_mateusz.pack(side=tk.LEFT)
    button_usun_koszt_mateusz = tk.Button(frame_koszty_mateusz, text="Usun koszt Mateusz",
                                          command=lambda: [usun_koszt(listbox_koszty_mateusz), update_wynagrodzenie()])
    button_usun_koszt_mateusz.pack(side=tk.LEFT, padx=10)

    frame_dodaj_koszt = tk.Frame(window)
    frame_dodaj_koszt.pack(pady=5)
    label_nazwa_kosztu = tk.Label(frame_dodaj_koszt, text="Nazwa kosztu:")
    label_nazwa_kosztu.pack(side=tk.LEFT)
    entry_nazwa_kosztu = tk.Entry(frame_dodaj_koszt)
    entry_nazwa_kosztu.pack(side=tk.LEFT)
    label_kwota_kosztu = tk.Label(frame_dodaj_koszt, text="Kwota kosztu (sek):")
    label_kwota_kosztu.pack(side=tk.LEFT, padx=10)
    entry_kwota_kosztu = tk.Entry(frame_dodaj_koszt)
    entry_kwota_kosztu.pack(side=tk.LEFT)
    button_dodaj_koszt = tk.Button(frame_dodaj_koszt, text="Dodaj koszt projektu",
                                   command=lambda: [dodaj_koszt(entry_nazwa_kosztu.get(),
                                                                float(entry_kwota_kosztu.get()),
                                                                listbox_koszty),
                                                    update_wynagrodzenie()])
    button_dodaj_koszt.pack(side=tk.LEFT, padx=10)

    frame_dodaj_koszt_osobowy = tk.Frame(window)
    frame_dodaj_koszt_osobowy.pack(pady=5)
    label_nazwa_kosztu_osobowy = tk.Label(frame_dodaj_koszt_osobowy, text="Nazwa kosztu osobowego:")
    label_nazwa_kosztu_osobowy.pack(side=tk.LEFT)
    entry_nazwa_kosztu_osobowy = tk.Entry(frame_dodaj_koszt_osobowy)
    entry_nazwa_kosztu_osobowy.pack(side=tk.LEFT)
    label_kwota_kosztu_osobowy = tk.Label(frame_dodaj_koszt_osobowy, text="Kwota kosztu osobowego (sek):")
    label_kwota_kosztu_osobowy.pack(side=tk.LEFT, padx=10)
    entry_kwota_kosztu_osobowy = tk.Entry(frame_dodaj_koszt_osobowy)
    entry_kwota_kosztu_osobowy.pack(side=tk.LEFT)
    button_dodaj_koszt_bronek = tk.Button(frame_dodaj_koszt_osobowy, text="Dodaj koszt Bronek",
                                          command=lambda: [dodaj_koszt_osobowy(entry_nazwa_kosztu_osobowy.get(),
                                                                               float(entry_kwota_kosztu_osobowy.get()),
                                                                               listbox_koszty_bronek, "Bronek"),
                                                           update_wynagrodzenie()])
    button_dodaj_koszt_bronek.pack(side=tk.LEFT, padx=10)
    button_dodaj_koszt_mateusz = tk.Button(frame_dodaj_koszt_osobowy, text="Dodaj koszt Mateusz",
                                           command=lambda: [dodaj_koszt_osobowy(entry_nazwa_kosztu_osobowy.get(),
                                                                                float(entry_kwota_kosztu_osobowy.get()),
                                                                                listbox_koszty_mateusz, "Mateusz"),
                                                            update_wynagrodzenie()])
    button_dodaj_koszt_mateusz.pack(side=tk.LEFT, padx=10)

    frame_wynik = tk.Frame(window)
    frame_wynik.pack(pady=10)
    label_wynik_projekt = tk.Label(frame_wynik, text="")
    label_wynik_projekt.pack()
    label_wynik_bronek = tk.Label(frame_wynik, text="")
    label_wynik_bronek.pack()
    label_wynik_mateusz = tk.Label(frame_wynik, text="")
    label_wynik_mateusz.pack()

    def update_wynagrodzenie(event=None):
        koszty_projektu = [float(listbox_koszty.get(i).split(": ")[1].split(" ")[0]) for i in range(listbox_koszty.size())]
        koszty_bronek = [float(listbox_koszty_bronek.get(i).split(": ")[1].split(" ")[0]) for i in range(listbox_koszty_bronek.size())]
        koszty_mateusz = [float(listbox_koszty_mateusz.get(i).split(": ")[1].split(" ")[0]) for i in range(listbox_koszty_mateusz.size())]

        oblicz_wynagrodzenie(entry_faktura.get(), entry_stawka_godzinowa.get(),
                             koszty_projektu, koszty_bronek, koszty_mateusz,
                             label_wynik_projekt, label_wynik_bronek, label_wynik_mateusz)

    entry_faktura.bind("<Return>", update_wynagrodzenie)
    entry_stawka_godzinowa.bind("<Return>", update_wynagrodzenie)

if __name__ == "__main__":
    window = tk.Tk()
    create_gui(window)
    window.mainloop()