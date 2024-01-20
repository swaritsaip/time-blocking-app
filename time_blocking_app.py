import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class TimeBlockingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Blocking App")

        self.activities = []
        self.total_time_left = tk.StringVar()
        self.total_time_left.set("")

        self.is_24_hour_format = tk.BooleanVar()
        self.is_24_hour_format.set(False)

        self.create_widgets()

    def create_widgets(self):
        activity_frame = ttk.Frame(self.root, padding="10")
        activity_frame.pack(expand=True, fill="both")

        ttk.Label(activity_frame, text="Select Start Time:").grid(row=0, column=0, padx=5, pady=5)
        self.start_hour_combo = ttk.Combobox(activity_frame, values=self.get_hour_values())
        self.start_hour_combo.set(self.get_default_hour_value())
        self.start_hour_combo.grid(row=0, column=1, padx=5, pady=5)

        self.start_minute_combo = ttk.Combobox(activity_frame, values=[f"{i:02d}" for i in range(1, 60)])
        self.start_minute_combo.set("01")
        self.start_minute_combo.grid(row=0, column=2, padx=5, pady=5)

        if not self.is_24_hour_format.get():
            self.start_am_pm_combo = ttk.Combobox(activity_frame, values=["AM", "PM"], state="readonly")
            self.start_am_pm_combo.set("AM")
            self.start_am_pm_combo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(activity_frame, text="Select End Time:").grid(row=1, column=0, padx=5, pady=5)
        self.end_hour_combo = ttk.Combobox(activity_frame, values=self.get_hour_values())
        self.end_hour_combo.set(self.get_default_hour_value())
        self.end_hour_combo.grid(row=1, column=1, padx=5, pady=5)

        self.end_minute_combo = ttk.Combobox(activity_frame, values=[f"{i:02d}" for i in range(1, 60)])
        self.end_minute_combo.set("01")
        self.end_minute_combo.grid(row=1, column=2, padx=5, pady=5)

        if not self.is_24_hour_format.get():
            self.end_am_pm_combo = ttk.Combobox(activity_frame, values=["AM", "PM"], state="readonly")
            self.end_am_pm_combo.set("AM")
            self.end_am_pm_combo.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(activity_frame, text="Enter Activity Description:").grid(row=2, column=0, padx=5, pady=5)
        self.activity_description_entry = ttk.Entry(activity_frame)
        self.activity_description_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

        ttk.Button(activity_frame, text="Add Activity", command=self.add_activity).grid(row=3, column=1, columnspan=3, pady=(5, 0))

        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.pack(expand=True, fill="both")

        self.activities_listbox = tk.Listbox(list_frame, height=10, selectmode=tk.SINGLE)
        self.activities_listbox.pack(expand=True, fill="both")
        self.activities_listbox.bind("<ButtonRelease-1>", self.handle_activity_click)

        ttk.Button(list_frame, text="Remove Selected", command=self.remove_activity).pack(pady=(50, 5))

        total_time_frame = ttk.Frame(self.root, padding="10")
        total_time_frame.pack(expand=True, fill="both")

        ttk.Label(total_time_frame, text="Total Time Left in the Day:").pack()
        ttk.Label(total_time_frame, textvariable=self.total_time_left).pack()

        clock_frame = ttk.Frame(self.root, padding="10")
        clock_frame.pack(expand=True, fill="both")

        self.clock_label = ttk.Label(clock_frame, text="", font=("Helvetica", 20))
        self.clock_label.pack(expand=True)

        ttk.Checkbutton(clock_frame, text="24-Hour Format", variable=self.is_24_hour_format, command=self.update_hour_format).pack(pady=10)

        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def add_activity(self):
        start_hour = int(self.start_hour_combo.get())
        start_minute = int(self.start_minute_combo.get())

        end_hour = int(self.end_hour_combo.get())
        end_minute = int(self.end_minute_combo.get())

        activity_description = self.activity_description_entry.get()

        if activity_description:
            start_time = f"{start_hour:02d}:{start_minute:02d}"
            end_time = f"{end_hour:02d}:{end_minute:02d}"

            if not self.is_24_hour_format.get():
                start_time += f" {self.start_am_pm_combo.get()}"
                end_time += f" {self.end_am_pm_combo.get()}"

            activity_time = f"{start_time} to {end_time}"
            self.activities.append((activity_time, activity_description))
            self.activities_listbox.insert(tk.END, f"{activity_time} - {activity_description} ({self.calculate_duration(start_time, end_time)})")

            self.activity_description_entry.delete(0, tk.END)

            self.start_hour_combo.set(self.get_default_hour_value())
            self.start_minute_combo.set("01")
            if not self.is_24_hour_format.get():
                self.start_am_pm_combo.set("AM")

            self.end_hour_combo.set(self.get_default_hour_value())
            self.end_minute_combo.set("01")
            if not self.is_24_hour_format.get():
                self.end_am_pm_combo.set("AM")

            total_time_left = self.calculate_total_time_left()
            self.total_time_left.set(total_time_left)

    def remove_activity(self):
        selected_index = self.activities_listbox.curselection()
        if selected_index:
            self.activities_listbox.delete(selected_index)
            self.activities.pop(selected_index[0])

            total_time_left = self.calculate_total_time_left()
            self.total_time_left.set(total_time_left)

    def handle_activity_click(self, event):
        clicked_item = self.activities_listbox.nearest(event.y)
        self.activities_listbox.selection_clear(0, tk.END)
        self.activities_listbox.selection_set(clicked_item)

    def update_hour_format(self):
        self.start_hour_combo["values"] = self.get_hour_values()
        self.end_hour_combo["values"] = self.get_hour_values()

        if not self.is_24_hour_format.get():
            self.start_am_pm_combo.grid(row=0, column=3, padx=5, pady=5)
            self.end_am_pm_combo.grid(row=1, column=3, padx=5, pady=5)
        else:
            self.start_am_pm_combo.grid_forget()
            self.end_am_pm_combo.grid_forget()

        self.start_hour_combo.set(self.get_default_hour_value())
        self.end_hour_combo.set(self.get_default_hour_value())

    def get_hour_values(self):
        return [f"{i:02d}" for i in range(1, 13)] if not self.is_24_hour_format.get() else [f"{i:02d}" for i in range(0, 24)]

    def get_default_hour_value(self):
        return "01" if not self.is_24_hour_format.get() else "00"

    def calculate_duration(self, start_time, end_time):
        start_datetime = datetime.strptime(start_time, "%I:%M %p") if not self.is_24_hour_format.get() else datetime.strptime(start_time, "%H:%M")
        end_datetime = datetime.strptime(end_time, "%I:%M %p") if not self.is_24_hour_format.get() else datetime.strptime(end_time, "%H:%M")
        duration = end_datetime - start_datetime
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = remainder // 60
        return f"{hours}h {minutes}m"

    def calculate_total_time_left(self):
        total_time_left = timedelta(hours=24)

        for activity_time, _ in self.activities:
            start_time, end_time = activity_time.split(" to ")
            start_datetime = datetime.strptime(start_time, "%I:%M %p") if not self.is_24_hour_format.get() else datetime.strptime(start_time, "%H:%M")
            end_datetime = datetime.strptime(end_time, "%I:%M %p") if not self.is_24_hour_format.get() else datetime.strptime(end_time, "%H:%M")

            total_time_left -= end_datetime - start_datetime

        return str(total_time_left)

    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

def main():
    root = tk.Tk()
    app = TimeBlockingApp(root)
    root.geometry("800x600")
    root.resizable(False, False)
    root.after(1000, app.update_clock)
    root.mainloop()

if __name__ == "__main__":
    main()
