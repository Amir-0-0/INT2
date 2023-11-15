import paramiko
from logs import log


# класс содержащий поля с информацией для соединения к ОС и содержащий методы для сканирования ОС
class Computer:
    def __init__(self, hostname, username, password: str, port: int):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.data = {'ОС': 'Unknown Linux',
                     'Версия': 'Unknown',
                     'Архитектура': 'Unknown'}

    # резервное сканирование компьютера(на случай если по каким-то причинам не сработало первое
    def backup_scaning(self):
        # подключаемся по ssh
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            client.connect(hostname=self.hostname,
                           username=self.username,
                           password=self.password,
                           port=self.port)
        except Exception as e:
            log('[Error] Ошибка при подключении по ssh ' + str(e))
            return 'error'

        # Выполняем команду для нахождения информации о ОС
        log(f'[INFO] подключение к {self.hostname} установлено')
        stdin, stdout, stderr = client.exec_command('cat /etc/*release* | grep \'NAME="\'')
        result = stdout.read().decode('utf-8').replace(' ', '').split('\n')
        self.data['ОС'] = result[0].split('=')[1]

        # Выполняем команду для нахождения информации о версии ОС
        stdin, stdout, stderr = client.exec_command('cat /etc/*release* | grep \'VERSION=\'')
        result = stdout.read().decode('utf-8').replace(' ', '').split('\n')
        self.data['Версия'] = result[0].split('=')[1]

        # Выполняем команду для нахождения информации о архитектуре ОС
        stdin, stdout, stderr = client.exec_command('/usr/bin/lscpu | grep Architecture')
        result = stdout.read().decode('utf-8').replace(' ', '').split('\n')
        self.data['Архитектура'] = result[0].split(':')[1]

        client.close()
        log(f'[INFO] Сканирование окончено')

    # Сканирование компьютера
    def scaning(self):
        # подключаемся по ssh
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            client.connect(hostname=self.hostname,
                           username=self.username,
                           password=self.password,
                           port=self.port)
        except Exception as e:
            log('[Error] Ошибка при подключении по ssh ' + str(e))
            return 'error'
        log(f'[INFO] подключение к {self.hostname} установлено')

        # выполняем команду для сбора информации об ОС
        stdin, stdout, stderr = client.exec_command('hostnamectl')
        result = stdout.read().decode('utf-8').replace(' ', '').split('\n')

        # если в результате выполнения команды мы не получили информации, то логируем ошибку и запускаем резервное
        # сканирование
        if result == ['']:
            log('[Error]' + stderr.read().decode('utf-8'))
            client.close()
            return self.backup_scaning()

        # Обрабатываем полученую информацию
        for i in result:
            if i.find(':') != -1:
                key, value = i.split(':')
                keys = {'Statichostname': 'ОС',
                        'OperatingSystem': 'Версия',
                        'Architecture': 'Архитектура'}
                if key in keys.keys():
                    self.data[keys[key]] = value

        client.close()
        log(f'[INFO] Сканирование окончено')
