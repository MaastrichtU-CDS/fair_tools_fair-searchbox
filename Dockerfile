FROM python:3-stretch

ADD ./app /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5050
CMD ["python", "runService.py"]