# Modules that I used
from tkinter import *
from PIL import ImageTk, Image
import requests
import json

# Switching frames function
def switch_to_frame(frame):
    frame.tkraise()

# My main function to acess files in JSON file
def show_entry():
    # Hinding initial labels, that would be replaced by the info

    # Hide labels in FrameA
    for widget in FrameA.winfo_children(): # a function to get child widgets
        if widget != result_label: # If widget not in result label
            widget.place_forget() # Hides the widget

    # Hide labels in FrameB
    for widget in FrameB.winfo_children():
        if widget != result_label:
            widget.place_forget()

    # Hide labels in FrameC
    for widget in FrameC.winfo_children():
        if isinstance(widget, Label) and widget != result_label: # Hide except 1 button, which is to switch frames
            widget.place_forget()

    # Getting info from user
    entered_text = UserSearch.get()#.title() # Get info from the the entry 
    for country in data: # Loop to get each wanted info
        if entered_text == country['name']['common']: # If entered text matches a country in the api
            official_name = country['name']['official'] # Getting the data from api and storing in a variables to be used.
            subregion = country.get('subregion', 'Not Available') # A get method, because some country don't have this data.
            region = country['region']
            capital = country['capital']
            continent = country['continents']
            timezone = country['timezones']
            weekstart = country['startOfWeek']

            # Extract currencies information
            currencies_data = country['currencies']
            currencies_info = "\n".join([f"{code}: {info['name']} ({info['symbol']})" for code, info in currencies_data.items()])

            # Extract flag information using get function
            flag_info = country.get('flags', {})
            flag_png_link = flag_info.get('png', 'default_flag.png')  # Provide a default flag URL

            # Output in an organize manner, storing it all in one variable
            result_text = (
            f"Selected Country: {entered_text}\n"
            f"Official Name: {official_name}\n"
            f"Continent: {', '.join(continent)}\n"
            f"Region: {region}\n"
            f"Subregion: {subregion}\n"
            f"Capitals: {', '.join(capital)}\n"
            f"Currencies:\n{currencies_info}\n"
            f"Timezone: {', '.join(timezone)}\n"
            f"Start of the Week: {(weekstart)}\n"
            )

            # Check if 'alt' key is present in flag_info
            if 'alt' in flag_info:
                flag_alt_text = flag_info['alt']
            else:
                flag_alt_text = 'No Flag info available for the selected country.'

            #Output will be on frame C
            result_label.config(text=result_text, compound="top")

            try:
                # Load the flag image using Pillow
                flag_image = Image.open(requests.get(flag_png_link, stream=True).raw)
                flag_image = ImageTk.PhotoImage(flag_image)
                # Display the flag image in FrameA
                flag_label = Label(FrameA, image=flag_image)
                flag_label.image = flag_image
                flag_label.place(x=35, y=0, height=200)
            except Exception as e:
                # Incase that flag is not available in the API
                print(f"Error loading flag image: {e}")
                flag_label = Label(FrameA, text="Flag Image Not Available", bg='white')
                flag_label.place(x=35, y=0, height=200)

            # Display the alt text in FrameB with line wrapping to fit the frame
            alt_label = Label(FrameB, text=flag_alt_text, font=("Monserat", 13), wraplength=380, bg='white')
            alt_label.place(x=10, y=10) 
            break 
    else:
        result_label.config(text=f"Selected Country: {entered_text}\nNot Found")

# API URL
url= "https://restcountries.com/v3.1/all"

# Getting data of API and storing it to a variable
response = requests.get(url)

# Storing response in a variable named data
data = response.json()

# File name of the JSON file containing API data
file_name = "all_countries_data.json"

# Save the JSON data to a file
with open(file_name, 'w') as json_file:
    json.dump(data, json_file, indent=4)

# Open the JSON file for reading
with open(file_name, 'r') as json_file:
    # Load the JSON data from the file
    data = json.load(json_file)

# Main Tkinter window
root = Tk()
root.title("World Explorer") #Add title
root.geometry('1000x700') #Ouput window size
root.resizable(0,0) #Fixed output window

# Start Frame
Start_frame = Frame(root, bg='#111D13')
img = ImageTk.PhotoImage(Image.open("logo.png") )
# Display the logo image
label = Label(Start_frame, image=img, bg='#111D13')
label.place(x=250, y=0)
Button(Start_frame, text="START", font=("impact", 30), bg='#415D43', fg='white', 
       command=lambda: switch_to_frame(frame1)).place(x=440, y= 500)
Start_frame.place(x=0,y=0, width=1000,height=700)

#  frame 1, opening page
frame1 = Frame(root, bg='#111D13')
Label(frame1, text="Welcome To World Explorer..",fg='white',bg='#111D13', font=("impact", 40)).place(x=200, y=200)
Label(frame1, text="World Explorer is an app that helps you know more about the world.",
      fg='white',bg='#111D13', font=("Monserat", 20)).place(x=100, y=300)
Label(frame1, text="Discover, Connect, and Explore with World Explorer:\nYour Gateway to Global Knowledge.",
      fg='white',bg='#111D13', font=("Monserat", 20)).place(x=200, y=335)
Label(frame1, text="Created by: Mark Buyco \n Bathspa University year 2 ",
      fg='white',bg='#111D13', font=("Monserat", 15)).place(x=10, y=30)
Button(frame1, text="Discover The World", font=('impact', 30), bg='#415D43', fg='white',
       command=lambda: switch_to_frame(frame2)).place(x=330, y= 500)
frame1.place(x=0,y=0, width=1000,height=700)

# frame 2, tagline page
frame2 = Frame(root, bg='#111D13')
Label(frame2, text="World Explorer",
      fg='white',bg='#111D13', font=("impact", 30)).place(x=390, y=30)
Label(frame2, text="Enter a country:", fg='white', bg='#111D13', 
      font=("impact", 20)).place(x=250, y=100)
UserSearch = Entry(frame2, width=25, font=("Monserat", 15))
UserSearch.place(x=450, y=110)
search_button = Button(frame2, text="Search", command=show_entry, font=("impact", 20), bg='#415D43', fg='white')
search_button.place(x=750, y=100)
frame2.place(x=0,y=0, width=1000,height=670)

# Nested Frames, isnide frame 2, which is the main app.

# Frame 2a, inside frame 2
miniframe = Frame(frame2, bg='#415D43')
miniframe.place(x=30,y=180, width=940,height=500)

# Frame A, inside miniframe
FrameA = Frame(miniframe, bg='white', bd='1', relief='ridge')
Label(FrameA, text="Country Flag will be displayed here:", font=("Monserat", 13), bg='white').place(x=10, y=10)
FrameA.place(x=20,y=20, width=400,height=200)

# Frame B, inside miniframe
FrameB = Frame(miniframe, bg='white', bd='1', relief='ridge')
Label(FrameB, text="Flag description will be displayed here:", font=("Monserat", 13), bg='white').place(x=10, y=10)
FrameB.place(x=20,y=250, width=400,height=210)

# Frame C, inside miniframe
FrameC = Frame(miniframe, bg='white', bd='1', relief='ridge')
Label(FrameC, text="Details will be displayed here:", font=("Monserat", 13), bg='white').place(x=10, y=10)
result_label = Label(FrameC, font=("Monserat", 13), justify="left", wraplength=300, bg='white')
result_label.place(x=120, y=30)
Button(FrameC, text="End", font=('impact', 30), bg='#415D43', fg='white',
       command=lambda: switch_to_frame(lastframe)).place(x=350, y= 340)
FrameC.place(x=450,y=20, width=460,height=440)

# Last Frame
lastframe = Frame(root, bg='#111D13')
Label(lastframe, text="Thank you for using World Explorer!",fg='white',bg='#111D13', font=("impact", 40)).place(x=120, y=200)
Button(lastframe, text="Start Over", font=('impact', 30), bg='#415D43', fg='white',
       command=lambda: switch_to_frame(Start_frame)).place(x=400, y= 400)
lastframe.place(x=0,y=0, width=1000,height=700)



# Show Start frame initially
switch_to_frame(Start_frame)

root.mainloop()