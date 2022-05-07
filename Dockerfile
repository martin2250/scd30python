FROM python:3.10.4

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY scd30python /scd30python
WORKDIR /scd30python

CMD ["python", "read_minitsdb.py"]
