FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./restapi.py ./Room.py ./RoomManager.py ./ConnectionManager.py /code/

CMD ["uvicorn", "restapi:app", "--host", "0.0.0.0", "--port", "8000"]