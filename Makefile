.PHONY: all clean build lint test html livehtml

all: build html
clean:
	rm -rf ./dist ./docs/_build ./docs/api/*.rst

lint:
	pre-commit run --all-files
test:
	pytest -v ./tests
	./tests/test_examples.sh
build:
	python3 -m pip install build
	python3 -m build

html:
	env SPHINX_APIDOC_OPTIONS="members" \
		sphinx-apidoc --no-toc --separate --force --output-dir=./docs/api ./src
	sphinx-build -W -b html ./docs ./docs/_build/html
livehtml: html
	sphinx-autobuild -b html ./docs ./docs/_build/html
