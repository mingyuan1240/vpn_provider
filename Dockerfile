FROM python:3.5

RUN pip install redis; \
	pip install flask; \
	pip install pysocks

WORKDIR /src
EXPOSE 80
CMD ["python", "server.py"]