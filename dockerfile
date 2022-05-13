FROM python:3
ENV PYTHONUNBUFFERED=1
COPY . /
WORKDIR /StockFlow 
RUN pip install -r requirements.txt
ENTRYPOINT ["sh","entrypoint.sh"]

