import datetime
import subprocess
from typing import Union, List

# Day schedules
Monday: list = ['Example', 'Hello']
Tuesday: list = []
Wednesday: list = []
Thursday: list = ['World']
Friday: list = []
Saturday: list = []
Sunday: list = []

def check_if_empty(target_list: list, day_name: str) -> str:
    """Check if a list is empty and return formatted string."""
    if not target_list:
        return f"{day_name} - EMPTY".rjust(20)
    return f"{day_name} - {', '.join(map(str, target_list))}".rjust(20)

def generate_grid() -> str:
    """Generate a grid view of the week's schedule."""
    # Get today's date
    today = datetime.date.today()

    # Map weekday numbers to lists
    day_lists = {
        0: Monday,
        1: Tuesday,
        2: Wednesday,
        3: Thursday,
        4: Friday,
        5: Saturday,
        6: Sunday
    }

    # Map weekday numbers to names
    day_names = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    # Get current day's list and name
    current_day_list = day_lists.get(today.weekday(), [])
    current_day_name = day_names.get(today.weekday(), "Unknown")

    print('\nSelect - Week Lists:\n')
    selected_day = select_day()
    print(f"Selected day: {selected_day}")
    if selected_day == 'Monday':
        print(check_if_empty(day_lists[0], day_names[0]))
    elif selected_day == 'Tuesday':
        print(check_if_empty(day_lists[1], day_names[1]))
    elif selected_day == 'Wednesday':
        print(check_if_empty(day_lists[2], day_names[2]))
    elif selected_day == 'Thursday':
        print(check_if_empty(day_lists[3], day_names[3]))
    elif selected_day == 'Friday':
        print(check_if_empty(day_lists[4], day_names[4]))
    elif selected_day == 'Saturday':
        print(check_if_empty(day_lists[5], day_names[5]))
    elif selected_day == 'Sunday':
        print(check_if_empty(day_lists[6], day_names[6]))

    return current_day_name

def select_day() -> str:
    """Show day selection menu using gum."""
    result = subprocess.run(
        ["gum", "choose", "Monday", "Tuesday", "Wednesday",
         "Thursday", "Friday", "Saturday", "Sunday"],
        stdout=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()

if __name__ == "__main__":
    current_day = generate_grid()
