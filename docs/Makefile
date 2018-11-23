all: autograde publish
.PHONY: all

autograde:
	pdoc --overwrite --html autograde

build/notes.pdf: src/notes.tex
	pdflatex -output-directory build src/notes.tex

clean:
	rm -f build/*
.PHONY: clean

publish: build/notes.pdf
	cp build/*.pdf .
.PHONY: publish
