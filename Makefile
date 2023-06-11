.PHONY: all clean build test test_cmds publish

all: clean build test test_cmds

clean:
	poetry env remove --all
	rm -rf dist build *.egg-info .mypy_cache .pytest_cache htmlcov

build:
	poetry install
	poetry build

projects:
	neoncli project --create 1 --create 2 --create 3 --create 4 --create 5 --create 6 --create 7 --create 8 --create 9 --create 10 -c 11 -c 12 -c 13 -c 14 -c 15 -c 16 -c 17 -c 18 -c 19 -c 20
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


