import curses
import sqlite3
from datetime import datetime
import sys, re, os

username = os.environ.get('USER') or os.environ.get('USERNAME')

class TodoManager:
    def __init__(self, db_path=f"/home/{username}/.todos.db"):
        self.db_path = db_path
        self.setup_database()
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.current_day_index = datetime.now().weekday()
        self.current_pos = 0
        self.todos = []

    def setup_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY,
                    day TEXT NOT NULL,
                    task TEXT NOT NULL,
                    time_value TEXT,
                    completed INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def extract_time_value(self, task):
        time_match = re.match(r'^(\d{1,2}:\d{2})', task)
        if time_match:
            time_str = time_match.group(1)
            if len(time_str.split(':')[0]) == 1:
                time_str = f"0{time_str}"
            return time_str
        return "99:99"

    def get_todos(self, day):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT id, task, completed, time_value
                   FROM todos
                   WHERE day = ?
                   ORDER BY time_value, created_at""",
                (day,)
            )
            return cursor.fetchall()

    def add_todo(self, day, task):
        time_value = self.extract_time_value(task)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO todos (day, task, time_value) VALUES (?, ?, ?)",
                (day, task, time_value)
            )
            conn.commit()

    def delete_todo(self, todo_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            conn.commit()

    def toggle_todo(self, todo_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """UPDATE todos
                   SET completed = CASE WHEN completed = 0 THEN 1 ELSE 0 END
                   WHERE id = ?""",
                (todo_id,)
            )
            conn.commit()

    def draw_vertical_lines(self, stdscr, height, width):
        section_width = width // 7
        for i in range(1, 7):
            x = i * section_width
            for y in range(0, 2):
                stdscr.addch(y, x-1, '│')

    def get_up_next(self):
        """Get the first incomplete task for the current day, sorted by time."""
        incomplete_tasks = [task for _, task, completed, time_value in self.todos if not completed]
        if incomplete_tasks:
            # Sort by time_value (already sorted in self.todos)
            return incomplete_tasks[0]
        return "No upcoming tasks"

    def run(self, stdscr):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            section_width = width // 7

            # Display days with centered text
            for i, day in enumerate(self.days):
                x = i * section_width
                day_text = day[:section_width-2]
                padding = (section_width - len(day_text) - 1) // 2
                attr = curses.color_pair(1) if i == self.current_day_index else curses.A_NORMAL
                stdscr.addstr(0, x + padding, day_text, attr)

            # Draw vertical lines
            self.draw_vertical_lines(stdscr, height, width)

            # Draw horizontal line under the header
            stdscr.addstr(1, 0, "─" * (width-1))

            # Get and display todos for current day
            self.todos = self.get_todos(self.days[self.current_day_index])
            for i, (todo_id, task, completed, time_value) in enumerate(self.todos):
                if i + 2 >= height - 3:  # Adjusted to leave space for bottom status and "Up Next"
                    break
                prefix = "[x]" if completed else "[ ]"
                attr = curses.color_pair(2) if i == self.current_pos else curses.A_NORMAL
                if i == self.current_pos:
                    stdscr.addstr(i + 2, 0, f"> {prefix} {task}", attr)
                else:
                    stdscr.addstr(i + 2, 0, f"  {prefix} {task}", attr)

            # Display "Up Next" window
            up_next_task = self.get_up_next()
            up_next_text = f"Up Next: {up_next_task}"
            stdscr.addstr(height-3, 0, up_next_text, curses.color_pair(3))

            # Display help text and current day at bottom
            help_text = "a: Add | space: Toggle | DEL: Delete | ←→: Change day | ↑↓: Navigate | q: Quit"
            current_day_text = f"Current day: {self.days[self.current_day_index]}"

            # Calculate positions for bottom status line
            help_pos = 0
            day_pos = width - len(current_day_text) - 1

            # Display bottom status line
            stdscr.addstr(height-1, help_pos, help_text, curses.color_pair(3))
            stdscr.addstr(height-1, day_pos, current_day_text, curses.color_pair(3))

            stdscr.refresh()
            key = stdscr.getch()

            if key == ord('q'):
                break
            elif key == ord('a'):
                curses.echo()
                curses.curs_set(1)
                stdscr.addstr(height-2, 0, "Enter todo: ")
                stdscr.clrtoeol()
                task = stdscr.getstr(height-2, 11).decode('utf-8')
                if task:
                    self.add_todo(self.days[self.current_day_index], task)
                curses.noecho()
                curses.curs_set(0)
            elif key == ord(' '):
                if self.todos:
                    self.toggle_todo(self.todos[self.current_pos][0])
            elif key in (curses.KEY_DC, ord('\x7f'), ord('\x08')):  # Delete, Backspace keys
                if self.todos:
                    self.delete_todo(self.todos[self.current_pos][0])
                    if self.current_pos >= len(self.todos) - 1:
                        self.current_pos = max(0, len(self.todos) - 2)
            elif key == curses.KEY_LEFT:
                self.current_day_index = (self.current_day_index - 1) % 7
                self.current_pos = 0
            elif key == curses.KEY_RIGHT:
                self.current_day_index = (self.current_day_index + 1) % 7
                self.current_pos = 0
            elif key == curses.KEY_UP:
                self.current_pos = max(0, self.current_pos - 1)
            elif key == curses.KEY_DOWN:
                self.current_pos = min(len(self.todos) - 1, self.current_pos + 1)

def main():
    todo_manager = TodoManager()
    curses.wrapper(todo_manager.run)

if __name__ == "__main__":
    main()
