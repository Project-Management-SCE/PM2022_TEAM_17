FROM python:3-alpine
COPY . /StockFlow
WORKDIR /StockFlow
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD [ "python", "./manage.py", "runserver"]