from rich.prompt import Prompt as prompt
from rich import *
from rich.table import *
import os

# Rich is nodig, pip install rich

opties = Table(title="Opties")

opties.add_column("Optie", justify="left", no_wrap=True, style="cyan")
opties.add_column("Actie", justify="left", style="magenta")
opties.add_column("Optie", justify="left", style="cyan")
opties.add_column("Actie", justify="left", style="magenta")

opties.add_row("1.", "Bekijk jouw contacten", "4.", "Verwijder een contact")
opties.add_row("2.", "Voeg contact toe", "5.", "Sla mijn contacten op")
opties.add_row("3.", "Pas een contact aan", "", "")

r = True
contacten = {}
confile = open("contacten.txt")
for line in confile:
    contactNaam = line.split(",")[0]
    contactTelefoon = line.split(",")[1]
    contacten[contactNaam] = contactTelefoon
confile.close()

def doorgaan():
    global r
    doorgaan = prompt.ask("Wil je doorgaan?", choices=["y", "n", "\n"]).lower()
    if doorgaan == "y" or doorgaan == "\n":
        return True
    elif doorgaan == "n":
        return False
contactenTable = Table(title="Contacten")

def reset():
    print("\n" * 150)
    global contactenTable
    contactenTable = Table(title="Contacten")

    contactenTable.add_column("Contact", justify="left", style="green")
    contactenTable.add_column("Telefoonnummer", justify="left", style="yellow")

    for naam in contacten:
        contactenTable.add_row(naam, contacten[naam])
while r:
    print("\n"*150)
    print(opties)
    optie = prompt.ask("Selecteer een optie", choices=["1", "2", "3", "4", "5"], show_choices=False)
    reset()
    if optie == "1":
        print(contactenTable)
        if not doorgaan():
            r = False
    elif optie == "2":
        nieuwNaam = prompt.ask("[green]Wie wil je toevoegen?")
        nieuwTelefoonnummer = prompt.ask(f"[yellow]Wat is {nieuwNaam}'s telefoonnummer?")
        contacten[nieuwNaam] = nieuwTelefoonnummer
        if not doorgaan():
            r = False
    elif optie == "3":
        pasNaam = prompt.ask("[green]Wie wil je aanpassen?", choices=contacten)
        aanpassen = prompt.ask("[red]Wat wil je aanpassen?", choices=["Telefoonnummer".lower(), "Naam".lower()]).lower()
        if aanpassen == "telefoonnummer":
            aanpassenValue = prompt.ask("[yellow]Naar wat wil je het veranderen?")
        elif aanpassen == "naam":
            aanpassenValue = prompt.ask("[green]Naar wat wil je het veranderen?")
        contacten[pasNaam] = aanpassenValue
        print("[green]Aangepast!")
        if not doorgaan():
            r = False
    elif optie == "4":
        wie = prompt.ask("[green]Wie wil je verwijderen?")
        contacten.pop(wie)
        print("[red]Verwijderd!")
        print(contacten)
        if not doorgaan():
            r = False
    elif optie == "5":
        newconfile = ""
        for contact in contacten:
            newconfile += f"{contact},{contacten[contact]},\n"
        confile = open("contacten.txt", "r+")
        confile.truncate(0)
        confile.write(newconfile)
        confile.close()
        print("[green]Opgeslagen!")
        if not doorgaan():
            r = False