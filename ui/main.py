import sys
import time

from rich.live import Live
from rich.table import Table
from rich.console import Console

from util.time import format_second_to_str


class UI:
    def get_bus_color(self, bus):
        time_remained = bus["TimeRemained"]
        color = "red"
        if time_remained < 300:
            color = "green"
        elif time_remained < 600:
            color = "yellow"
        elif time_remained < 900:
            color = "bright_red"

        return color

    def generate_bus_row(self, bus):
        time_remained = bus["TimeRemained"]
        color = self.get_bus_color(bus)
        return (
            f'[{color}]{bus["Fleet"]}',
            f'[{color}]{bus["FleetCode"]}',
            f'[{color}]{bus["BienKiemSoat"]}',
            f'[{color}]{bus["PartRemained"]}',
            f"[{color}]{format_second_to_str(time_remained)}",
        )

    def generate_buses_table(self, buses):
        if buses is None:
            sys.exit("No bus is working right now!")

        table = Table(title="Realtime bus tracking", min_width=120)
        table.add_column("Số xe")
        table.add_column("Tên xe")
        table.add_column("Biển kiếm soát")
        table.add_column("Khoách cách (m)")
        table.add_column("Thời gian")
        for bus in buses:
            bus_row = self.generate_bus_row(bus)
            table.add_row(*bus_row)

        return table

    def live_update_buses_table(self, buses, get_update_data_func):
        table = self.generate_buses_table(buses)
        with Live(table, refresh_per_second=4) as live:
            while True:
                try:
                    time.sleep(1)
                    _buses = get_update_data_func()
                    table = self.generate_buses_table(_buses)
                    live.update(table)
                except KeyboardInterrupt:
                    print("End.")
                    break

    def render(self, place, buses, get_update_data_func):
        console = Console()
        console.print(f'[yellow]Điểm dừng : [green]{place["Name"]}')
        print()

        self.live_update_buses_table(buses, get_update_data_func)
