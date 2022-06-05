FROM python:3-alpine
COPY ./ /.
WORKDIR /App
RUN pip install -r ./requirements.txt
EXPOSE 8181
CMD python3 ./main.py
