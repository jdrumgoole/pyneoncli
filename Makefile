.PHONY: all clean build test publish

all: clean build test

clean:
	poetry env remove
	rm -rf dist build *.egg-info .mypy_cache .pytest_cache htmlcov

build:
	poetry install
	poetry build

test:
	poetry run pytest

publish: all
	poetry publish

test_publish: all
	poetry publish -r testpypi

test_neoncli:
	neoncli -h
	neoncli --version
	neoncli project --list
	neoncli project --create dummy_project > grep id
	neoncli branch --project_id red-sea-544606 --list

