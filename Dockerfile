FROM python:3.10-alpine

RUN ["/bin/sh", "-c", "apk add --update --no-cache bash ca-certificates"]

COPY ["src", "/src/"]

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/src/main.py"]

