.PHONY: all clean build lint test html livehtml

all: build html
clean:
	rm -rf ./dist ./docs/_build ./docs/api/*.rst

lint:
	pre-commit run --all-files
test:
	pytest -v ./tests
build: lint test
	poetry build

html:
	sphinx-apidoc --no-toc --force --output-dir=./docs/api ./src
	sphinx-build -W -b html ./docs ./docs/_build/html
livehtml: html
	sphinx-autobuild -b html ./docs ./docs/_build/html
