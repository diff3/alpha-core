from multiprocessing import Process

import colorama

from sys import platform

from game.realm import RealmManager
from game.world import WorldManager
from utils.ConfigManager import config
from database.realm.RealmDatabaseManager import RealmDatabaseManager
from utils.Logger import Logger


if __name__ == '__main__':
    # Initialize colorama
    colorama.init()

    if platform != 'win32':
        from signal import signal, SIGPIPE, SIG_DFL
        # https://stackoverflow.com/a/30091579
        signal(SIGPIPE, SIG_DFL)

    login_process = Process(target=RealmManager.LoginServerSessionHandler.start)
    login_process.start()

    proxy_process = Process(target=RealmManager.ProxyServerSessionHandler.start)
    proxy_process.start()

    world_process = Process(target=WorldManager.WorldServerSessionHandler.start)
    world_process.start()
