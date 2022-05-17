from rich.prompt import Prompt as prompt
from rich import *
from rich.table import *
import os

# Rich is nodig, pip install rich


def setup(opties, contacten, contactenNamen):

    opties.add_column("Optie", justify="left", no_wrap=True, style="cyan")
    opties.add_column("Actie", justify="left", style="magenta")
    opties.add_column("Optie", justify="left", style="cyan")
    opties.add_column("Actie", justify="left", style="magenta")

    opties.add_row("1.", "Bekijk jouw contacten", "4.", "Verwijder een contact")
    opties.add_row("2.", "Voeg contact toe", "5.", "Sla mijn contacten op")
    opties.add_row("3.", "Pas een contact aan", "", "")

    confile = open("contacten.txt")
    for line in confile: # Zet de contacten in de dict
        contactNaam = line.split(",")[0]
        contactTelefoon = line.split(",")[1]
        contacten[contactNaam] = contactTelefoon
        contactenNamen.append(contactNaam)
    confile.close()
    return opties, contacten, contactenNamen

def doorgaan(): # Wilt de gebruiker doorgaan?
    doorgaan = prompt.ask("Wil je doorgaan?", choices=["y", "n", "qq", ""]).lower()
    if doorgaan == "y" or doorgaan == "":
        return True
    elif doorgaan == "n" or doorgaan == "qq":
        return False


def update(contacten):
    print("\n" * 150)
    contactenTable = Table(title="Contacten") # Pas alles aan

    contactenTable.add_column("Contact", justify="left", style="green")
    contactenTable.add_column("Telefoonnummer", justify="left", style="yellow")

    for naam in contacten:
        contactenTable.add_row(naam, contacten[naam])

    return contactenTable


def verwijderContact(contacten):
    wie = prompt.ask("[green]Wie wil je verwijderen?", choices=contacten)
    contacten.pop(wie) # Haal het contact weg
    print("[red]Verwijderd!")
    return contacten

def bekijkContacten(contactenTable, contacten):
    contactenTable = update(contacten)
    return contactenTable # Laat de contacten zien

def voegContactToe(contacten):
    nieuwNaam = prompt.ask("[green]Wie wil je toevoegen?")
    nieuwTelefoonnummer = prompt.ask(f"[yellow]Wat is {nieuwNaam}'s telefoonnummer?")
    contacten[nieuwNaam] = nieuwTelefoonnummer # Pas het aan
    return contacten

def pasContactAan(contacten):
    pasNaam = prompt.ask("[green]Wie wil je aanpassen?", choices=contacten)
    aanpassen = prompt.ask("[red]Wat wil je aanpassen?", choices=["Telefoonnummer".lower(), "Naam".lower()]).lower()
    if aanpassen == "telefoonnummer":
        aanpassenValue = prompt.ask("[yellow]Naar wat wil je het veranderen?")
        contacten[pasNaam] = aanpassenValue
    elif aanpassen == "naam":
        aanpassenValue = prompt.ask("[green]Naar wat wil je het veranderen?")
        contactTelefoonnummer = contacten[pasNaam]
        contacten.pop(pasNaam)
        contacten.update({aanpassenValue: contactTelefoonnummer})
    return contacten
    print("[green]Aangepast!")

def slaContactenOp(contacten):
    newconfile = ""
    for contact in contacten: # Zet alle contacten in een string
        newconfile += f"{contact},{contacten[contact]},\n"
    confile = open("contacten.txt", "r+")
    confile.truncate(0) # Verwijder alles in contacten.txt
    confile.write(newconfile) # Voeg de nieuwe contacten toe
    confile.close()
    print("[green]Opgeslagen!")


def main(): # main
    contacten = {}
    contactenNamen = []
    opties = Table(title="Opties")
    contactenTable = Table(title="Contacten")
    r = True
    setups = setup(opties, contacten, contactenNamen)
    opties = setups[0]
    contacten = setups[1]
    contactenNamen = setups[2]


    while r:
        print("\n"*150)
        print(opties)
        optie = prompt.ask("Selecteer een optie", choices=["1", "2", "3", "4", "5", "qq"], show_choices=False)
        if optie == "1":
            print(bekijkContacten(contactenTable, contacten))
        elif optie == "2":
            contacten = voegContactToe(contacten)
            print("[green]Toegevoegd!")
        elif optie == "3":
            contacten = pasContactAan(contacten)
        elif optie == "4":
            contacten = verwijderContact(contacten)
        elif optie == "5":
            slaContactenOp(contacten)
        elif optie == "qq":
            r = False
        r = doorgaan()

main()