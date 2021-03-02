FROM python:3.9

WORKDIR /usr/src/djask
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x ep.sh
CMD ./ep.sh


