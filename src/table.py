
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.box import ASCII_DOUBLE_HEAD
from time import sleep
import threading


class LiveTable:

    def __init__(self, TONxDAO):
        self.THREAD = None
        self.is_running = 0
        self.TONxDAO_Miner = TONxDAO
        self.console = Console()

    
    def create_table(self):
        table = Table(title="TONxDAO Miner By Abdo Sleem", box=ASCII_DOUBLE_HEAD)

        table.add_column("ID", style="cyan", no_wrap=True, justify='center', width=3)
        table.add_column("Account", style="magenta", justify='center', width=20)
        table.add_column("Profit", style="green", justify='center', width=11)
        table.add_column("Coins", style="green", justify='center', width=11)
        table.add_column("Energy", style="green", justify='center', width=7)

        for i in range(len(self.TONxDAO_Miner.tokens)):
            table.add_row(str(i+1), str(self.TONxDAO_Miner.info[i]['name']), str(self.TONxDAO_Miner.info[i]['coins']), str(self.TONxDAO_Miner.info[i]['energy']))
        return table

    def Loop(self):
        with Live(console=self.console, refresh_per_second=4) as live:
            while True:
                if not self.is_running:break
                table = self.create_table()
                live.update(table)
                sleep(0.2)
    def start(self):
        self.is_running = 1
        self.THREAD = threading.Thread(target=self.Loop)
        self.THREAD.start()
    
    def stop(self):
        self.is_running = 0