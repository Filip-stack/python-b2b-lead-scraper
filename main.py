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

wojewodztwa_do_pobrania = {
    "Mazowieckie": 349,   
    "Małopolskie": 332,   
    "Śląskie": 327,   
    "Dolnośląskie": 245,
    "Wielkopolskie": 238,
    "Pomorskie": 178,
    "Lubelskie": 89,
    "Zachodniopomorskie": 112,
    "Podkarpackie": 110,
    "Kujawsko-Pomorskie": 105,
    "Warmińsko-Mazurskie": 64,
    "Podlaskie": 64,
    "Łódzkie": 131,
    "Świętokrzyskie": 54,
    "Opolskie": 39,
    "Lubuskie": 46,
    "Cała+Polska": 92
}
widziane_maile = set()

with open(sciezka_do_pliku, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Nazwa firmy", "Email", "Strona internetowa"])
    

    for wojewodztwo, liczba_stron in wojewodztwa_do_pobrania.items():
        print(f"\n=======================================================")
        print(f"=== ROZPOCZYNAM POBIERANIE WOJEWÓDZTWA: {wojewodztwo.upper()} ===")
        print(f"=======================================================\n")
        
        for page_num in range(0, liczba_stron):
            print(f"Pobieram stronę {page_num} ({wojewodztwo})...")
            

            url = f"https://www.firmyogloszenia.pl/showstate2.php?state={wojewodztwo}&copage={page_num}"
            
            try:
                czas_pauzy = random.uniform(0.3, 0.7)
                time.sleep(czas_pauzy)
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, "html.parser")
                firmy = soup.find_all("div", class_="compall")
                
                if not firmy:
                    print(f"Brak firm na stronie {page_num}. Przechodzę do kolejnej.")
                    continue
                
                for firma in firmy:
                    # nazwa
                    name_tag = firma.find("h1")
                    nazwa = name_tag.text.strip() if name_tag else "Brak nazwy"
                    
                    kontakt_tag = firma.find("span", class_="coright")
                    # e-mail
                    if kontakt_tag:
                        email = "Brak e-maila"
                    

                        for tekst in kontakt_tag.stripped_strings:
                            if email_pattern.fullmatch(tekst):
                                email = tekst
                                break
                        
                        # WWW
                        a_tag = kontakt_tag.find("a")
                        if a_tag and 'href' in a_tag.attrs:
                            www = a_tag['href']
                        else:
                            www = "Brak strony"
                    else:
                        email = "Brak e-maila"
                        www = "Brak strony"
                    if email == "Brak e-maila":
                        continue
                    
                    
                    print(f"-> {nazwa} | E-mail: {email} | WWW: {www}")
                    writer.writerow([nazwa, email, www])
                    
            except requests.exceptions.RequestException as e:
                print(f"Błąd przy pobieraniu strony {page_num} ({wojewodztwo}): {e}")
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
                    continue
                h3_tag = post_text_div.find('h3', class_='elementor-post__title')

                if h3_tag and h3_tag.find('a'):
                    a_tag = h3_tag.find('a')
                    nazwa = a_tag.text.strip()
                    www = a_tag.get('href', 'Brak strony')
                else:
                    nazwa = "Brak nazwy"
                    www = "Brak strony"

                # e-mail
                excerpt_div = post_text_div.find('div', class_='elementor-post__excerpt')
                if excerpt_div:
                    caly_tekst = excerpt_div.text
                    znalezione_maile = email_pattern.findall(caly_tekst)
                    email = znalezione_maile[0] if znalezione_maile else "Brak e-maila"
                else:
                    email = "Brak e-maila"

                if email == "Brak e-maila":
                    continue

                if email in widziane_maile:
                    print(f"[!] Pomijam duplikat: {email}")
                    continue
                widziane_maile.add(email)
                print(f"-> {nazwa} | E-mail: {email} | WWW: {www}")
                writer.writerow([nazwa, email, www])
        except requests.exceptions.RequestException as e:
            print(f"Błąd przy pobieraniu strony {url_notariusze}: {e}")

    # KATALOGFIRMA

    print("\n=== ROZPOCZYNAM POBIERANIE Z KATALOGFIRMA.PL ===")
    url_katalogfirma = "https://katalogfirma.pl/lista-firm/"

    try:
        czas_pauzy = random.uniform(0.5, 1.0)
        time.sleep(czas_pauzy)
        response = requests.get(url_katalogfirma, headers=headers)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, "html.parser")

        firmy = soup.find_all('div', class_='lsd-row')

        for firma in firmy:
            
            # 1. NAZWA (z tagu h3 z klasą lsd-listing-title)
            name_tag = firma.find('h3', class_='lsd-listing-title')
            nazwa = name_tag.text.strip() if name_tag else "Brak nazwy"
            
            # 2. E-MAIL
            email_tag = firma.find('span', itemprop='email')
            
            if email_tag:
                # sprawdzenie czy wewnątrz email_tag ukryto atrybut data-enc-email
                mail_link = email_tag.find('a', class_='mail-link')
                
                if mail_link and 'data-enc-email' in mail_link.attrs:
                     encrypted_mail = mail_link['data-enc-email']
                     import codecs
                     email = codecs.decode(encrypted_mail, 'rot_13').replace('[ng]', '@')
                else:
                    email = email_tag.text.strip()
            else:
                email = "Brak e-maila"
                
            # WWW
            contact_info = firma.find('div', class_='lsd-listing-contact-info')
            
            if contact_info:
                a_tag = contact_info.find('a', href=re.compile(r'^http'))
                if a_tag:
                    www = a_tag['href']
                else:
                    www = "Brak strony"
            else:
                www = "Brak strony"
            if email == "Brak e-maila":
                continue

            if email in widziane_maile:
                print(f"[!] Pomijam duplikat: {email}")
                continue
            widziane_maile.add(email)
                
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
                         caly_tekst = email_li.text 
                         # Używamy naszego psa tropiącego (regex)
                         znalezione_maile = email_pattern.findall(caly_tekst)
                         email = znalezione_maile[0] if znalezione_maile else "Brak e-maila"
                else:
                    email = "Brak e-maila"
                
                www = "Brak strony"
                if email == "Brak e-maila":
                    continue

                if email in widziane_maile:
                    print(f"[!] Pomijam duplikat: {email}")
                    continue
                widziane_maile.add(email)

                print(f"-> {nazwa} | {email} | {www}")
                writer.writerow([nazwa, email, www])
    except requests.exceptions.RequestException as e:
            print(f"Błąd przy pobieraniu strony {url_notariusze}: {e}")

    def decode_cfemail(cfemail):
        try:
            r = int(cfemail[:2], 16)
            email = ''.join([chr(int(cfemail[i:i+2], 16) ^ r) for i in range(2, len(cfemail), 2)])
            return email
        except Exception:
            return "Błąd dekodowania"

    print("\n=== GOSPODARKA MORSKA SZUKANIE ===")
    try:
        for i in range(1, 295):
            url_gosp = f"https://www.gospodarkamorska.pl/lista-firm?page={i}"
            czas_pauzy = random.uniform(0.5, 1.0)
            time.sleep(czas_pauzy)
            response = requests.get(url_gosp, headers=headers)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, "html.parser")

            firmy = soup.find_all("div", class_="cate_box")
            
            if not firmy:
                print("Nie znaleziono firm pod linkiem")
                continue

            for firma in firmy:
                # --- 1. NAZWA ---
                name_h2 = firma.find("h2", class_="article-h1-title")
                if name_h2:
                    nazwa = name_h2.text.strip()
                else:
                    nazwa = "Brak nazwy"

                # --- 2. E-MAIL ---
                email = "Brak e-maila"
                info_divs = firma.find_all("div", class_="cate_box_info")

                for info in info_divs:
                    h6_tag = info.find("h6")
                    if h6_tag and h6_tag.text.strip() == "E-mail:":
                        p_tag = info.find("p")
                        if p_tag:
                            # sprawdzenie, czy cloudfare zablokowal maila
                            cf_span = p_tag.find(class_='__cf_email__')
                            if cf_span and 'data-cfemail' in cf_span.attrs:
                                email = decode_cfemail(cf_span['data-cfemail'])
                            else:
                                email = p_tag.text.strip()
                            break

                # WWW
                site_div = firma.find("div", class_="cate_box_link")
                www = "Brak strony" 
                
                if site_div:
                    a_tag = site_div.find('a', href=re.compile(r'^http', re.IGNORECASE))
                    if a_tag:
                        www = a_tag['href']
                if email == "Brak e-maila":
                    continue

                if email in widziane_maile:
                    print(f"   [!] Pomijam duplikat: {email}")
                    continue
                widziane_maile.add(email)

                
                print(f"-> {nazwa} | {email} | {www}")
                writer.writerow([nazwa, email, www])
            
    except requests.exceptions.RequestException as e:
        print(f"Błąd przy pobieraniu strony {url_gosp}: {e}")

    api_url = "https://www.portalmorski.pl/index.php?option=com_catalogue&task=category&format=raw"

    def decode_cfemail(cfemail):
        try:
            r = int(cfemail[:2], 16)
            email = ''.join([chr(int(cfemail[i:i+2], 16) ^ r) for i in range(2, len(cfemail), 2)])
            return email
        except Exception:
            return "Błąd dekodowania"

    print("\n=== ROZPOCZYNAM POBIERANIE Z PORTALMORSKI.PL ===")

    for start_offset in range(0, 4100, 10):
        print(f"Pobieram paczkę firm od pozycji: {start_offset}...")
        
        payload = {
            "qs": "",
            "city": "",
            "catid": "",
            "province": "",
            "id": "1", 
            "start": str(start_offset) 
        }
        
        try:
            czas_pauzy = random.uniform(1.0, 2.0)
            time.sleep(czas_pauzy)
            
            response = requests.post(api_url, headers=headers, data=payload)
            response.raise_for_status()

            if not response.text.strip():
                 print("Dotarłem do końca bazy,zamykam pobieranie.")
                 break
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            firmy = soup.find_all("div", class_="company-container")

            if not firmy:
                 print("⚠️ Pusta paczka (brak klasy company-container).")
                 continue

            for firma in firmy:
                # 1. NAZWA
                h3_tag = firma.find("h3")
                if h3_tag:
                    nazwa = h3_tag.text.strip()
                else:
                    nazwa = "Brak nazwy"

                # 2. E-MAIL 
                caly_tekst = firma.get_text(separator=' ')
                znalezione_maile = email_pattern.findall(caly_tekst)
                email = znalezione_maile[0] if znalezione_maile else "Brak e-maila"
                
                # Odkodowywanie cloudflare
                cf_span = firma.find(class_='__cf_email__')
                if cf_span and 'data-cfemail' in cf_span.attrs:
                    email = decode_cfemail(cf_span['data-cfemail'])
                www = "Brak strony"
                wszystkie_linki = firma.find_all("a")
                for link in wszystkie_linki:
                    href = link.get('href', '')
                    # Ignorujemy linki wewnętrzne Portalu Morskiego
                    if (href.startswith('http') or href.startswith('www.')) and 'portalmorski.pl' not in href:
                        www = href
                        break # Mamy to, kończymy szukać WWW
                if email == "Brak e-maila":
                    continue

                if email in widziane_maile:
                    
                    print(f"[!] Pomijam duplikat: {email}")
                    continue
                widziane_maile.add(email)

                print(f"-> {nazwa} | {email} | {www}")
                writer.writerow([nazwa, email, www])
        except requests.exceptions.RequestException as e:
            print(f"Błąd przy pobieraniu paczki {start_offset}: {e}")

    
    



    

