from threading import Thread
from configparser import ConfigParser
from tornado.web import Application
from tornado.ioloop import IOLoop
from servidor.common.controllers import Error404Handler
from servidor.routes import get_handlers
from servidor.database import connection

import os
import sys
import re
import platform
import psutil
import schedule
import time
import asyncio


def main():
    create_app()


def vaciar_puerto(puerto):
    pid = ""

    if platform.system() == "Windows":
        output_command = os.popen("netstat -noa").readlines()
        for line in output_command:
            if len(re.findall(puerto, line)) > 0:
                print(line)
                pid = (list(line.split(" "))).pop()
                break

        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                processName = proc.name()
                processID = proc.pid

                try:
                    if processID == int(pid) and processName == "python.exe":
                        print(processName, ' ::: ', processID)
                        endProcess = "taskkill /F /PID " + pid
                        os.system(endProcess)
                        break
                except:
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass


def get_settings(config):
    return {
        "template_path": os.path.join(os.getcwd(), 'servidor'),
        "cookie_secret": config["Server"]["cookie_secret"],
        "login_url": "/inicio",
        "xsrf_cookies": True,
        'autoreload': True,
        "debug": True
    }


def launch_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


def create_app():
    config = ConfigParser()
    config.read('settings.ini')
    connection.db_url = config['Database']['url']
    puerto = config['Server']['port']
    address = config['Server']['address']
    vaciar_puerto(puerto)
    port = int(os.getenv('PORT', puerto))

    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    settings = get_settings(config)
    Thread(target=launch_schedule).start()
    app = Application(get_handlers(), **settings, default_handler_class=Error404Handler)

    # app.listen(int(puerto), address)
    app.listen(int(port), address)
    print('Ejecutando servidor en http://'+config['Server']['address']+':'+config['Server']['port'])
    IOLoop.instance().start()


if __name__ == "__main__":
    sys.exit(int(main() or 0))
