from watchdog.observers import Observer
from watchdog.events import *
import time
from atftp import Parser
from dhcpleases import Dhcp


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print(
                "directory moved from {0} to {1}".format(
                    event.src_path, event.dest_path
                )
            )
        else:
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))
            monitor_atftp()


from switch.provision import Provision


def monitor_atftp():
    parser = Parser("/var/log/atftpd.log")
    # parser = Parser("/tmp/atftpd.log")
    res = parser.fliter_service()
    # res = parser.get_last_line()
    print(res)
    dhcpdic = Dhcp("/var/lib/dhcp/dhcpd.leases").get_history()
    # print(dhcpdic)
    # print(aa.get_history())
    if res:
        new = (
            Provision(res[0]["ip"], dhcpdic[res[0]["ip"]], True)
            if res[0]["success"]
            else Provision(res[0]["ip"], dhcpdic[res[0]["ip"]], False)
        )
        # if res[0]['success']:
        #    new = Provision(res[0]['ip'],dhcpdic[res[0]['ip']],True)
        # new = Provision(res[0]['ip'],list(dhcpdic.keys())[list(dhcpdic.values()).index(res[0]['ip'])])
        print("new state:", new)
    print("--" * 20)


if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    # observer.schedule(event_handler, "/tmp/atftpd.log", True)
    observer.schedule(event_handler, "/var/log/atftpd.log", True)
    observer.start()
    print("test")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()