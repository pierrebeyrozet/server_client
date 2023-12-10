from multiprocessing.connection import Client
import time
from datetime import datetime, timedelta
import threading


class Scheduler:
    def __init__(self):
        self.strats = {'strat1': {'port': 6000, 'pwd': 'pwd1', 'conn': None},
                       'strat2': {'port': 6001, 'pwd': 'pwd2', 'conn': None},
                       'strat3': {'port': 6002, 'pwd': 'pwd3', 'conn': None}}
        self.connection_status = {'strat1': {'is_open': False, 'has_timeout': False, 'pending': False, 'connection': object},
                                  'strat2': {'is_open': False, 'has_timeout': False, 'pending': False, 'connection': object},
                                  'strat3': {'is_open': False, 'has_timeout': False, 'pending': False, 'connection': object}}
        self.freq_minute = 1
        self.delay_second = 3

    def run(self):
        while True:
            print('waiting until next trigger')
            self.trigger_cagg()
            print('sending trigger to all servers listening')
            self.trigger_signal_servers()

    def trigger_signal_servers(self):
        for signal_name, conn_status in self.connection_status.items():
            if conn_status['is_open']:
                print(f'a valid connection has been found for signal {signal_name}')
                conn_status['connection'].send('cagg has been refreshed')
                a=0
            # if self.open_connections['strat1']['is_open']:
            #     print('a valid connection has been found')
            #     # send some message to server strats at the right moment
            #     time.sleep(5)
            # else:
            #     if self.open_connections['strat1']['has_timeout']:
            #         pass
            #     else:
            #         if self.open_connections['strat1']['pending']:
            #             pass
            #         else:
            #             threading.Thread(target=self.connect_to_server, args=('strat1',)).start()

    def trigger_cagg(self):
        time.sleep(self.get_seconds_to_next_trigger() + self.delay_second)
        if self.is_time_to_trigger():
            print('calling cagg refresh to database')
            print(datetime.now())

    def init_connections(self):
        for signal_name, conn_status in self.connection_status.items():
            threading.Thread(target=self.connect_to_server, args=(signal_name,)).start()

    def is_time_to_trigger(self):
        utc_now = datetime.utcnow()
        if utc_now.minute % self.freq_minute == 0:
            return True
        else:
            return False

    @staticmethod
    def get_seconds_to_next_trigger():
        utc_now = datetime.utcnow()
        next_trigger = (utc_now+timedelta(minutes=1)).replace(microsecond=0, second=0)
        time_to_next_trigger = (next_trigger-utc_now).total_seconds()
        return time_to_next_trigger

    def connect_to_server(self, strat_name):
        self.connection_status[strat_name]['pending'] = True
        start_time = datetime.now()
        for i in range(1, 13):
            try:
                conn = Client(address=('localhost', self.strats[strat_name]['port']),
                              authkey=self.strats[strat_name]['pwd'].encode())
                self.connection_status[strat_name]['connection'] = conn
                self.connection_status[strat_name]['pending'] = False
                self.connection_status[strat_name]['is_open'] = True
                print(f'connection to {strat_name} established')
            except:
                if (datetime.now()-start_time).total_seconds() > 60:
                    print(f'connection to {strat_name} could not be established. exiting')
                    self.connection_status[strat_name]['pending'] = False
                    self.connection_status[strat_name]['has_timeout'] = True
                    break
                else:
                    print(f'connection to {strat_name} number {str(i)} failed. retrying in 5 sec')
                    time.sleep(5)


        return


if __name__ == '__main__':
    schd = Scheduler()
    schd.init_connections()
    schd.run()
