class PomodoroTimer:
    """Manages the logic of the Pomodoro timer."""
    def __init__(self, work_min=25, short_break_min=5, long_break_min=15):
        self.work_min = work_min
        self.short_break_min = short_break_min
        self.long_break_min = long_break_min

        self.reps = 0
        self.timer = None
        self.is_running = False

    def get_current_state(self):
        """Returns the current state (Work, Short Break, Long Break)."""
        self.reps += 1
        if self.reps % 8 == 0:
            return "Long Break", self.long_break_min * 60
        elif self.reps % 2 == 0:
            return "Short Break", self.short_break_min * 60
        else:
            return "Work", self.work_min * 60

    def reset(self):
        """Resets the timer and session count."""
        self.reps = 0
        self.is_running = False