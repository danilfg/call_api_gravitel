import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design
import requests
import time
import re

url_get_info = 'https://callapi.gravitel.ru/api/v1/getdialoutstat'
url_list = 'https://callapi.gravitel.ru/api/v1/listdialouts'
headers = {'Content-Type': 'application/json'}


def check_token():
    forCheckToken = requests.post(url_list, headers=headers, json={'token': token}).json()
    if forCheckToken['status'] == 'error':
        print("May be invalid token!")
        exit()


class ExampleApp(QtWidgets.QMainWindow, design.Ui_CounterCallAPI):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.found_dialouts.pressed.connect(self.connectUI)
        self.get_info_dialout.pressed.connect(self.get_info)

    def output_message(self, message_to_ui):
        self.output_info.setText(message_to_ui)

    def connectUI(self):
        token = self.token_enter.text()
        try:
            all_dialouts = requests.post(url_list, headers=headers, json={'token': token}).json()
            for_output = """
                <style type="text/css">
                   BODY {
                    background: white; 
                   }
                   TABLE {
                    width: 300px;
                    border-collapse: collapse;
                    border: 2px solid white;
                   }
                   TD, TH {
                    padding: 3px;
                    border: 1px solid maroon;
                    text-align: left;
                    }
                </style>
                <tr>
                    <th>ID автообзвона</th>
                    <th>Дата начала автообзвона</th>
                    <th>Дата окончания автообзвона</th>
                    <th>Статус автообзвона</th>
                </tr>"""
            for id_num in all_dialouts['result']:
                tsstart = time.ctime(id_num['tsstart'])
                tsend = time.ctime(id_num['tsend'])
                if id_num['status'] == 1:
                    status = 'Новый'
                elif id_num['status'] == 2:
                    status = 'Обработан'
                elif id_num['status'] == 3:
                    status = 'Запущен'
                elif id_num['status'] == 4:
                    status = 'Выполнен'
                elif id_num['status'] == 5:
                    status = 'Остановлен'
                else:
                    status = 'Ошибка'
                for_output = for_output + "<tr><td>" + str(id_num['id']) + "</td><td>" + tsstart + \
                             "</td><td>" + tsend + "</td><td>" + status + "</td></tr>"
            self.output_message(for_output)
        except:
            message_to_ui = "Не правильно введен токен"
            self.output_message(message_to_ui)

    def get_info(self):
        token = self.token_enter.text()
        id_dialout = self.dialout.text()
        try:
            all_dialouts = requests.post(url_get_info, headers=headers,
                                         json={'token': token, 'dialoutid': id_dialout}).json()
            for_output = """
                <style type="text/css">
                   BODY {
                    background: white; 
                   }
                   TABLE {
                    width: 300px;
                    border-collapse: collapse;
                    border: 2px solid white;
                   }
                   TD, TH {
                    padding: 3px;
                    border: 1px solid maroon;
                    text-align: left;
                    }
                </style>
                <tr>
                    <th>Номер</th>
                    <th>Время начала звонка</th>
                    <th>Статус звонка</th>
                    <th>Статус вызова</th>
                    <th>Длительность вызова</th>
                </tr>"""
            for info_num in all_dialouts['result']['data']:
                if (info_num['duration'] // 60) == 0:
                    duration = str(info_num['duration'] % 60) + ' сек'
                else:
                    duration = str((info_num['duration'] // 60)) + ' мин ' + str(info_num['duration'] % 60) + ' сек'

                if info_num['callstatus'] == 1:
                    callstatus = 'Новый'
                elif info_num['callstatus'] == 2:
                    callstatus = 'Активный'
                else:
                    callstatus = 'Завершен'

                if info_num['intstatus'] == 1:
                    intstatus = 'Новый'
                elif info_num['intstatus'] == 2:
                    intstatus = 'Получен ответ'
                elif info_num['intstatus'] == 3:
                    intstatus = 'Занято'
                elif info_num['intstatus'] == 4:
                    intstatus = 'Не сняли трубку'
                else:
                    intstatus = 'Ошибка'

                for_output = for_output + "<tr><td>" + str(info_num['number']) + "</td><td>" + info_num['tscall'] + \
                             "</td><td>" + callstatus + "</td><td>" + intstatus + "</td><td>" + duration + "</td></tr>"
            self.output_message(for_output)
        except:
            message_to_ui = "Что-то пошло не так"
            self.output_message(message_to_ui)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
