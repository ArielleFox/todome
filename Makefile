all: build install clean

build:
	pyinstaller todome.py --onefile
	cp ./dist/todome .

clean:
	rm -rf ./dist ./build ./*.spec todome __pycache__ *.tar ./libs/__pycache__ ./plugins/__pycache__ ~/.config/todome/

install:
	cp todome ~/.local/bin/
	mkdir ~/.config/todome/
	#echo "" > ~/.config/todome/config.yaml

deinstall:
	rm  ~/.local/bin/todome ~/.config/todome/config.yaml

reinstall: clean build deinstall install clean

compress-src: clean
	ouch compress todome.py libs/ Makefile plugins README.md todome_v.0.1-pre.tar
