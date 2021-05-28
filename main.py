import csv
import tkinter as tk, tkinter.messagebox as messagebox
from gen_pass import generate_pass
import os

def setup_window(window: tk.Tk) -> None:       
    window.minsize(800, 600)
    window.title("Password manager")
    window.config(padx=160, pady=100, bg="black")
    photo = tk.PhotoImage(file="logo.png")
    window.iconphoto(False, photo)

def clear() -> None:
    password.delete(0, tk.END) 
    website.delete(0, tk.END) 

def write_data(website: str, email: str, password: str) -> None:
    if not len(website) or not len(email) or not len(password):
        messagebox.showinfo("Warning", "Please fill out every field!")
        return
    user_choice = messagebox.askyesno(title="Confirmation", message=f"You sure you want to submit this data?\nWebsite: {website}\nEmail: {email}\nPassword: {password}")
    if user_choice:
        with open("./text.csv", "a") as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerow([website, email, password])
        messagebox.showinfo(title="Result", message="Data has been written to the file!")
        window.clipboard_clear()
        window.clipboard_append(password)
        window.update(
        clear()

def get_most_used_email() -> str:
    with open("text.csv", "r+") as file:
        reader = csv.DictReader(file, delimiter='|')
        emails: [str] = [i["email"] for i in reader]
    if len(emails):
        return max(emails, key=lambda email: emails.count(email))
    return ""

def auto_pass() -> None:
    p: str = generate_pass()
    if len(password.get()):
        password.delete(0, tk.END)
    password.insert(0, p) 
    messagebox.showinfo("New password", message=f"Generated a new random password: {p}")

if __name__ == "__main__":
    window = tk.Tk()
    setup_window(window)
    if not os.path.exists(os.path.join(os.getcwd(), "text.csv")):
        with open("text.csv", "a") as f:
            f.write("website|email|password\n")
    most_used_email = get_most_used_email()

    # Widgets
    image = tk.PhotoImage(master=window, file="logo.png")
    canvas = tk.Canvas(master=window, width=image.width(), height=image.height())
    canvas.config(bg="orange", highlightthickness=0)
    canvas.create_image(100, 110, image = image)
    password_gui = tk.Label(master=window, text="Password")
    email_username_gui = tk.Label(master=window, text="Email/Username")
    website_gui = tk.Label(master=window, text="Website")
    password_gui.config(bg="orange", highlightthickness=0)
    email_username_gui.config(bg="orange", highlightthickness=0)
    website_gui.config(bg="orange", highlightthickness=0)

    # Input stuff 
    password = tk.Entry(master=window, text="Password", width=30)
    website = tk.Entry(master=window, text="Website", width=30) 
    email_username= tk.Entry(master=window, text="Email/username", width=30)
    email_username.insert(tk.END, most_used_email)

    # Buttons
    gen_pass_btn = tk.Button(master=window, text="Generate Password", command = auto_pass)
    add_btn = tk.Button(master=window, width=20, height=1, command=lambda: write_data(website.get(), email_username.get(), password.get()), text="Add")

    # Layout widgets
    canvas.place(x=40, y=30)
    canvas.grid(column=1, row=0)
    password.grid(column=1, row=3, sticky="EW")
    email_username.grid(column=1, row=2, columnspan=2, sticky="EW")
    website.grid(column=1, row=1, columnspan=2, sticky="EW")
    website.focus()

    # Layout buttons
    add_btn.grid(column=1, row=4, columnspan=2)
    gen_pass_btn.grid(column=3, row=3)

    # Layout GUI
    website_gui.grid(column=0, row=1)
    email_username_gui.grid(row=2, column=0)
    password_gui.grid(row=3, column=0)

    # Main loop
    window.mainloop()
