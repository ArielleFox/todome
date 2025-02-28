all: build install alpha clean

venv:
	python3.13 -m venv venv

build:
	mkdir -p ~/.config/todome/
	pyinstaller todome.py --onefile
	pyinstaller alpha.py --onefile
	cp ./dist/todome .
	mv ./dist/alpha  ~/.config/todome/alpha
	chmod +x  ~/.config/todome/alpha

clean:
	rm -rf ./dist ./build ./*.spec todome __pycache__ *.tar ./libs/__pycache__ ./plugins/__pycache__

install:
	cp todome ~/.local/bin/
	mkdir -p ~/.config/todome/
alpha:
	mkdir -p home/arielle/.config/todome/
	#echo "" > ~/.config/todome/config.yaml

deinstall:
	rm  ~/.local/bin/todome ~/.config/todome/config.yaml

reinstall: clean build deinstall install clean

compress-src: clean
	ouch compress todome.py libs/ Makefile plugins README.md todome_v.0.1-pre.tar
