from .colorLib import *

def clear_screen() -> None:
	print("\n" * 100)  # Prints many newlines to push old content up

def welcome_screen(verbose: bool) -> None:
	if verbose == True:
		return f"🦄 {color_pink_bg('TODOME')} List Manager - Type '{color_yellow_fg('help')}' for commands"
	else: return f"🦄 {color_pink_bg('TODOME')} List Manager"



if __name__ == '__main__':
	welcome_screen()
