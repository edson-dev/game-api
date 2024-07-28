FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python","main.py"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]