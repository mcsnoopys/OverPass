# Overpass
# Visar ISS position och besättning i realtid.
# API: Open Notify (open-notify.org)
# Databas: Sparar position och besättning vid varje hämtning.
#
# GUI:
#   - En knapp för att hämta data
#   - Etiketter som visar position och besättning
#   - En lista med tidigare hämtningar

import tkinter as tk
import requests
import sqlite3
from datetime import datetime

conn = sqlite3.connect("Overpass.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS overpass (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, latitude REAL, longitude REAL, crew INTEGER)""")
conn.commit()
# Funktion för att hämta information om besättning på ISS


def get_astros():
    response = requests.get("http://api.open-notify.org/astros.json")
    if response.status_code == 200:
        data = response.json()
        iss_crew = [person for person in data['people']
                    if person['craft'] == "ISS"]
        names = ""
        for person in iss_crew:
            names += f"{person['name']} - ISS\n"
    return len(iss_crew), names


# Funktion för att hämta position av ISS
def get_position():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    if response.status_code == 200:
        data = response.json()
        lat = data['iss_position']['latitude']
        lon = data['iss_position']['longitude']
        return lat, lon

# sparar tid, position och mängden besättning


def save_info(timestamp, latitude, longitude, crew):
    cursor.execute("""INSERT INTO overpass (timestamp, latitude, longitude, crew)VALUES (?,?,?,?)""",
                   (timestamp, latitude, longitude, crew))
    conn.commit()

# visar det som sparades


def show_history():
    cursor.execute("SELECT * FROM overpass")
    lines = cursor.fetchall()
    output = "\n".join(
        [f"{l[1]} | LAT: {l[2]} | LON: {l[3]} | CREW: {l[4]}" for l in lines])
    label_history.config(text=output)

# Lägger ihop allt för att kunna visa information


def fetch_all():
    label_info.config(text="Loading...")
    root.update()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lat, lon = get_position()
    crew_count, crew_names = get_astros()
    save_info(timestamp, lat, lon, crew_count)
    label_info.config(
        text=f"ISS Position:\nLatitude: {lat} \nLongitude: {lon}\n\n Crew: {crew_count}\n{crew_names}")


# Detta är interface för programmet
root = tk.Tk()
root.geometry("400x600")
root.title("OverPass")

label_title = tk.Label(root, text="OverPass", font=('arial', 18, 'bold'))
label_title.pack()

label_description = tk.Label(
    root, text="Tracking the international Space Station", font=('arial', 10))
label_description.pack()

# Buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_fetch = tk.Button(frame_buttons, text="Fetch", command=fetch_all)
btn_fetch.pack(side="left", padx=5)

btn_history = tk.Button(frame_buttons, text="History", command=show_history)
btn_history.pack(side="left", padx=5)

# Frame for ISS info
frame_info = tk.LabelFrame(root, text="ISS Info",
                           padx=10, pady=10, width=240, height=260)
frame_info.pack(padx=10, pady=10)
frame_info.pack_propagate(False)

label_info = tk.Label(frame_info, text="Press fetch to track the ISS")
label_info.pack()

# Frame for History
frame_history = tk.LabelFrame(
    root, text="History", padx=10, pady=10, width=360, height=300)
frame_history.pack(padx=10, pady=10)
frame_history.pack_propagate(False)

label_history = tk.Label(frame_history, text="")
label_history.pack()


root.mainloop()
