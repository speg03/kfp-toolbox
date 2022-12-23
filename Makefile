.PHONY: all clean requirements lint test dist html livehtml

all: dist html
clean:
	rm -rf ./dist ./docs/_build ./docs/api/*.rst

requirements:
	pip-compile --upgrade --output-file=requirements.txt --resolver=backtracking pyproject.toml

lint:
	pre-commit run --all-files
test:
	pytest -v ./tests
dist:
	python3 -m build

html:
	env SPHINX_APIDOC_OPTIONS="members" \
		sphinx-apidoc --no-toc --separate --force --output-dir=./docs/api ./src
	sphinx-build -W -b html ./docs ./docs/_build/html
livehtml: html
	sphinx-autobuild -b html ./docs ./docs/_build/html
