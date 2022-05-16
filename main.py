from tkinter import *
from tkinter import messagebox
from tabulate import tabulate
import random
import pyperclip
import json
import time
# Window dimension constants
WINDOW_HEIGHT = 200
WINDOW_WIDTH = 200
PAD_X = 40
PAD_Y = 40

# Colors etc
BACKGROUND_COLOR = "white"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


# Password Generator
def generate_password():
    # Clear password field
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(1, 2)
    nr_numbers = random.randint(1, 2)

    password_list = []

    [password_list.append(random.choice(letters)) for _ in range(nr_letters)]
    [password_list.append(random.choice(symbols)) for _ in range(nr_symbols)]
    [password_list.append(random.choice(numbers)) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    # Convert back to string
    password = ''.join(password_list)

    # Insert generated password in field
    password_entry.insert(0, string=password)

    # Copy to clipboard
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():
    # Assign user data to variables
    website = website_str.get()
    email = email_str.get()
    password = password_str.get()

    # convert website to lower case
    website = website.lower()

    # JSON dictionary
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    # Give warning if there are empty fields
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Uh oh!", message="Please don't leave empty fields")
    # Otherwise, ask for confirmation and write to file
    else:
        try:
            # Look for "data.json"
            with open("data.json", "r") as file:
                data = json.load(file)
                data.update(new_data)
        # If it doesn't exist, create it and put something in it
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file)
        else:
            # If file is opened and loaded, we can write new data to it
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

        # Clear all entry fields
        website_entry.delete(0, END)
        password_entry.delete(0, END)


def search():
    website_text = website_str.get()

    # convert to lower case
    website_text = website_text.lower()

    # try to open and find key
    try:
        with open("data.json", "r") as file:
            file_data = json.load(file)
            email = file_data[website_text]["email"]
            password = file_data[website_text]["password"]
    # if key doesn't exist of if there's no json file, throw an error
    except FileNotFoundError:
        messagebox.showerror(title="No json file", message="No json file exists. Please create an entry, first")
    except KeyError:
        messagebox.showerror(title="Entry not found", message=f"An entry for {website_text} does not exist.")
    else:
        # display record
        email_entry.delete(0, END)
        password_entry.insert(0, password)
        email_entry.insert(0, email)

        # confirm clipboard copied
        clipboard_message = mesg_canvas.create_text(110, 30, text="Copied to clipboard!")
        mesg_canvas.after(800, mesg_canvas.delete, clipboard_message)





# ---------------------------- UI SETUP ------------------------------- #
# Set up our root grid
root = Tk()
root.title("Password Manager")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.config(padx=PAD_X, pady=PAD_Y, bg=BACKGROUND_COLOR)

# MyPass logo canvas
canvas = Canvas(root, height=WINDOW_HEIGHT, width=WINDOW_WIDTH, bg=BACKGROUND_COLOR, highlightthickness=0)
lock_logo = PhotoImage(file="logo.png")
lock_image = canvas.create_image(100, 100, image=lock_logo)
canvas.grid(row=0, column=1)

# Message canvas
mesg_canvas = Canvas(root, height=50, width=200, bg=BACKGROUND_COLOR, highlightthickness=0)
mesg_canvas.grid(row=5, column=1)

# Labels
website_label = Label(text="Website:", bg=BACKGROUND_COLOR)
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:", bg=BACKGROUND_COLOR)
email_label.grid(row=2, column=0)

password_label = Label(text="Password:", bg=BACKGROUND_COLOR)
password_label.grid(row=3, column=0)

# Entry fields
website_str = StringVar()
email_str = StringVar()
password_str = StringVar()

website_entry = Entry(root, textvariable=website_str, width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()

email_entry = Entry(root, textvariable=email_str, width=50)
email_entry.grid(row=2, column=1, columnspan=3)
email_entry.insert(0, "kenjameswinston@gmail.com")

password_entry = Entry(root, textvariable=password_str, width=35)
password_entry.grid(row=3, column=1,columnspan=2)

# Buttons
# The GENERATE button
generate_button = Button(root, text="Generate", bg=BACKGROUND_COLOR, width=11, command=generate_password)
generate_button.grid(row=3, column=3)

# The ADD button
add_button = Button(root, text="Add", bg=BACKGROUND_COLOR, width=33, command=save_data)
add_button.grid(row=4, column=1, columnspan=2)

# The search button
search_button = Button(root, text="Search", bg=BACKGROUND_COLOR, width=11, command=search)
search_button.grid(row=1, column=3)
root.mainloop()
