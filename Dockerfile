FROM python:3.10-alpine

RUN ["/bin/sh", "-c", "apk add --update --no-cache bash ca-certificates"]

COPY ["src", "/src/"]

ENTRYPOINT ["/src/main.py"]
