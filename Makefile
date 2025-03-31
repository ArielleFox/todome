all: venv clean build alpha

venv:
	python3.13 -m venv ~/Apps/todome-venv; source ~/Apps/todome-venv/bin/activate; pip install -r requirements.txt; deactivate;
	source ~/Apps/todome-venv/bin/activate; pip install pyyaml; pip install requests; pip install --upgrade pip; deactivate;

build:
	mkdir -p ~/.config/todome/
	source ~/Apps/todome-venv/bin/activate; pyinstaller todome.py --onefile
	source ~/Apps/todome-venv/bin/activate; pyinstaller alpha.py --onefile
	mv ./dist/alpha  ~/.config/todome/alpha
	chmod +x  ~/.config/todome/alpha
	mkdir -p ~/Apps/libs; rm -rf ~/Apps/libs/*; mkdir -p ~/Apps/plugins; cp -r plugins/* ~/Apps/plugins/ ; cp -r libs/* ~/Apps/libs/;
clean:
	rm -rf ./dist ./build ./*.spec todome __pycache__ *.tar ./libs/__pycache__ ./plugins/__pycache__ ~/Apps/libs/color*.py

install:
	cp todome.py $HOME/Apps/todome.py
	mkdir -p ~/.config/todome/
alpha:
	mkdir -p home/arielle/.config/todome/
	#echo "" > ~/.config/todome/config.yaml

deinstall:
	rm  ~/.local/bin/todome ~/.config/todome/config.yaml

reinstall: clean build deinstall install clean

compress-src: clean
	ouch compress todome.py libs/ Makefile plugins README.md todome_v.0.1-pre.tar
run:
	source ~/Apps/todome-venv/bin/activate; pip install pyyaml; pip install requests; pip install --upgrade pip; cd ~/Apps/; ./todome.py; deactivate; cd -;
