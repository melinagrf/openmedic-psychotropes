.PHONY: install run

install:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt

run:
	.venv/bin/python -m streamlit run app.py
