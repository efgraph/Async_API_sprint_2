Поднять сервисы:

    docker-compose up

Установить зависимости:

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Запустить проект:

    uvicorn src.main:app --reload
    