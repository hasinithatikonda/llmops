.PHONY: install run test clean migrate help

help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies"
	@echo "  make run      - Run development server"
	@echo "  make test     - Run tests"
	@echo "  make clean    - Clean cache files"
	@echo "  make migrate  - Run database migrations"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf .pytest_cache

migrate:
	python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
