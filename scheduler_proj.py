import tkinter as tk
from tkinter import ttk
from plyer import notification
import schedule
from requests_html import HTMLSession
import requests

# Function to display notification
def job():
    global finalCity, temp, unit, desc
    notification.notify(
        title='Weather Scheduler',
        message=f"{finalCity} has a temperature of: {temp}, {unit} and is {desc}",
        timeout=10,
    )

# Function to schedule notifications based on user input
def show():
    global finalCity, selectedOccurrence, durationValue
    intDuration = durationInput.get()
    durationValue = int(intDuration)
    selectedOccurrence = occurenceVar.get().lower()

    if selectedOccurrence == 'seconds':
        schedule.every(durationValue).seconds.do(job)
    elif selectedOccurrence == 'minutes':
        schedule.every(durationValue).minutes.do(job)
    elif selectedOccurrence == 'hours':
        schedule.every(durationValue).hours.do(job)
    elif selectedOccurrence == 'days':
        schedule.every(durationValue).days.do(job)
    elif selectedOccurrence == 'weeks':
        schedule.every(durationValue).weeks.do(job)

# Function to check and run the schedule
def check_schedule():
    schedule.run_pending()
    root.after(1000, check_schedule)

# Initialize Tkinter window
root = tk.Tk()
root.title("Weather Scheduler")

style = ttk.Style()
style.configure("TMenubutton", font=('Helvetica', 11))
style.configure("TButton", font=('Arial', 11), padding=8)
label_font = ("Lexend", 13, "bold ")
button_font = ("Helvetica", 10, "underline")
entry_font = ('Helvetica', 11)

# UI elements
cityLabel = tk.Label(root, text="City: ", font=label_font)
occurenceLabel = tk.Label(root, text="Occurrence: ", font=label_font)
durationLabel = tk.Label(root, text="Duration: ", font=label_font)

cityLabel.grid(column=1, row=1, padx=5, pady=5)
occurenceLabel.grid(column=1, row=2, padx=5, pady=5)
durationLabel.grid(column=1, row=3, padx=5, pady=5)

cityList = ["Tagaytay", "Dasmarinas", "Trece Martires City","Oslo","Bacoor","Batangas"]
cityVar = tk.StringVar(root)
cityVar.set(cityList[0])
cityDrop = ttk.OptionMenu(root, cityVar, *cityList)

occurenceList = ["Seconds", "Minutes", "Hours", "Days", "Weeks"]
occurenceVar = tk.StringVar(root)
occurenceVar.set(occurenceList[0])
occurenceDrop = ttk.OptionMenu(root, occurenceVar, *occurenceList)

durationInput = tk.Entry(root, font=entry_font, width=11)

cityDrop.grid(column=2, row=1, padx=8, pady=5)
occurenceDrop.grid(column=2, row=2, padx=8, pady=5)
durationInput.grid(column=2, row=3, padx=8, pady=5)

# Function to start the weather retrieval and scheduling
def start():
    global finalCity, temp, unit, desc
    selectedCity = cityVar.get()
    finalCity = selectedCity.replace(" ", "%")
    url = f"https://www.google.com/search?q=weather+{finalCity}"

    s = HTMLSession()
    r = s.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0'})

    try:
        response = requests.get(url)
        if response.status_code == 200:
            temp = int(r.html.find('span#wob_tm', first=True).text)
            unit = r.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
            desc = r.html.find('span#wob_dc', first=True).text

            resultButton = tk.Button(root, text="Enter", command=show)
            resultButton.grid(column=2, row=4)

            root.after(1000, check_schedule)
        else:
            notification.notify(
                title='Weather Scheduler',
                message=f"Connection failed with status code: {response.status_code}",
                timeout=10,
            )

    except requests.RequestException as e:
        notification.notify(
            title='Weather Scheduler',
            message=f"Failed to connect: {e}",
            timeout=10,
        )

# Start button to trigger weather retrieval and scheduling setup
startButton = ttk.Button(root, text="Start", command=start)
startButton.grid(column=1, row=4,columnspan=3)

root.mainloop()
