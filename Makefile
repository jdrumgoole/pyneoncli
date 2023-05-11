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
	neoncli -h > /dev/null
	neoncli --version > /dev/null
	neoncli project --list > /dev/null
	neoncli --nocolor project --list > /dev/null
	neoncli --fieldfilter id --nocolor project --list > /dev/null
	neoncli branch --list --project_id red-sea-544606 --list > /dev/null
	neoncli branch --get --project_id red-sea-544606 --branch_id br-muddy-wildflower-293772 > /dev/null

