#!/home/ashley/Apps/todome-venv/bin/python3.13
import json, os, sys, time
from dataclasses import dataclass
from typing import List, Tuple
from datetime import date, datetime
from pathlib import Path
from libs.colorLib import *
from libs.tutorials import development_tutorial
from libs.securityLib import wait_for_enter
from libs.animationLib import *
from libs.weatherLib import get_weather
from libs.settings import load_location, load_time_format
from libs.timeLib import get_current_time
from plugins.week_list import generate_grid

# CONSTANT VARIABLES
TODO_FILE = Path.home() / '.todo.me'
username = os.environ.get('USER') or os.environ.get('USERNAME')
ending, checked, unchecked = "\033[0m", " - [x] ", " - [ ] "
time_format = load_time_format(os.getenv('USER', ''))


# TIME LOGIC
def clock(time_format: str) -> str:
	cache_bool = True if time_format == 'True' else False
	return get_current_time(switch=cache_bool)

current_clock: str = clock(time_format)

def update_time() -> str:
	global current_clock
	get_date = date.today()
	day = get_date.strftime("%d")
	month = get_date.strftime("%m")
	year = get_date.strftime("%Y")
	result = color_yellow_fg(day) + '/' + color_yellow_fg(month) + '/' + color_yellow_fg(year) + '		[' + color_red_fg(current_clock) + ']'
	return result

def get_weekday() -> str:
	today = datetime.now().strftime('%A')
	return f"'{color_magenta_bg(today)}'"


# SAVEFILE LOGIC
def load_todos() -> list:
	global username
	try:
		with open(TODO_FILE, 'r') as f:
			return json.load(f)
	except (FileNotFoundError, json.JSONDecodeError):
		return [(f'Welcome {color_yellow_fg(username)}, to TODOME', True), (f'''type t '<{color_yellow_fg("2")}>' to togle me on''', False), (f'''type r '<{color_yellow_fg("2")}>' to remove checkbox above⬆''', False)]

todos = load_todos()


@dataclass
class AnimationConfig:
    frames: List[Tuple[str, str]]
    delay: float = 0.01
    icon: str = "💾"
    spacing: str = "  "

def save_animation(config: AnimationConfig = None) -> None:
    """
    Display an animated saving indicator.

    Args:
        config: Optional AnimationConfig object for customization
    """
    if config is None:
        config = AnimationConfig(
            frames=[
                ('Saving', '.         |'),
                ('Saving', '..        |'),
                ('Saving', '...       |'),
                ('Saving', '....      |'),
                ('Saving', '.....     |'),
                ('Saving', '......    |'),
                ('Saving', '.......   |'),
                ('Saving', '........  |'),
                ('Saving', '......... |')
            ]
        )
    for text, dots in config.frames:
        clear_screen()
        save_msg = f"{config.spacing}{config.icon} {color_pink_fg(text)} {color_pink_fg(dots)}"
        print(save_msg)
        time.sleep(config.delay)
    clear_screen()

def save_todos() -> None:
	with open(TODO_FILE, 'w') as f:
		json.dump(todos, f, indent=2)
	clear_screen()
	print(welcome_screen(False))
	list_todos(True)

# CHECKBOX CLASS MODEL
class Checkbox:
	def __init__(self, number: int, title: str) -> None:
		self.number = number
		self.title = title

	def fg(self, text: str, color: int) -> str:
		return f"\033[38;5;{color}m{text}{ending}"

	def bg(self, text: str, color: int) -> str:
		return f"\033[48;5;{color}m{text}{ending}"

	def unchecked(self) -> None:
		number = self.fg(f"{self.number:2d}. ", 245)
		chunk_0 = self.fg(" - ", 231)
		chunk_1 = self.fg("[", 197)
		chunk_2 = self.fg(" ", 197)
		chunk_3 = self.fg("] ", 197)
		result = f"{number}{chunk_0}{chunk_1}{chunk_2}{chunk_3}{self.title}{ending}"
		print(result)

	def checked(self) -> None:
		number = self.fg(f"{self.number:2d}. ", 245)
		chunk_0 = self.fg(" - ", 231)
		chunk_1 = self.fg("[", 48)
		chunk_2 = self.bg("x", 48)
		chunk_3 = self.fg("] ", 48)
		result = f"{number}{chunk_0}{chunk_1}{chunk_2}{chunk_3}{self.title}{ending}"
		print(result)

# COMMAND LOGIC
def add_Todo() -> None:
	global todos
	new_todo = (input(f'{color_magenta_bg("Title:")} '), False)
	todos.append(new_todo)
	clear_screen()
	print(welcome_screen(False))
	list_todos(True)
def list_todos(verbose: bool):
	print(f"\n{color_pink_fg('Current')}{color_green_fg('-')}{color_green_fg('TODOs')}:                   {get_weekday()}")
	for i, (title, is_checked) in enumerate(todos, 1):
		todo = Checkbox(i, title)
		if is_checked:  # Fix: Indent these lines to be inside the loop
			todo.checked()
		else:
			todo.unchecked()
	completed = sum(1 for _, is_checked in todos if is_checked)
	total = len(todos)
	if verbose == True:
		print(f"\nGOALS FINISHED: {color_red_fg(completed)}/{color_green_fg(total)} TODAY! {update_time()}")
def toggle_todo(num: int) -> None:
	global todos
	if 1 <= num <= len(todos):
		title, is_checked = todos[num-1]
		todos[num-1] = (title, not is_checked)
		list_todos(True)
		save_todos()
	else:
		print(f"Error: No todo with number {color_red_fg(num)}")
def remove_todo(num: int) -> None:
	global todos
	if 1 <= num <= len(todos):
		removed = todos.pop(num-1)
		print(f"Removed: {removed[0]}")
		list_todos(True)
		save_todos()
	else:
		print(f"Error: No todo with number {color_red_fg(num)}")
def comando_check(cmd: str) -> None:
	global username
	cmd = cmd.lower().strip()
	# Handle toggle command (e.g., "toggle 1" or "t 1")
	if cmd.startswith(('toggle ', 't ')):
		try:
			num = int(cmd.split()[1])
			toggle_todo(num)
			return
		except (IndexError, ValueError):
			print(f"Usage: toggle <number> or {color_magenta_fg('t')} <{color_green_fg('number')}>")
			return
	# Handle remove command (e.g., "remove 1" or "r 1")
	if cmd.startswith(('remove ', 'r ')):
		try:
			num = int(cmd.split()[1])
			remove_todo(num)
			return
		except (IndexError, ValueError):
			print(f"Usage: remove <number> or {color_magenta_fg('r')} <{color_green_fg('number')}>")
			return
	# Handle other commands
	if cmd == 'list' or cmd == 'l':
		print(welcome_screen(False))
		list_todos(True)
	elif cmd == 'add' or cmd == 'a':
		add_Todo()
	elif cmd == 'week' or cmd == 'w':
		#generate_grid()
		os.system(f'/home/{username}/.config/todome/alpha')
		print(welcome_screen(False))
		list_todos(True)
	elif cmd == 'save' or cmd == 's':
		save_animation()
		save_todos()
	elif cmd == 'dev-manual' or cmd == 'dev':
		clear_screen()
		development_tutorial()
		print(welcome_screen(True))
		list_todos(True)
	elif cmd == 'help' or cmd == 'h':
		clear_screen(), print(welcome_screen(False)), list_todos(False)
		print(f"\n{color_magenta_bg('Available commands:')}\n")
		print(f"{color_yellow_fg('list')} (l)    {color_green_fg('-')} Show all todos")
		print(f"{color_yellow_fg('week')} (w)    {color_green_fg('-')} Show all weekend todos {color_darkgreen_bg('PLUGIN')}")
		print(f"{color_yellow_fg('add')} (a)     {color_green_fg('-')} Add a new todo")
		print(f"{color_yellow_fg('toggle')} <n>  {color_green_fg('-')} Toggle todo status (t <n>)")
		print(f"{color_yellow_fg('remove')} <n>  {color_green_fg('-')} Remove todo (r <n>)")
		print(f"{color_yellow_fg('save')} (s)    {color_green_fg('-')} Save todos")
		print(f"{color_yellow_fg('help')} (h)    {color_green_fg('-')} Show this help message")
		print(f"{color_yellow_fg('exit')} (q)    {color_green_fg('-')} Exit the program")
		print(f"{color_yellow_fg('dev')}         {color_green_fg('-')} Teaches you how to modify this program")
		print(f"\nsavefile is located in {TODO_FILE}")
	elif cmd in ['exit', 'quit', 'q']:
		print(welcome_screen(False)), list_todos(True)
		print(f"Goodbye! {color_green_fg(username.upper())} 👾")
		sys.exit(0)
	else:
		print(f"Unknown command: '{cmd}'. Type '{color_yellow_fg('help')}' for available commands.")

# MAIN FUNCTION
def main():
	print(welcome_screen(True))
	list_todos(True)
	while True:
		try:
			cmd = input('\n> ')
			clear_screen()
			comando_check(cmd)
		except KeyboardInterrupt:
			print("\nSaving and exiting...")
			save_todos()
			break
		except Exception as e:
			print(f"Error: {e}")

if __name__ == '__main__':
	main()
