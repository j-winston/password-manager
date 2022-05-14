from tkinter import *
from tkinter import ttk
import pandas as pd
from tabulate import tabulate

# Window dimension constants
WINDOW_HEIGHT = 200
WINDOW_WIDTH = 200
PAD_X = 40
PAD_Y = 40

# Colors etc
BACKGROUND_COLOR = "white"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():
    # Assign user entry fields to dict
    user_df = {"Website":[website_str.get()], "Email/Username":[email_str.get()], "Password": [password_str.get()]}
    # Tabulate() creates pretty formatting

        # Write data to file
    with open("data.txt", "a+") as f:
        table = tabulate(user_df, tablefmt="plain")
        # If there's data, don't write the header
        f.seek(0)
        data = f.read(100)
        if len(data) > 0:
            f.write("\n")
            f.write(table)
        else:
            table = tabulate(user_df, headers=["Website", "Email/Username", "Password"])
            f.write(table)



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

email_entry = Entry(root, textvariable=email_str, width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "kenjameswinston@gmail.com")

password_entry = Entry(root, textvariable=password_str, width=21)
password_entry.grid(row=3, column=1)

# Buttons
# Generate password
generate_button = Button(root, text="Generate", bg=BACKGROUND_COLOR, width=11)
generate_button.grid(row=3, column=2)

# Add user data to text file
add_button = Button(root, text="Add", bg=BACKGROUND_COLOR, width=33, command=save_data)
add_button.grid(row=4, column=1, columnspan=2)


root.mainloop()
