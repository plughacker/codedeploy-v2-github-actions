FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

RUN ["/bin/sh", "-c", "apk add --update --no-cache bash ca-certificates"]

COPY ["src", "/src/"]

COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/src/main.py"]

