import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import string
import random

page = {}



headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
}

email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

sciezka_do_pliku = "dane_firm.csv"

# 1. Definiujemy województwa i liczbę stron dla każdego z nich (dla testów dajemy mało stron)
wojewodztwa_do_pobrania = {
    "Mazowieckie": 549,   # Zamiast 549, dla testów pobierze tylko strony 0, 1, 2, 3
    "Małopolskie": 332,   # Zamiast 332, dla testów pobierze tylko strony 0, 1, 2, 3
    "Śląskie": 327,      # Zamiast 327, dla testów pobierze tylko strony 0, 1, 2, 3
    "Dolnośląskie": 245,   # Zamiast 245, dla testów pobierze tylko strony 0, 1, 2, 3
    "Wielkopolskie": 238,   # Zamiast 238, dla testów pobierze tylko strony 0, 1, 2, 3
    "Pomorskie": 178,   # Zamiast 178, dla testów pobierze tylko strony 0, 1, 2, 3
    "Lubelskie": 89,   # Zamiast 89, dla testów pobierze tylko strony 0, 1, 2, 3
    "Zachodniopomorskie": 112,   # Zamiast 112, dla testów pobierze tylko strony 0, 1, 2, 3
    "Podkarpackie": 110,   # Zamiast 110, dla testów pobierze tylko strony 0, 1, 2, 3
    "Kujawsko-Pomorskie": 105,   # Zamiast 105, dla testów pobierze tylko strony 0, 1, 2, 3
    "Warmińsko-Mazurskie": 64,   # Zamiast 64, dla testów pobierze tylko strony 0, 1, 2, 3
    "Podlaskie": 64,   # Zamiast 64, dla testów pobierze tylko strony 0, 1, 2, 3
    "Łódzkie": 131,   # Zamiast 131, dla testów pobierze tylko strony 0, 1, 2, 3
    "Świętokrzyskie": 54,   # Zamiast 54, dla testów pobierze tylko strony 0, 1, 2, 3
    "Opolskie": 39,   # Zamiast 39, dla testów pobierze tylko strony 0, 1, 2, 3
    "Lubuskie": 46,   # Zamiast 46, dla testów pobierze tylko strony 0, 1, 2, 3
    "Cała+Polska": 92   # Zamiast 92, dla testów pobierze tylko strony 0, 1, 2, 3
}

with open(sciezka_do_pliku, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Nazwa firmy", "Email", "Strona internetowa"])
    
    # 2. Główna pętla, która "chodzi" po województwach z naszego słownika
    for wojewodztwo, liczba_stron in wojewodztwa_do_pobrania.items():
        print(f"\n=======================================================")
        print(f"=== ROZPOCZYNAM POBIERANIE WOJEWÓDZTWA: {wojewodztwo.upper()} ===")
        print(f"=======================================================\n")
        
        # 3. Pętla "chodząca" po stronach danego województwa
        for page_num in range(0, liczba_stron):
            print(f"Pobieram stronę {page_num} ({wojewodztwo})...")
            
            # Wklejamy nazwę województwa bezpośrednio do linku (url encoding nie jest tu konieczny dla requests)
            url = f"https://www.firmyogloszenia.pl/showstate2.php?state={wojewodztwo}&copage={page_num}"
            
            try:
                # Delikatny czas na "oddech" przed każdym strzałem
                czas_pauzy = random.uniform(0.3, 0.7)
                time.sleep(czas_pauzy)
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Szukamy pudełek z firmami
                firmy = soup.find_all("div", class_="compall")
                
                # Zabezpieczenie: Jeśli nie ma firm na stronie, to prawdopodobnie koniec katalogu lub blokada
                if not firmy:
                    print(f"⚠️ Uwaga: Brak firm na stronie {page_num}. Przechodzę do kolejnej.")
                    continue
                
                # 4. Pętla przetwarzająca pojedyncze wizytówki na danej stronie
                for firma in firmy:
                    # Wyciągamy nazwę firmy z <h1>
                    name_tag = firma.find("h1")
                    nazwa = name_tag.text.strip() if name_tag else "Brak nazwy"
                    
                    # Szukamy sekcji kontaktowej
                    kontakt_tag = firma.find("span", class_="coright")
                    
                    if kontakt_tag:
                        # Szukamy maila używając wyrażeń regularnych
                        caly_tekst_kontaktu = kontakt_tag.text
                        znalezione_maile = email_pattern.findall(caly_tekst_kontaktu)
                        email = znalezione_maile[0] if znalezione_maile else "Brak e-maila"
                        
                        # Szukamy strony WWW w atrybucie 'href'
                        a_tag = kontakt_tag.find("a")
                        if a_tag and 'href' in a_tag.attrs:
                            www = a_tag['href']
                        else:
                            www = "Brak strony"
                    else:
                        email = "Brak e-maila"
                        www = "Brak strony"
                    
                    print(f"-> {nazwa} | E-mail: {email} | WWW: {www}")
                    writer.writerow([nazwa, email, www])
                    
            except requests.exceptions.RequestException as e:
                print(f"Błąd przy pobieraniu strony {page_num} ({wojewodztwo}): {e}")
                # Przerywamy pobieranie TEGO konkretnego województwa (ale program przejdzie do następnego!)
                break 



    # NOTARIUSZE
    litera = "a"
    url2 = "https://rejent.poznan.pl/wykaz_notariuszy/a/"
    alfabet = list(string.ascii_lowercase)

    for litera in alfabet:
        print(f"\n--- Pobieram notariuszy na literę: {litera.upper()} ---")
        url_notariusze = f"https://rejent.poznan.pl/wykaz_notariuszy/{litera}/"
        try:
            czas_pauzy = random.uniform(0.3, 0.7)
            time.sleep(czas_pauzy)
            response = requests.get(url_notariusze, headers=headers)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, "html.parser")
            wizytowki = soup.find_all('article', class_=re.compile(r'elementor-post'))

            if not wizytowki:
                print(f"Uwaga: Nie znalazłem wizytówek na stronie {litera.upper()}")
                continue
        
            for wizytowka in wizytowki:
                post_text_div = wizytowka.find('div', class_='elementor-post__text')
                if not post_text_div:
                    continue # Jeśli z jakiegoś powodu go nie ma, pomiń tę wizytówkę
                h3_tag = post_text_div.find('h3', class_='elementor-post__title')

                if h3_tag and h3_tag.find('a'):
                    a_tag = h3_tag.find('a')
                    nazwa = a_tag.text.strip()
                    www = a_tag.get('href', 'Brak strony')
                else:
                    nazwa = "Brak nazwy"
                    www = "Brak strony"

                # --- E-mail (w div.elementor-post__excerpt) ---
                excerpt_div = post_text_div.find('div', class_='elementor-post__excerpt')
                if excerpt_div:
                    caly_tekst = excerpt_div.text
                    znalezione_maile = email_pattern.findall(caly_tekst)
                    email = znalezione_maile[0] if znalezione_maile else "Brak e-maila"
                else:
                    email = "Brak e-maila"
                print(f"-> {nazwa} | E-mail: {email} | WWW: {www}")
                writer.writerow([nazwa, email, www])
        except requests.exceptions.RequestException as e:
            print(f"Błąd przy pobieraniu strony {url_notariusze}: {e}")

    # KATALOGFIRMA

    print("\n=== ROZPOCZYNAM POBIERANIE Z KATALOGFIRMA.PL ===")
    url_katalogfirma = "https://katalogfirma.pl/lista-firm/"

    try:
        # Zabezpieczenie przed pobraniem
        czas_pauzy = random.uniform(0.5, 1.0)
        time.sleep(czas_pauzy)
        
        # POPRAWKA 1: Używamy prawidłowej zmiennej url_katalogfirma
        response = requests.get(url_katalogfirma, headers=headers)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, "html.parser")

        firmy = soup.find_all('div', class_='lsd-row')

        # POPRAWKA 2: Pętla musi być WCIĘTA, aby działała wewnątrz with open(...)
        for firma in firmy:
            
            # 1. NAZWA (z tagu h3 z klasą lsd-listing-title)
            name_tag = firma.find('h3', class_='lsd-listing-title')
            nazwa = name_tag.text.strip() if name_tag else "Brak nazwy"
            
            # 2. E-MAIL
            email_tag = firma.find('span', itemprop='email')
            
            if email_tag:
                # Rozwiązanie problemu "protected email" z wtyczki Anti-Spam
                # Sprawdzamy czy wewnątrz email_tag ukryto atrybut data-enc-email
                mail_link = email_tag.find('a', class_='mail-link')
                
                if mail_link and 'data-enc-email' in mail_link.attrs:
                     # Znaleźliśmy zaszyfrowany mail! Rozszyfrowujemy go.
                     encrypted_mail = mail_link['data-enc-email']
                     # Szyfr ROT13, np. p staje się c
                     import codecs
                     email = codecs.decode(encrypted_mail, 'rot_13').replace('[ng]', '@')
                else:
                    # Klasyczne pobranie, jeśli nie jest zaszyfrowany
                    email = email_tag.text.strip()
            else:
                email = "Brak e-maila"
                
            # 3. STRONA WWW
            contact_info = firma.find('div', class_='lsd-listing-contact-info')
            
            if contact_info:
                a_tag = contact_info.find('a', href=re.compile(r'^http'))
                if a_tag:
                    www = a_tag['href']
                else:
                    www = "Brak strony"
            else:
                www = "Brak strony"
                
            print(f"-> {nazwa} | E-mail: {email} | WWW: {www}")
            writer.writerow([nazwa, email, www])
            
    except requests.exceptions.RequestException as e:
        print(f"Błąd przy pobieraniu strony {url_katalogfirma}: {e}")

    # NOTARIUSZE.WAW
    print("\n=== ROZPOCZYNAM POBIERANIE Z NOTARIUSZE.WAW ===")
    kody_miast = [32, 1, 12, 11, 102, 64, 116]

    try:
        for kod_miasta in kody_miast:
            url_notariusze = f"https://notariusze.waw.pl/znajdz/znajdz-notariusza.php?search_name=&search_city={kod_miasta}&search_district=&search_street="
            czas_pauzy = random.uniform(0.5, 1.0)
            time.sleep(czas_pauzy)
            response = requests.get(url_notariusze, headers=headers)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, "html.parser")

            notariusze = soup.find_all('li', class_='notary-result')

            if not notariusze:
                print("Brak notraiuszy dla kodu miasta")
                continue

            for notariusz in notariusze:
                name_li = notariusz.find("li", class_="name")
                if name_li and name_li.find("a"):
                    nazwa = name_li.find("a").text.strip()
                else:
                    nazwa = "Brak nazwy"

                email_li = notariusz.find("li", class_="email")
                if email_li and email_li.find("a"):
                    email = email_li.find("a").text.strip()

                    if not email:
                         # Zmieniamy całą zawartość elementu li na tekst
                         caly_tekst = email_li.text 
                         # Używamy naszego psa tropiącego (regex)
                         znalezione_maile = email_pattern.findall(caly_tekst)
                         email = znalezione_maile[0] if znalezione_maile else "Brak e-maila"
                else:
                    email = "Brak e-maila"
                
                www = "Brak strony"

                print(f"-> {nazwa} | {email} | {www}")
                writer.writerow([nazwa, email, www])
    except requests.exceptions.RequestException as e:
            print(f"Błąd przy pobieraniu strony {url_notariusze}: {e}")