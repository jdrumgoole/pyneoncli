.PHONY: all clean build test test_cmds publish

all: clean build test test_cmds

clean:
	poetry env remove --all
	rm -rf dist build *.egg-info .mypy_cache .pytest_cache htmlcov

build:
	poetry install
	poetry build

test:
	poetry run pytest

test_cmds:
	neoncli -h > /dev/null
	neoncli --version > /dev/null
	neoncli list  > /dev/null
	neoncli list -h > /dev/null
	neoncli project -h > /dev/null
	neoncli branch -h > /dev/null
	neoncli project --create "dummy" > /dev/null
	neoncli  list --project_name dummy | head -1 | cut -f3 -d: > dummy_project_id
	neoncli list --branches `cat dummy_project_id` > /dev/null
	neoncli --nocolor list > /dev/null
	neoncli --fieldfilter id --nocolor list> /dev/null
	neoncli --fieldfilter id branch --create `cat dummy_project_id` > /dev/null
	neoncli --yes project --delete `cat dummy_project_id` > /dev/null
	rm dummy_project_id

publish: all
	poetry publish

test_publish: all
	poetry publish -r testpypi


