from tkinter import *
from logs import log
from lxml import etree

# функция для изменени данных о базе данных
def db_setting():
    log('[INFO] Настройка соединения к базе данных')

    # Функция, которая вносит введеные пользователе данные о базе данных в xml-файл, функция запускается при нажатии
    # кнопки
    def change():
        tree = etree.parse('db.xml')
        root = tree.getroot()
        for i in range(4):
            root[i].text = field_entry[i].get().replace(' ', '')
        tree.write('db.xml')
        log('[INFO] Изменения сохранены')
        window.destroy()

    # Ниже код для создания окна и элементов внутри него
    for_labels = {'font': ('Open Sans', 15),
                  'background': '#82c1e9',
                  'foreground': '#1b13cc'
                  }

    window = Tk()
    window.title('Настройка базы данных')
    window.geometry('300x300')
    window['bg'] = for_labels['background']

    label = Label(window,
                  text='Данные для подключения к\n базе данных',
                  font=('Open Sans', 15),
                  background=for_labels['background'],
                  foreground=for_labels['foreground'])
    label.pack(anchor='n')

    button = Button(window, text='Внести изменения', font=('Open Sans', 15),
                    command=change, activebackground='#0000FF', activeforeground='#F0F0FF')
    button.place(relx=0.1, rely=0.8)

    field_labels = []
    field_entry = []
    name_of_field = ['hostname', 'user', 'password', 'name']
    for i in name_of_field:
        field_labels.append(Label(window,
                                  text=i,
                                  font=('Open Sans', 14),
                                  foreground=for_labels['foreground'],
                                  background=for_labels['background']
                                  )
                            )
        field_entry.append(Entry(window))
    for i in range(4):
        field_labels[i].place(relx=0.1, rely=0.3 + i / 10)
        field_entry[i].place(relx=0.5, rely=0.3 + i / 10)
    field_entry[2]['show'] = '*'
    window.mainloop()
