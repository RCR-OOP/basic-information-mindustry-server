# БИМС
from threading import Thread
import tkinter as tk
import pydustry
import time
import json
import sys
import os
import re

# Перемены для работы
class operation:
	TimeUpdate = True
	InfoServerUpdate = True

cfgd_std = {
				"host": "rcr.fvds.ru",
				"port": 6567,
				"attributes": False
}

class config_data:
	if "config.json" in os.listdir():
		try:
			with open("config.json") as config_data_file:
				config_data_dict = json.load(config_data_file)
			host = config_data_dict["host"]
			port = config_data_dict["port"]
			attributes = config_data_dict["attributes"]
		except:
			host = cfgd_std["host"]
			port = cfgd_std["port"]
			attributes = cfgd_std["attributes"]
			config_data_dict = cfgd_std
			with open("config.json", "w") as config_data_file:
				json.dump(config_data_dict, config_data_file)
	else:
		host = cfgd_std["host"]
		port = cfgd_std["port"]
		attributes = cfgd_std["attributes"]
		config_data_dict = cfgd_std
		with open("config.json", "w") as config_data_file:
			json.dump(config_data_dict, config_data_file)

# Инфомация программы
class proginfo:
	name = "БИМС"
	version = "0.1-beta"
	author = "Роман Слабицкий"

# Создание окна и настройка
root = tk.Tk()
root.title(str(proginfo.name) + " v" + str(proginfo.version))
root.geometry("500x105")
root.resizable(0, 0)
root.attributes("-topmost", config_data.attributes)

# Объекты
TimeLabel = tk.Label(root, text = "Загрузка", font = 'helvetica 10 bold', bg = "black", fg = "white", width = 10)
NameServerLabel = tk.Label(root, text = "Имя севрера: Загрузка...", font = 'helvetica 10 bold')
MapServerLabel = tk.Label(root, text = "Карта: Загрузка...", font = 'helvetica 10 bold')
PlayersServerLabel = tk.Label(root, text = "Игроков: Загрузка...", font = 'helvetica 10 bold')
WaveServerLabel = tk.Label(root, text = "Волна: Загрузка...", font = 'helvetica 10 bold')
VersionServerLabel = tk.Label(root, text = "Версия ядра: Загрузка...", font = 'helvetica 10 bold')
ButtonSwitchingOptionsAttributes = tk.Label(root, text = "📌", font = 'helvetica 12 bold')
if config_data.attributes:
	ButtonSwitchingOptionsAttributes["fg"] = "green"
else:
	ButtonSwitchingOptionsAttributes["fg"] = "red"

# Постановка объектов
TimeLabel.place(x = 415, y = 0)
NameServerLabel.place(x = 5, y = 0)
MapServerLabel.place(x = 5, y = 20)
PlayersServerLabel.place(x = 5, y = 40)
WaveServerLabel.place(x = 5, y = 60)
VersionServerLabel.place(x = 5, y = 80)
ButtonSwitchingOptionsAttributes.place(x = 390, y = -5)

# Логика
def UpdateTimeHandler():
	while operation.TimeUpdate:
		try:
			TimeLabel["text"] = str(time.strftime("%H:%M:%S", time.localtime()))
		except:
			TimeLabel["text"] = "Ошибка"
		time.sleep(0.5)

def UpdateServerInfoLabels():
	MindServer = pydustry.Server(str(config_data.host), int(config_data.port))
	while operation.InfoServerUpdate:
		try:
			mind_status = MindServer.get_status()
			NameServerLabel["text"] = "Имя севрера: {0}".format((re.sub(r"(?<=\[).*?(?=\])", "", mind_status["name"])).replace("[", "").replace("]", ""))
			MapServerLabel["text"] = "Карта: " + str(mind_status["map"])
			PlayersServerLabel["text"] = "Игроков: " + str(mind_status["players"])
			WaveServerLabel["text"] = "Волна: " + str(mind_status["wave"])
			VersionServerLabel["text"] = "Версия ядра: " + str(mind_status["version"])
		except:
			NameServerLabel["text"] = "Имя севрера: Ошибка"
			MapServerLabel["text"] = "Карта: Ошибка"
			PlayersServerLabel["text"] = "Игроков: Ошибка"
			WaveServerLabel["text"] = "Волна: Ошибка"
			VersionServerLabel["text"] = "Версия ядра: Ошибка"
		time.sleep(0.5)

def SwitchingOptionsAttributes(event):
	global config_data
	if config_data.attributes:
		config_data.attributes = False
		config_data.config_data_dict["attributes"] = False
		root.attributes("-topmost", config_data.attributes)
		ButtonSwitchingOptionsAttributes["fg"] = "red"
	else:
		config_data.attributes = True
		config_data.config_data_dict["attributes"] = True
		root.attributes("-topmost", config_data.attributes)
		ButtonSwitchingOptionsAttributes["fg"] = "green"
	with open("config.json", "w") as config_data_file:
		json.dump(config_data.config_data_dict, config_data_file)

# Привязка объектов у логике
ButtonSwitchingOptionsAttributes.bind('<Button-1>', SwitchingOptionsAttributes)

# Запуск в фоне
Thread(target = UpdateTimeHandler, args = (), daemon = True).start()
Thread(target = UpdateServerInfoLabels, args = (), daemon = True).start()

# Конец
root.mainloop()
operation.TimeUpdate = False