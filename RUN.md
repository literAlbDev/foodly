# RUN.md

## Install requirements

```bash
pip install -r requirements.txt
```

## Initialize database

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

## Run the project

```bash
python main.py
```