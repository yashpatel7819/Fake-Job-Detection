from python:3.14-slim

workdir /app

copy requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py index.html model.pkl ./

EXPOSE 8000

CMD ['uvicorn','app:app','--host','--port','8000']