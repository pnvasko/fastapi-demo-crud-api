FROM python:3.9-slim

WORKDIR /app
COPY ["requirements.txt", "./"]
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# RUN uvicorn app.main:app --host 0.0.0.0 --port 8000
# docker build --rm -t dream-x-crud-api .
# docker run -it --rm --name dream-x-crud-api -p 8000:8000 dream-x-crud-api