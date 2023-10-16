FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./spam.csv /code/spam.csv


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app.py /code/app.py

COPY ./model_for_spam /code/model_for_spam

CMD ["uvicorn","app:app" ,"--host","0.0.0.0"]