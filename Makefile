dev:
	fastapi dev src/main.py

start:
	fastapi run src/main.py

build:
	docker build -t ajchili/visum:latest .