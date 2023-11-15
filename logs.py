from datetime import datetime


# функция для создания логов
def log(information: str):
    with open('logs.txt', 'a') as logs:
        logs.write(f'{information} {__file__} {datetime.now()}\n')
