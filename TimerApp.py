import tkinter as tk
from tkinter import messagebox
import time
import csv
from datetime import datetime

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Timer")
        self.running = False
        self.counter = 0

        # Wyświetlanie czasu
        self.time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
        self.time_label.pack(pady=20)

        # Wyświetlanie sumy czasu
        self.summary_label = tk.Label(root, text="Suma czasu: 00:00:00", font=("Helvetica", 16))
        self.summary_label.pack(pady=20)

        # Przycisk start
        self.start_button = tk.Button(root, text="Start", font=("Helvetica", 16), command=self.start_timer)
        self.start_button.pack(pady=10)

        # Przycisk stop
        self.stop_button = tk.Button(root, text="Stop", font=("Helvetica", 16), command=self.stop_timer)
        self.stop_button.pack(pady=10)

        # Resetowanie
        self.reset_button = tk.Button(root, text="Reset", font=("Helvetica", 16), command=self.reset_timer)
        self.reset_button.pack(pady=10)

        # Przycisk do zapisania sumy
        self.save_summary_button = tk.Button(root, text="Zapisz sumę czasu", font=("Helvetica", 16), command=self.save_summary)
        self.save_summary_button.pack(pady=10)

        # Ładowanie sumy czasu przy starcie
        self.load_summary()

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

    def stop_timer(self):
        if self.running:
            self.running = False
            self.save_time_to_file()

    def reset_timer(self):
        self.stop_timer()
        self.counter = 0
        self.time_label.config(text="00:00:00")

    def update_timer(self):
        if self.running:
            self.counter += 1
            formatted_time = time.strftime('%H:%M:%S', time.gmtime(self.counter))
            self.time_label.config(text=formatted_time)
            self.root.after(1000, self.update_timer)

    def save_time_to_file(self):
        """Zapisuje czas sesji do pliku CSV"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total_time = time.strftime('%H:%M:%S', time.gmtime(self.counter))
        data = [current_time, total_time]
        file_name = "timer_logs.csv"

        # Zapis do pliku CSV
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

        messagebox.showinfo("Zapisano", f"Czas zapisany: {total_time}")

    def save_summary(self):
        """Sumuje całkowity czas z pliku timer_logs.csv i zapisuje do nowego pliku"""
        file_name = "timer_logs.csv"
        total_seconds = 0

        # Odczyt danych z pliku
        try:
            with open(file_name, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    # Zakładamy, że drugi element w wierszu to czas w formacie HH:MM:SS
                    if len(row) > 1:
                        time_str = row[1]
                        h, m, s = map(int, time_str.split(':'))
                        total_seconds += h * 3600 + m * 60 + s
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Nie znaleziono pliku z logami.")

        # Formatowanie całkowitego czasu
        total_time_formatted = time.strftime('%H:%M:%S', time.gmtime(total_seconds))

        # Zapis całkowitego czasu do nowego pliku
        summary_file = "time_summary.csv"
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(summary_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_date, total_time_formatted])

        messagebox.showinfo("Zapisano", f"Suma czasu: {total_time_formatted}")

        # Aktualizacja etykiety z sumą czasu
        self.summary_label.config(text=f"Suma czasu: {total_time_formatted}")

    def load_summary(self):
        """Ładuje ostatnią sumę czasu z pliku time_summary.csv i aktualizuje etykietę"""
        summary_file = "time_summary.csv"
        try:
            with open(summary_file, mode='r') as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1].strip().split(',')
                    if len(last_line) > 1:
                        last_time = last_line[1].strip()
                        self.summary_label.config(text=f"Suma czasu: {last_time}")
        except FileNotFoundError:
            self.summary_label.config(text="Suma czasu: 00:00:00")

# Tworzenie okna aplikacji
root = tk.Tk()
app = TimerApp(root)
root.mainloop()
