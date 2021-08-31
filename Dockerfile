FROM python:3.9
COPY / ./farm-to-front-door/
WORKDIR farm-to-front-door
RUN /bin/sh -c 'pip install --no-cache-dir --index-url https://nexus.dev.afsmtddso.com/repository/pypi-internal/simple -r requirements.txt'
ENTRYPOINT ["python"]
CMD ["server.py"]
