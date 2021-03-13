.PHONY: clean build run

test:
	poetry run python -m pytest

build: test
	docker build -t mcbot .

run: build
	docker run -d -p 8000:8000 mcbot