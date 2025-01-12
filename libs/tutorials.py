from .securityLib import *
from .colorLib import *
from .animationLib import *

def tutorial_page_2():
	print(f'''{color_pink_bg('LESSON 2')}: Have fun
Create your custom code in the plugin folder.
Add a new cmd command for your plugin to the cmd section
of the main script: {color_pink_fg('todome.py')} then you're finished.

Have fun and keep the things as simple as possible <3.

One last tip before we end: in the securityLib.py
you are going to find a cool function it might be
for you handy to utilize.

End of Development pages.
''')

def tutorial_page_1() -> None:
	clear_screen()
	print('Starting Tutorial')
	tut = f'''{color_pink_bg('LESSON 1')}: Folder Structure

This project has the folllowing folder structure:
  {color_green_fg('├──')} plugins
  {color_green_fg('├──')} libs
  {color_green_fg('└──')} todome.py
-------------------------------------------------
This folder {color_green_fg('├──')} libs
    contains all the necessary libarys
    this applications needs.

For example colorLib.py contains all the necesarry
functions in order to color the output you are seeing
right now:

  def {color_pink_fg('color_pink_fg')}(text: str) -> str
  def {color_pink_bg('color_pink_bg')}(text: str) -> str
  def {color_green_fg('color_green_fg')}(text: str) -> str
  def {color_green_bg('color_green_bg')}(text: str) -> str
  def {color_darkgreen_fg('color_darkgreen_fg')}(text: str) -> str
  def {color_darkgreen_bg('color_darkgreen_bg')}(text: str) -> str
  def {color_red_fg('color_red_fg')}(text: str) -> str
  def {color_red_bg('color_red_bg')}(text: str) -> str
  def {color_yellow_fg('color_yellow_fg')}(text: str) -> str
  def {color_yellow_bg('color_yellow_bg')}(text: str) -> str
  def {color_magenta_fg('color_magenta_fg')}(text: str) -> str
  def {color_magenta_bg('color_magenta_bg')}(text: str) -> str

{color_pink_bg("isn't that awsome?")}
In the next lesson we will go through the security lib (tutorial in development....)

'''

	print(tut)


def development_tutorial() -> None:
	print(f"{color_magenta_bg('Hello')} from the tutorials lib.")
	cli = input(f"Wanna learn how to develop an an extension? (y/n)\n{color_green_fg('>')} ").upper()
	if cli == 'Q' or cli == 'N':
		return
	elif cli == 'Y':
		tutorial_page_1()
		wait_for_enter(tutorial_page_2)
		wait_for_enter()
	else: development_tutorial()

if __name__ == '__main__':
	development_tutorial()
