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

        # Show time
        self.time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
        self.time_label.pack(pady=20)

        # Show time sum
        self.summary_label = tk.Label(root, text="Time: 00:00:00", font=("Helvetica", 16))
        self.summary_label.pack(pady=20)

        # Start button
        self.start_button = tk.Button(root, text="Start", font=("Helvetica", 16), command=self.start_timer)
        self.start_button.pack(pady=10)

        # Stop button
        self.stop_button = tk.Button(root, text="Stop", font=("Helvetica", 16), command=self.stop_timer)
        self.stop_button.pack(pady=10)

        # Reset
        #self.reset_button = tk.Button(root, text="Reset", font=("Helvetica", 16), command=self.reset_timer)
        #self.reset_button.pack(pady=10)

        # Save sum button
        self.save_summary_button = tk.Button(root, text="Save time", font=("Helvetica", 16), command=self.save_summary)
        self.save_summary_button.pack(pady=10)

        # Load sum when turn on app
        self.load_summary()

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

    def stop_timer(self):
        if self.running:
            self.running = False
            self.save_time_to_file()

    #def reset_timer(self):
    #    self.stop_timer()
    #    self.counter = 0
    #    self.time_label.config(text="00:00:00")

    def update_timer(self):
        if self.running:
            self.counter += 1
            formatted_time = time.strftime('%H:%M:%S', time.gmtime(self.counter))
            self.time_label.config(text=formatted_time)
            self.root.after(1000, self.update_timer)

    def save_time_to_file(self):
        """Save time to csv"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total_time = time.strftime('%H:%M:%S', time.gmtime(self.counter))
        data = [current_time, total_time]
        file_name = "timer_logs.csv"

        # Save file to csv
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

        messagebox.showinfo("Save", f"time: {total_time}")

    def save_summary(self):
        """Save time from timer_logs.csv and save it to new file"""
        file_name = "timer_logs.csv"
        total_seconds = 0

        # Read data from file
        try:
            with open(file_name, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    # format HH:MM:SS
                    if len(row) > 1:
                        time_str = row[1]
                        h, m, s = map(int, time_str.split(':'))
                        total_seconds += h * 3600 + m * 60 + s
        except FileNotFoundError:
            messagebox.showerror("Error, no log file.")

        # time format
        total_time_formatted = time.strftime('%H:%M:%S', time.gmtime(total_seconds))

        # Save timw to new file
        summary_file = "time_summary.csv"
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(summary_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_date, total_time_formatted])

        messagebox.showinfo("Save", f"time: {total_time_formatted}")

        # Update time label
        self.summary_label.config(text=f"time: {total_time_formatted}")

    def load_summary(self):
        """Loadl last time sum time_summary.csv and update label"""
        summary_file = "time_summary.csv"
        try:
            with open(summary_file, mode='r') as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1].strip().split(',')
                    if len(last_line) > 1:
                        last_time = last_line[1].strip()
                        self.summary_label.config(text=f"time: {last_time}")
        except FileNotFoundError:
            self.summary_label.config(text="time: 00:00:00")

# App window
root = tk.Tk()
app = TimerApp(root)
root.mainloop()
