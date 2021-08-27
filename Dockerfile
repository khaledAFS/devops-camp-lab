FROM python:3.9
RUN /bin/sh -c 'pip install --index-url https://nexus.dev.afsmtddso.com/repository/labs-pypi-proxy/simple/'
ENTRYPOINT ["python"]
CMD ["server.py"]