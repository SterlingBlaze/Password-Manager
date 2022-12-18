import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(6, 8)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

# ------------- List Comprehension---------- #
    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list2 = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list3 = [random.choice(symbols) for _ in range(nr_symbols)]

    new_password = password_list + password_list2 + password_list3
    random.shuffle(new_password)
    password = "".join(new_password)  # -------------> joining strings in list together.

    password_entry.insert(0, password)
    pyperclip.copy(password)

# ------------------------ find password ----------------------------------------#
def find_password():
    # Get website data
    web = website.get().capitalize()
    if web == "":
        messagebox.showinfo(message=f"Are you in the right mind?")
    try:
        with open('Files/data.json', 'r') as data_file:
            data = json.load(data_file)
        #catch exception and prompt user to save files first----------------------------------------
    except FileNotFoundError:
        messagebox.showinfo(title="error!", message="DataFile is missing. Please save your credentials first.")
    else:
        if web in data:
            ques = messagebox.askquestion('Existing Website', 'Data found.')
            if ques == 'yes':
                user = data[web]["email"]
                passw = data[web]["pass"]
                messagebox.showinfo(title="Exists", message=f'{user}\n{passw}')
        else:
            messagebox.showinfo(title="Oops!", message="Data does not exist.")
    finally:
        website.delete(0, END)
        password_entry.delete(0, END)

# --------------------------------- CLEAR ALL ENTRIES--------------------------- #
def clear():
    password_entry.delete(0, END)
    email.delete(0, END)
    website.delete(0, END)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = website.get().capitalize()
    username = email.get()
    password = password_entry.get()
    new_data = {web: {
        "email": username,
        "pass": password}
    }
    # check empty fields
    if len(web) == 0 or len(password) == 0 or len(username) == 0:
        messagebox.showinfo(title="Ooops!", message="Empty fields")
        # check password length
    elif len(password) < 8:
        messagebox.showinfo(title="Ooops!", message="Too short.")
        # if website exists
    else:
        try:  # Try Opening data.json file
            with open('Files/data.json', 'r') as data_file:
                data = json.load(data_file)
                    # if file does not exist.
        except FileNotFoundError:
            with open('Files/data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open('Files/data.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website.delete(0, END)
            password_entry.delete(0, END)
        # else:
        # messagebox.showinfo('Return', 'Successfully added.')

# ----------------------------------- SHOW PASSWORD --------------------------#
def show_password():
    password_entry.configure(show='')
    checkbox.configure(command=hide, text='Hide')

# ---------------------------------- HIDE PASSWORD ---------------------------#
def hide():
    password_entry.configure(show='*')
    checkbox.configure(command=show_password, text='Show')

# -------------------------------cancel-------------------------------------#
def close_window():
    res = messagebox.askquestion('Exit Application', 'Do you really want to exit')
    if res == 'yes':
        window.destroy()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Python Password Manager")
window.config(padx=50, pady=20)
mypass_logo = PhotoImage(file="logo.png")
window_canvas = Canvas(width=200, height=200)
window_canvas.create_image(100, 100, image=mypass_logo)
window_canvas.grid(column=1, row=0)

# labels
Web_label = Label(text="Website:")
Web_label.grid(column=0, row=1)
username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)
pass_label = Label(text="Password:")
pass_label.grid(row=3, column=0)

# entry widgets
website = Entry(width=50)
website.focus()
website.grid(column=1, row=1, columnspan=2, sticky="W")
email = Entry(width=50)
email.grid(column=1, row=2, columnspan=2, sticky="W")
email.insert(END, "aqdasahmadis34@gmail.com")
password_entry = Entry(width=39, show="*")
password_entry.grid(row=3, column=1, sticky="W")

# buttons
generate_pass = Button(text="Generate", width=10, command=generate)
generate_pass.grid(column=3, row=3)
add_pass = Button(text="Add", width=43, command=save)
add_pass.grid(row=4, column=1, columnspan=2)
clear_all = Button(text="Clear all", width=10, command=clear)
clear_all.grid(column=3, row=4)
search = Button(text="Search", width=10, command=find_password)
search.grid(column=3, row=1)
cancel = Button(text="Cancel", width=10, command=close_window)
cancel.grid(column=3, row=5)

# checkbox show box
checkbox = Checkbutton(text="Show", command=show_password)
checkbox.grid(column=2, row=3)
window.mainloop()

