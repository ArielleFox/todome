#!/bin/env python3
import os
import getpass

# mv /libs/colorLib.py cache/
# cp lite/libs/colorLib.py /libs/colorLib.py

# mv cache/colorLib.py /libs/colorLib.py

def main():
	USERNAME = getpass.getuser()
	os.system('mkdir -p ./cache')
	print('''
Options:
	lite
	classic
''')
	cli = input('⌬ ')
	if cli == 'lite':
		print('Generating From Template:    Lite Version')
		os.system(f'echo "#!/home/{USERNAME}/Apps/todome-venv/bin/python3.13" > todome.py')
		os.system('cat cache/todome.code >> todome.py; cp todome.py /home/ashley/Apps/todome.py;')
		os.system('mv libs/colorLib.py cache/colorLib.py; mv lite/libs/colorLib.py libs/colorLib.py; ')
		os.system('make')
		os.system('mv libs/colorLib.py lite/libs/colorLib.py; mv cache/colorLib.py libs/colorLib.py; chmod +x todome.py;')
		print("""Please add this line to your .bash_aliases file:\n        alias todome='source ~/Apps/todome-venv/bin/activate; pip install pyyaml; pip install requests; pip install --upgrade pip; cd ~/Apps/ && python3 ./todome.py; deactivate; cd -;'""")
	elif cli == 'classic':
		print('Generating From Template:    Classic Version')
		os.system('make')

main()
