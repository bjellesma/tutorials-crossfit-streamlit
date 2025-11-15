.PHONY: frontend backend test fulltest install lint


PYTHON ?= 3.10


frontend:
	cd frontend && uv run $(if $(PYTHON),--python $(PYTHON),) streamlit run main.py


backend:
	cd backend && uv run $(if $(PYTHON),--python $(PYTHON),) uvicorn routes:app --reload --port 5000


test:
	uv run $(if $(PYTHON),--python $(PYTHON),) pytest -m single -v --cov=.


fulltest:
	uv run $(if $(PYTHON),--python $(PYTHON),) pytest -v --cov=.


install:
	uv sync $(if $(PYTHON),--python $(PYTHON),)


lint:
	uv run $(if $(PYTHON),--python $(PYTHON),) ruff check .
