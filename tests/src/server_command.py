import psutil


def terminate_server():
    for i in psutil.process_iter():
        if i.name() == 'python3':
            if i.cmdline()[0] == 'python3' and i.cmdline()[1] == 'main.py':
                i.terminate()
