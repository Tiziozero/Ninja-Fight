import tkinter as tk
import client_con as cn

def update_string(n):
    new_string = n.recv_data()
    if new_string is not None:
        label.config(text=new_string)
    # Schedule this function to be called again after 100 milliseconds
    root.after(100, update_string, n)

def on_closing():
    if n:
        n.close()
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("String Update App")
root.geometry("300x200")

# Create a Label widget to display the string
label = tk.Label(root, text="Initial String", font=("Arial", 16))
label.pack(pady=20)

# Setup network
n = cn.Network('localhost', 48878)
n.run()
print("Setup network")

# Start the update cycle
update_string(n)

# Bind the closing function to the window's close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI event loop
root.mainloop()

