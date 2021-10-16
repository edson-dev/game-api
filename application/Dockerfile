FROM python:3.8
COPY requirements.txt ./application/requirements.txt
RUN pip3 install  FastAPI
RUN pip3 install uvicorn
RUN pip3 install -r ./application/requirements.txt
COPY ./ /
CMD ["python3", "main.py" ]
#CMD ["uvicorn", "app.main:app","--reload", "--host", "localhost", "--port", "8080" ]