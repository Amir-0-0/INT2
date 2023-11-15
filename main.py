from tkinter import *
from scaning import Computer
from db import db, log
from db_setting import db_setting
import re


# функция которая запускается после ввода данных и их обработки
def start_of_scaning(host, user, password: str, port: int):
    # создаем объект класса computer, указываем введенные пользователем данные
    computer = Computer(host, user, password, port)
    # запускаем сканирование
    if computer.scaning() == 'error':
        show_error('Ошибка подключения по ssh, попробуйте снова')
        return 'error'
    # достаем результат сканирования
    data = computer.data
    if db(data['ОС'], data['Версия'], data['Архитектура']) == 'error':
        show_error('Ошибка при работе с базой данных')
        return 'error'
    return computer.data


# создание и настройка окна
root = Tk()
root.geometry('300x400')
root['bg'] = '#82c1e9'
root.title('Сканер системы')
for_labels = {'font': ('Open Sans', 15),
              'background': '#82c1e9',
              'foreground': '#1b13cc'
              }
# два списка для хранения элементов экрана для ввода данных и экрана вывода данных
main_screen = []
data_labels = []


# функция для вывода ошибок пользователю
def show_error(error):
    global labelForError
    labelForError['text'] = error
    labelForError.pack()


# Функция, которая запускается при нажатии кнопки для ввода данных
def click():
    labelForError.pack_forget()
    # обработка введенных данных
    login = login_entry.get().replace(' ', '')
    password = password_entry.get().replace(' ', '')
    ip = ip_entry.get().replace(' ', '')
    if not (re.match("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip)):
        log('[Error] Введен некорректный ip')
        show_error(error='Введен некорректный ip')
        ip_entry.delete(0, END)
        return None

    port = int(port_entry.get())
    if not (0 < port < 65536):
        log('[Error] Введен некорректный порт')
        show_error(error='Введен некорректный порт')
        port_entry.delete(0, END)
        return None

    # запуск функции с сканированием
    data = start_of_scaning(ip, login, password, port)
    if data == 'error':
        return 1

    # отчистка полей для ввода
    for entry in login_entry, port_entry, password_entry, ip_entry:
        entry.delete(0, END)

    # отчистка окна от старых элементов
    global main_screen
    for element in main_screen:
        element.place_forget()

    # вывод полученных данных на экран
    root.geometry('600x300')
    global data_labels
    x = 0
    for i in data.items():
        tempKey = Label(root, text=i[0] + ':', font=for_labels['font'], background=for_labels['background'],
                        foreground=for_labels['foreground'])
        tempValue = Label(root, text=i[1], font=for_labels['font'], background=for_labels['background'],
                          foreground='#000000')
        tempValue.place(relx=0.5, rely=0.2 + x)
        tempKey.place(relx=0.1, rely=0.2 + x)
        data_labels.append(tempKey)
        data_labels.append(tempValue)
        x += 0.1

    # кнопка назад
    back_button.place(relx=0.7, rely=0.8)


# создание заголовка
label = Label(root, text='Сканер', font=('Open Sans', 25), background='#82c1e9', foreground='#1b13cc')
label.pack(anchor='n')

# создание названий всех полей
entry_names = ['login:', 'password:', 'ip:', 'port:']
for i in range(4):
    main_screen.append(Label(root, text=entry_names[i], font=for_labels['font'], background=for_labels['background'],
                             foreground=for_labels['foreground']))

for i in range(4):
    main_screen[i].place(relx=0.1, rely=0.2 + i / 10)

# label, который будет использоваться для вывода ошибки пользователю
errorLabel = Label(root, text="вывод ошибок", foreground='#FF0000')

# поля для ввода данных
login_entry = Entry(root)
login_entry.place(relx=0.5, rely=0.2)
password_entry = Entry(root, show='*')
password_entry.place(relx=0.5, rely=0.3)
ip_entry = Entry(root)
ip_entry.place(relx=0.5, rely=0.4)
port_entry = Entry(root)
port_entry.place(relx=0.5, rely=0.5)
entryes = [login_entry, password_entry, ip_entry, port_entry]
main_screen.extend(entryes)

# кнопка для внесения данных
button = Button(root, text='Внести данные', font=('Open Sans', 15), background='#F0F0FF', foreground='#0000FF',
                command=click, activebackground='#0000FF', activeforeground='#F0F0FF')
button.place(relx=0.1, rely=0.7)
main_screen.append(button)

# кнопка для настройки базы данных
db_button = Button(root, text='Настроить базу данных', font=('Open Sans', 10), background='#F0F0FF',
                   foreground='#0000FF',
                   command=db_setting, activebackground='#0000FF', activeforeground='#F0F0FF')
db_button.place(relx=0.1, rely=0.9)
main_screen.append(db_button)

# надпись для ошибок
labelForError = Label(root, text='', foreground='#FF0000')
main_screen.append(labelForError)


# функция для возращения основного экрана(для ввода данных)
def back():
    back_button.place_forget()
    root.geometry('300x400')
    for element in data_labels:
        element.place_forget()

    for i in range(4):
        main_screen[i].place(relx=0.1, rely=0.2 + i / 10)
    for i in range(4, 8):
        main_screen[i].place(relx=0.5, rely=(i - 2) / 10)
    main_screen[8].place(relx=0.1, rely=0.7)
    main_screen[9].place(relx=0.1, rely=0.9)


# кнопка для возращения основного экрана
back_button = Button(root, text='назад', font=('Open Sans', 15), background='#F0F0FF',
                     foreground='#0000FF',
                     command=back, activebackground='#0000FF', activeforeground='#F0F0FF')

# запуск окна(цикла для окна)
root.mainloop()
