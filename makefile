.PHONY: all clean build test publish

all: clean build test

clean:
    poetry env remove -y
    rm -rf dist build *.egg-info .mypy_cache .pytest_cache htmlcov

build:
    poetry install
    poetry build

test:
    poetry run pytest --cov=my_project --cov-report=html

publish:
    poetry publish

