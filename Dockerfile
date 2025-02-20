FROM python:3.12.3
WORKDIR /app
COPY . /app/
RUN pip install -r application/requirements.txt
ENTRYPOINT ["python", "application/__init__.py"]