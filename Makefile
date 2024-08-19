all:
	@echo -n "=== Lancement du programme de pilotage de l'analyseur de spectre\n"
	@python3 ./src/main.py

.PHONY: doc build

doc:
	@echo "=== Génération de la documentation"
	@pydoc3 -w src/*
	@mv *.html doc/
	@firefox doc/

build:
	@echo "=== Compilation du projet"
	@pyinstaller --onefile --add-data "saves;saves" --add-data "doc;doc" --add-data "src;src" src/main.py