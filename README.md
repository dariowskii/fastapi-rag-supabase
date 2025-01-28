# Setup

## Python VENV

Create a virtual environment for the project:

```bash
python -m venv venv
```

Activate the virtual environment:

(Windows)
```bash
venv\Scripts\activate
```

(Linux/Mac)
```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run FastAPI

Run the FastAPI server:

```bash
fastapi dev main.py
```