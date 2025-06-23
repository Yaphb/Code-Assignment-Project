import json
import os
from datetime import datetime

class AppEntity:
    """A base class for application data entities to demonstrate inheritance."""
    def to_dict(self):
        raise NotImplementedError("Subclasses must implement this method.")

class Reminder(AppEntity):
    """Represents a single reminder."""
    def __init__(self, message, time_str):
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Reminder message cannot be empty.")
        try:
            # We expect time in 'YYYY-MM-DD HH:MM' format
            self.time = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ValueError("Invalid time format. Use YYYY-MM-DD HH:MM.")
        self.message = message

    def to_dict(self):
        """Converts the Reminder object to a dictionary for JSON serialization."""
        return {
            "message": self.message,
            "time": self.time.strftime('%Y-%m-%d %H:%M')
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Reminder object from a dictionary."""
        return cls(data['message'], data['time'])

class ReminderManager:
    """Manages all reminders, including loading and saving."""
    def __init__(self, data_file='data/reminders.json'):
        self.reminders = []
        self.data_file = data_file
        self._ensure_data_dir_exists()
        self.load_reminders()

    def _ensure_data_dir_exists(self):
        dir_name = os.path.dirname(self.data_file)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

    def add_reminder(self, reminder):
        self.reminders.append(reminder)
        self.reminders.sort(key=lambda r: r.time) # Keep reminders sorted
        self.save_reminders()

    def delete_reminder(self, reminder_to_delete):
        self.reminders = [r for r in self.reminders if r is not reminder_to_delete]
        self.save_reminders()

    def load_reminders(self):
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.reminders = [Reminder.from_dict(item) for item in data]
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading reminders: {e}")
            self.reminders = []

    def save_reminders(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump([r.to_dict() for r in self.reminders], f, indent=4)
        except IOError as e:
            print(f"Error saving reminders: {e}")