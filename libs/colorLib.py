
# CLI RENDERING
def color_pink_fg(text: str) -> str:
	return f"\033[38;5;205m{text}\033[0m"
def color_pink_bg(text: str) -> str:
	return f"\033[48;5;199m{text}\033[0m"
def color_green_fg(text: str) -> str:
	return f"\033[38;5;82m{text}\033[0m"
def color_green_bg(text: str) -> str:
	return f"\033[48;5;82m{text}\033[0m"
def color_darkgreen_fg(text: str) -> str:
	return f"\033[38;5;34m{text}\033[0m"
def color_darkgreen_bg(text: str) -> str:
	return f"\033[48;5;34m{text}\033[0m"
def color_red_fg(text: str) -> str:
	return f"\033[38;5;196m{text}\033[0m"
def color_red_bg(text: str) -> str:
	return f"\033[48;5;196m{text}\033[0m"
def color_yellow_fg(text: str) -> str:
	return f"\033[38;5;226m{text}\033[0m"
def color_yellow_bg(text: str) -> str:
	return f"\033[48;5;226m{text}\033[0m"
def color_magenta_fg(text: str) -> str:
	return f"\033[38;5;92m{text}\033[0m"
def color_magenta_bg(text: str) -> str:
	return f"\033[48;5;92m{text}\033[0m"
