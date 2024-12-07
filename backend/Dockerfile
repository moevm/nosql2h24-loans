FROM python:3.9.17-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
#CMD ["sh", "-c", "python init_db.py && python main.py"]
CMD ["python", "-u", "app/main.py"]