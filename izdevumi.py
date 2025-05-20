import time 
from googlesearch import search 
import requests 
import os 
import pandas 

# Iepriekš definēti piemēri kategoriju noteikšanai
kategoriju_piemeri = {
    "rimi": "Ēdiens",
    "maxima": "Ēdiens",
    "circle k": "Transports",
    "latvenergo": "Rēķini",
    "tele2": "Rēķini",
    "zara": "Apģērbs",
    "h&m": "Apģērbs"
    # var vēl papildināt
}

meklesanas_cache = {}

def meklet_kategoriju_google(vieta):
    try:
        vaicajums = f"{vieta} nozare site:firmas.lv"
        rezultati = list(search(vaicajums, num_results=3, lang="lv")) 
        for url in rezultati:
            print(f"Meklēju lapā: {url}")
            try:
                r = requests.get(url, timeout=5) 
                r.raise_for_status() 
                html = r.text.lower() 
                if any(atslegvards in html for atslegvards in ["ēdināšana", "restorāns", "kafejnīca"]):
                    return "Ēdiens"
                elif any(atslegvards in html for atslegvards in ["transports", "degviela", "autobuss"]):
                    return "Transports"
                elif any(atslegvards in html for atslegvards in ["telekom", "internets", "mobils", "īre", "namu apsaimniekošana", "apkure"]):
                    return "Rēķini"
                elif any(atslegvards in html for atslegvards in ["apģērbs", "drēbes", "mode", "apģērbu veikals", "apģērbu tirdzniecība"]):
                    return "Apģērbs"
            except Exception as e:
                print(f"Neizdevās ielādēt lapu {url}: {e}")
        return "Cits"
    except Exception as e:
        print(f"Kļūda Google meklēšanā vai lapas apstrādē: {e}")
        return "Cits"

def noteikt_kategoriju(vieta):
    vieta_lower = vieta.lower() 
    for atslegv in kategoriju_piemeri:
        if atslegv in vieta_lower:
            return kategoriju_piemeri[atslegv]

    if vieta in meklesanas_cache:
        return meklesanas_cache[vieta]

    print(f"Nezināma kategorija — meklēju internetā: {vieta}")
    time.sleep(1) 
    kateg = meklet_kategoriju_google(vieta)
    meklesanas_cache[vieta] = kateg
    return kateg

def lasit_izdevumus(fails):
    if not os.path.exists(fails):
        print(f"Fails {fails} nav atrasts. Pārbaudi ceļu un faila nosaukumu.")
        exit(1)

    if fails.endswith(".csv"):
        df = pandas.read_csv(fails, encoding="utf-8") 
    elif fails.endswith(".xlsx"):
        df = pandas.read_excel(fails)
    else:
        print("Atbalstīti tikai CSV un XLSX faili.")
        exit(1)

    izdevumi = [] 
    for _, row in df.iterrows(): 
        vieta = str(row["Iegādes vieta"])
        try:
            izd = float(row["Izdevumi"])
        except ValueError:
            print(f"Nevar pārveidot izdevumus: {row['Izdevumi']}, rindā ar iegādes vietu: {vieta}")
            continue
        kategorija = noteikt_kategoriju(vieta)
        izdevumi.append({"iegādes vieta": vieta, "izdevumi": izd, "kategorija": kategorija}) 
    return izdevumi

def main():
    fails = "dati/izdevumi.csv"  # vai "dati/izdevumi.xlsx"
    izdevumi = lasit_izdevumus(fails)

    print("\n--- Izdevumu saraksts ---")
    max_vieta = max(len(ieraksts['iegādes vieta']) for ieraksts in izdevumi)
    vieta_width = max(max_vieta, len("Iegādes vieta"))
    izd_width = max(15, len("Izdevumi (EUR)"))
    kateg_width = max(15, len("Kategorija"))

    print(f"{'Iegādes vieta':<{vieta_width}}  {'Izdevumi (EUR)':>{izd_width}}  {'Kategorija':<{kateg_width}}") 
    print("-" * (vieta_width + izd_width + kateg_width + 4))

    for ieraksts in izdevumi:
        vieta = ieraksts['iegādes vieta']
        izd = ieraksts['izdevumi']
        kategorija = ieraksts['kategorija']
        print(f"{vieta:<{vieta_width}}  {izd:>{izd_width}.2f}  {kategorija:<{kateg_width}}")

    kategoriju_kopsavilkums = {}
    for ieraksts in izdevumi:
        kateg = ieraksts['kategorija']
        izd = ieraksts['izdevumi']
        kategoriju_kopsavilkums[kateg] = kategoriju_kopsavilkums.get(kateg, 0) + izd

    print("\n--- Kopējie izdevumu katrā kategorijā ---")
    max_kateg = max(max(len(atslegvards) for atslegvards in kategoriju_kopsavilkums.keys()), len("Kategorija"))
    print(f"{'Kategorija':<{max_kateg}}  {'Kopējie izdevumi (EUR)':>24}")
    print("-" * (max_kateg + 26))

    for kategorija, kopējie_izdevumi in kategoriju_kopsavilkums.items():
        print(f"{kategorija:<{max_kateg}}  {kopējie_izdevumi:24.2f}")

if __name__ == "__main__":
    main()
