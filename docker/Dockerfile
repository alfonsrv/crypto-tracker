FROM python:3.8-slim as base
LABEL maintainer="alfonsrv <alfonsrv@protonmail.com>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Ensure layers stay small
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev libsasl2-dev libssl-dev \
    && apt-get install -y --no-install-recommends netcat libpq-dev postgresql-client tzdata \
    && apt-get install -y --no-install-recommends git libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt

FROM base
LABEL maintainer="alfonsrv <alfonsrv@protonmail.com>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app/
#COPY --from=base /venv /venv
COPY ./docker/docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh
COPY ./docker/start.sh /app/
RUN chmod +x /app/start.sh

RUN adduser --uid 9000 --disabled-password --gecos "" rausys && \
    usermod -a -G rausys rausys

VOLUME ["/app/static", "/app/media_files", "/app/ca_files"]

RUN chown -R rausys:rausys /app/media_files && \
    chown -R rausys:rausys /app/static

RUN update-ca-certificates --fresh
USER rausys:rausys
WORKDIR /app

ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]
CMD ["sh", "/app/start.sh"]
