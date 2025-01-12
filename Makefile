all: build install clean

build:
	pyinstaller todome.py --onefile
	cp ./dist/todome .

clean:
	rm -rf ./dist ./build ./*.spec todome __pycache__ *.tar ./libs/__pycache__ ./plugins/__pycache__

install:
	cp todome ~/.local/bin/

deinstall:
	rm  ~/.local/bin/todome

reinstall: clean build deinstall install clean

compress-src: clean
	ouch compress todome.py libs/ Makefile plugins README.md todome_v.0.1-pre.tar
