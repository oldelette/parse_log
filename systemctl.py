import logging
import subprocess
import sys
from dataclasses import dataclass, field


@dataclass
class SystemdService:
    """A systemd service object with methods to check it's activity, and to stop() and start() it."""

    service: str
    sudo_password: str = field(repr=False, init=False, default="xxxx")

    def runsudo(self):
        sudoer = subprocess.Popen(["echo", self.sudo_password], stdout=subprocess.PIPE)
        return sudoer.stdout

    def is_active(self) -> bool:
        """Return True if systemd service is running"""
        cmd = f"systemctl status {self.service}.service"
        completed = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if completed.stdout:
            print(
                completed.stdout.decode("utf-8"),
            )
            return any(
                [
                    True if "Active:" and "active (running)" in line else False
                    for line in completed.stdout.decode("utf-8").splitlines()
                ]
            )

        elif completed.stderr:
            print(
                completed.stderr.decode("utf-8"),
            )
            return False

    def stop(self) -> bool:
        """ Stop systemd service."""
        cmd = f"systemctl stop {self.service}.service".split()
        completed = subprocess.run(
            ["sudo", "-S"] + cmd,
            stdin=self.runsudo(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.stderr:
            print(completed.stderr.decode("utf-8"))
            return False
        print(f"stop {self.service} success")
        return True
        # except subprocess.CalledProcessError as err:
        #     print( 'ERROR:', err )

    def start(self) -> bool:
        """ Start systemd service."""
        cmd = f"systemctl start {self.service}.service".split()
        # print(cmd1.stdout,"---",self.runsudo())
        completed = subprocess.run(
            ["sudo", "-S"] + cmd,
            stdin=self.runsudo(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.stderr:
            print(completed.stderr.decode("utf-8"))
            return False
        print(f"start {self.service} success")
        return True

    def restart(self) -> bool:
        """ Restart systemd service."""
        cmd = f"systemctl restart {self.service}.service".split()
        completed = subprocess.run(
            ["sudo", "-S"] + cmd,
            stdin=self.runsudo(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.stderr:
            print(completed.stderr.decode("utf-8"))
            return False
        print(f"restart {self.service} success")
        return True


if __name__ == "__main__":

    monitor = SystemdService(sys.argv[1])
    monitor.start()
    # monitor.is_active()
    # monitor.stop()
    # monitor.restart()