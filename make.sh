#!/bin/bash

doc(){
    echo "=== Génération de la documentation"
    pydoc3 -w src/*
	mv *.html doc/
	firefox doc/
}

build(){
    echo "=== Compilation du projet"
    pyinstaller --onefile --add-data "saves;saves" --add-data "doc;doc" --add-data "src;src" --add-data "assets;assets" --noconsole --icon=assets/icon.ico --name ScryNet src/main.py
}

run(){
    echo "=== Lancement de l'application"
    ./dist/ScryNet.exe
}

case "$1" in
    doc)
        doc
        ;;
    build)
        build
        ;;
    run)
        run
        ;;
    *)

        echo "Usage: $0 {build|run|doc}"
        exit 1
        ;;
esac    