# БИМС
import tkinter as tk
from tkinter.ttk import Combobox
from threading import Thread
import pydustry
import pyglet
import time
import wget
import json
import sys
import os
import re

# Перемены для работы
class operation:
	TimeUpdate = True
	InfoServerUpdate = True
	ServersListUpdate = True

cfgd_std = {
				"attributes": False
}

class config_data:
	if "config.json" in os.listdir():
		try:
			with open("config.json") as config_data_file:
				config_data_dict = json.load(config_data_file)
			attributes = config_data_dict["attributes"]
		except:
			attributes = cfgd_std["attributes"]
			config_data_dict = cfgd_std
			with open("config.json", "w") as config_data_file:
				json.dump(config_data_dict, config_data_file)
	else:
		attributes = cfgd_std["attributes"]
		config_data_dict = cfgd_std
		with open("config.json", "w") as config_data_file:
			json.dump(config_data_dict, config_data_file)
	hosts = {}
	host = None
	port = None

pyglet.font.add_file(os.path.abspath("Minecraft.ttf"))

# Инфомация программы
class proginfo:
	name = "БИМС"
	version = "0.2.1-beta"
	versionint = 0.21
	author = "Роман Слабицкий"
	company = "RCR"

# Создание окна и настройка
root = tk.Tk()
root.title("{0} v{1} ({2})".format(proginfo.name, proginfo.version, proginfo.versionint))
root.geometry("500x130")
root.resizable(0, 0)
root.attributes("-topmost", config_data.attributes)

# Объекты
try:
	TimeLabel = tk.Label(root, text = "Загрузка", font = ('Minecraft Rus', 8), bg = "black", fg = "white", width = 10)
	NameServerLabel = tk.Label(root, text = "Имя севрера: Загрузка...", font = ('Minecraft Rus', 8))
	MapServerLabel = tk.Label(root, text = "Карта: Загрузка...", font = ('Minecraft Rus', 8))
	PlayersServerLabel = tk.Label(root, text = "Игроков: Загрузка...", font = ('Minecraft Rus', 8))
	WaveServerLabel = tk.Label(root, text = "Волна: Загрузка...", font = ('Minecraft Rus', 8))
	VersionServerLabel = tk.Label(root, text = "Версия ядра: Загрузка...", font = ('Minecraft Rus', 8))
	ButtonSwitchingOptionsAttributes = tk.Label(root, text = "📌", font = ('Minecraft Rus', 12))
	ComboboxListServers = Combobox(root, width = 78)
except:
	TimeLabel = tk.Label(root, text = "Загрузка", font = 'helvetica 10 bold', bg = "black", fg = "white", width = 10)
	NameServerLabel = tk.Label(root, text = "Имя севрера: Загрузка...", font = 'helvetica 10 bold')
	MapServerLabel = tk.Label(root, text = "Карта: Загрузка...", font = 'helvetica 10 bold')
	PlayersServerLabel = tk.Label(root, text = "Игроков: Загрузка...", font = 'helvetica 10 bold')
	WaveServerLabel = tk.Label(root, text = "Волна: Загрузка...", font = 'helvetica 10 bold')
	VersionServerLabel = tk.Label(root, text = "Версия ядра: Загрузка...", font = 'helvetica 10 bold')
	ButtonSwitchingOptionsAttributes = tk.Label(root, text = "📌", font = 'helvetica 12 bold')
	ComboboxListServers = Combobox(root, width = 78)
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
ComboboxListServers.place(x = 5, y = 105)

# Логика
def UpdateTimeHandler():
	while operation.TimeUpdate:
		try:
			TimeLabel["text"] = str(time.strftime("%H:%M:%S", time.localtime()))
		except:
			TimeLabel["text"] = "Ошибка"
		time.sleep(0.5)

def HandlerComboBoxLS():
	ls_filename = str(wget.download("https://raw.githubusercontent.com/Anuken/Mindustry/master/servers_v6.json"))
	with open(ls_filename) as ls_file:
		ls_data = json.load(ls_file)
	os.remove(ls_filename)

	for i in ls_data:
		for n in i["address"]:
			ServerData = n.split(":")
			if len(ServerData) > 1:
				config_data.hosts["({0}) {1}".format((re.sub(r"(?<=\[).*?(?=\])", "", i["name"])).replace("[", "").replace("]", ""), n)] = {"host": str(ServerData[0]), "port": int(ServerData[1])}
			else:
				config_data.hosts["({0}) {1}".format((re.sub(r"(?<=\[).*?(?=\])", "", i["name"])).replace("[", "").replace("]", ""), n)] = {"host": str(ServerData[0]), "port": 6567}

	ComboboxListServers['value'] = tuple(config_data.hosts)
	ComboboxListServers.current(0)

	while operation.ServersListUpdate:
		name = str(ComboboxListServers.get())
		if name in list(config_data.hosts):
			config_data.host = config_data.hosts[name]["host"]
			config_data.port = config_data.hosts[name]["port"]
		time.sleep(0.5)

def UpdateServerInfoLabels():
		while operation.InfoServerUpdate:
			if (config_data.host != None) and (config_data.port != None):
				MindServer = pydustry.Server(str(config_data.host), int(config_data.port))
				try:
					mind_status = MindServer.get_status(timeout = 3.0)
					NameServerLabel["text"] = "Имя севрера: {0}".format((re.sub(r"(?<=\[).*?(?=\])", "", mind_status["name"])).replace("[", "").replace("]", ""))
					MapServerLabel["text"] = "Карта: " + str((re.sub(r"(?<=\[).*?(?=\])", "", mind_status["map"])).replace("[", "").replace("]", ""))
					PlayersServerLabel["text"] = "Игроков: " + str(mind_status["players"])
					WaveServerLabel["text"] = "Волна: " + str(mind_status["wave"])
					VersionServerLabel["text"] = "Версия ядра: " + str(mind_status["version"])
				except:
					NameServerLabel["text"] = "Имя севрера: Сервер не доступен"
					MapServerLabel["text"] = "Карта: Сервер не доступен"
					PlayersServerLabel["text"] = "Игроков: Сервер не доступен"
					WaveServerLabel["text"] = "Волна: Сервер не доступен"
					VersionServerLabel["text"] = "Версия ядра: Сервер не доступен"
			else:
				NameServerLabel["text"] = "Имя севрера: Секунду..."
				MapServerLabel["text"] = "Карта: Секунду..."
				PlayersServerLabel["text"] = "Игроков: Секунду..."
				WaveServerLabel["text"] = "Волна: Секунду..."
				VersionServerLabel["text"] = "Версия ядра: Секунду..."
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
Thread(target = HandlerComboBoxLS, args = (), daemon = True).start()

# Конец
root.mainloop()
operation.TimeUpdate = False