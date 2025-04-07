
# Na začátku programu si naimportuju všechny potřebné knihovny. 
# Importy zapisuju postupně v průběhu psaní funkcí. 
# (Jedině pokud bych importovala nějakou velkou knihovnu a nebylo nutné ji 
# při každém spuštění importovat, je na zvážení dát import dovnitř funkce. )

import random
import sys
from rich.console import Console
import os
console = Console()
obrazek_sibenice = 0

# Načti náhodně slovo ze souboru words.txt a ulož ho do proměnné hledane_slovo.
def nacti_hledane_slovo():
    try:
        with open("words.txt", "r", encoding="utf-8") as file:
        # Každé slovo je na novém řádku, vytvořím seznam všech slov ze souboru 
        # a na ten pak použiju random.choice. 
        # Plus podmínka if line.strip() - tzn. pokud řádek nebyl prázdný.
            return random.choice([line.strip() for line in file if line.strip()])
    except FileNotFoundError: 
        print("Chyba: Soubor 'words.txt' nebyl nalezen. Ujistěte se, že soubor existuje.")
    except IndexError:
        print("Chyba: Soubor 'words.txt' je prázdný.")
    except Exception as e:
        print(f"Nastala neočekávaná chyba: {e}")
    return None

def vykresli_sibenici(index):
    try:
        from hangman_pictures import HANGMAN_PICS
        #global obrazek_sibenice
        odsazeni = " " * 22  # Přidá 22 mezer pro odsazení
        # Přidá odsazení před každý řádek šibenice
        obrazek = HANGMAN_PICS[index].split("\n")
        obrazek_s_odsazenim = "\n".join(odsazeni + radek for radek in obrazek)
        print(obrazek_s_odsazenim)
    except ImportError:
        print("Chyba: Nepodařilo se importovat HANGMAN_PICS z hangman_pictures.")
    except IndexError:
        print("Chyba: Index obrázku šibenice je mimo rozsah.")

# def zobraz_hraci_pole(hledane_slovo):
#    hraci_pole = ["_"] * len(hledane_slovo)
#    return hraci_pole

def zobraz_stav_hry(stav, hledane_slovo):
    console.print("-" * 6 + "H" + "-" * 6 + "A" + "-" * 6 + "N" + "-" * 6 + "G" + "-" * 6 + "M" + "-" * 6 + "A" + "-" * 6 + "N" + "-" * 6, style="bold magenta on black")

    vykresli_sibenici(stav["obrazek"])
    print(" ")
    print("                        " + " ".join(stav["pole"]))
    print(f"\nNeuhodnutá písmena: {', '.join(stav['neuhodnuta'])}\n")


def nacti_pismeno():
    while True:
        pismeno = input("\n\n                 Chceš utéct oprátce? \n\n                   Zadej písmeno: ")
        if len(pismeno) > 1:
            console.print("\nŘeklo se JEDNO písmeno! Tady někdo zraje pro šibenici...", style="yellow")
        elif pismeno in "aábcčdďeéěfghiíjklmnňoópqrřsštťuúůvwxyýzž":
            return pismeno
        else:
            print("\n    Na mou duši, musí to být písmeno. Malé tiskací. ")

def zapis_pismeno_do_pole(hledane_slovo, pismeno, hraci_pole):
    pozice = [index for index, znak in enumerate(hledane_slovo) if znak == pismeno]
    for index in pozice:
        hraci_pole[index] = pismeno
    return hraci_pole

def hraj_kolo(hledane_slovo):
    stav = {
        "obrazek": 0,
        "pole": ["_"] * len(hledane_slovo),
        "neuhodnuta": [],
        "vitez": False,
        "obesen": False
    }

    while not stav["vitez"] and not stav["obesen"]:
        print()
        zobraz_stav_hry(stav, hledane_slovo)

        pismeno = nacti_pismeno()

        if pismeno in stav["pole"] or pismeno in stav["neuhodnuta"]:
            console.print("Sorry kámo, ale tohle už tady bylo. Zkus něco jiného.", style="italic red")
        elif pismeno in hledane_slovo:
            stav["pole"] = zapis_pismeno_do_pole(hledane_slovo, pismeno, stav["pole"])
            if "_" not in stav["pole"]:
                stav["vitez"] = True
        else:
            stav["obrazek"] += 1
            stav["neuhodnuta"].append(pismeno)
            if stav["obrazek"] >= 6:
                stav["obesen"] = True

    return stav["vitez"], stav["obrazek"], stav["pole"]

def vypis_vysledky(jsi_vitez, hledane_slovo, hraci_pole, obrazek_sibenice):
    if jsi_vitez:
             print(" ")
             console.print("🌟🏆🌟🏆🌟🏆🌟🏆🌟🏆🌟 GRATULUJI!!! 🌟🏆🌟🏆🌟🏆🌟🏆🌟🏆🌟", style="bold green")
             print(" ")
             console.print(" " * 24 + " ".join(hledane_slovo), style="bold yellow")
             console.print("\n   Gratulace převeliká, tentokrát jsi vyhrál na celé čáře! \n\n              Pro šibenici ještě nejsi zralý, \n             máš koule pokoušet štěstěnu dál? 😈\n", style="green")
    else:
        vykresli_sibenici(obrazek_sibenice)
        print(" ")
        console.print("💀❌💀❌💀❌💀❌💀❌💀❌ GAME OVER ❌💀❌💀❌💀❌💀❌💀❌💀", style="bold red")
        console.print(f"\n                Pověste ho vejš, ať se houpá!!\n\n             Tentokrát to nevyšlo, oprátka čeká...\n\n                    Hledals slovo [bold yellow]{hledane_slovo}[/bold yellow].\n\n           Easy, co? Tak co takhle dát další kolo? 😈\n", style="red")

def dalsi_kolo():
    while True:  # Smyčka opakuje dotaz, dokud není platná odpověď
        chci_dalsi_kolo = input("                     Chceš hrát? ano/ne\n\n                            ").strip().lower()
        if chci_dalsi_kolo == "ano":
            print("\n                Skvělá volba, jdeme na to!")
            break  # Platná odpověď, smyčka se ukončí
        elif chci_dalsi_kolo == "ne":
            print("\n        Díky za hru, třeba zase někdy příště, šibeničníku... ")
            sys.exit()  # Ukončí program
        else:
            print("\n           Řekni to na rovinu: ano - ne. Nic mezi tím.")

# Tělo celého hangmana, opakuje se dokud uživatel nezvítězí nebo nevisí. 
def main():
    console.print("\n                     H A N G M A N                      ", style = "reverse bold")
    print(" ")
    console.print("                 ⚔️  . . . 👤 . . . ⚔️ \n\n                   Kat je připraven! \n\n         Překonej jeho hádanku, nebo čel oprátce!", style="cyan")
    #global obrazek_sibenice
    while True: 
        hledane_slovo = nacti_hledane_slovo()
        jsi_vitez, obrazek_sibenice, hraci_pole = hraj_kolo(hledane_slovo)
        vypis_vysledky(jsi_vitez, hledane_slovo, hraci_pole, obrazek_sibenice)
        dalsi_kolo()



if __name__ == "__main__":
    main()
        
       
        


            
