import tkinter as tk, tkinter.messagebox as messagebox
from gen_pass import generate_pass
import os
import json

def setup_window(window: tk.Tk) -> None:       
    window.minsize(800, 600)
    window.title("Password manager")
    window.config(padx=160, pady=100, bg="black")
    photo = tk.PhotoImage(file="logo.png")
    window.iconphoto(False, photo)

def find_data(website: str) -> dict:
    if not len(website):
        messagebox.showinfo(title="Missing website", message="Please enter a website")
        return
    with open("text.json", "r") as file:
        try:
            data: dict = json.load(file)
            for i, k in data.items():
                if i.lower() == website.lower():
                    password, email = k.get("password"), k.get("email")
                    messagebox.showinfo(title="Data found", message=f"Website: {website}\nEmail: {email}\nPassword: {password}")
                    window.clipboard_clear()
                    window.clipboard_append(password)
                    window.update()
                    return
            messagebox.showinfo(title="Data not found", message=f"Could not find data for website: {website}")
        except Exception:
            messagebox.showinfo(title="Data not found", message=f"Could not find data for website: {website}")
            return 

def clear() -> None:
    password.delete(0, tk.END) 
    website.delete(0, tk.END) 

def write_data(website: str, email: str, password: str) -> None:
    if not len(website) or not len(email) or not len(password):
        messagebox.showinfo("Warning", "Please fill out every field!")
        return
    user_choice: bool = messagebox.askyesno(title="Confirmation", message=f"You sure you want to submit this data?\nWebsite: {website}\nEmail: {email}\nPassword: {password}")
    data_to_write = {website: {"email": email, "password": password}}
    if user_choice:
        with open("text.json", "r") as file:
            try:
                data: dict = json.load(file)
                data.update(data_to_write)
            except Exception:
                data = data_to_write
        with open("text.json", "w") as file_write:
            json.dump(data, file_write)
        messagebox.showinfo(title="Result", message="Data has been written to the file!")
        window.clipboard_clear()
        window.clipboard_append(password)
        window.update()
        clear()

def get_most_used_email() -> str:
    with open("text.json", "r") as file:
        try:
            data: dict = json.load(file)
            stats = [k['email'] for _, k in data.items()]
            return max(stats, key=lambda x: stats.count(x))
        except Exception:
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
    if not os.path.exists(os.path.join(os.getcwd(), "text.json")):
        open("text.json", "w").close()
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
    add_btn = tk.Button(master=window, width=10, height=1, command=lambda: write_data(website.get(), email_username.get(), password.get()), text="Add")
    search_btn = tk.Button(master=window, width=10, text="Search", command=lambda: find_data(website.get()))

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
    search_btn.grid(column=3, row=1)

    # Layout GUI
    website_gui.grid(column=0, row=1)
    email_username_gui.grid(row=2, column=0)
    password_gui.grid(row=3, column=0)

    # Main loop
    window.mainloop()
