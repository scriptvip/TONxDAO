import asyncio, websockets, json, time
from concurrent.futures import ThreadPoolExecutor
from src.core import *
from src.table import LiveTable

class TONxDAO_Miner:
    def __init__(self, tokens):
        self.tokens = tokens
        self.user_dao = [None]*len(tokens)
        self.socket_tokens = [None]*len(tokens)
        self.counter = [0]*len(tokens)
        self.info = [{
            'name': '~~~',
            'profit': '~~~',
            'coins': '~~~',
            'energy': '~~~'
        } for _ in range(len(tokens))]
    
    
    def apply_changes(self, account_index, msg):
        if 'rpc' not in msg:return
        self.info[account_index]['energy'] = msg['rpc']['data']['energy']
        self.info[account_index]['coins'] = msg['rpc']['data']['coins']
        self.info[account_index]['profit'] = msg['rpc']['data']['dao_coins']

    def auth_message(self, account_index):
        self.counter[account_index] += 1
        return json.dumps({
            "connect": {
                "token": self.socket_tokens[account_index],
                "name": "js"
            },
            "id": self.counter[account_index]
        })
    def click_message(self, account_index):
        self.counter[account_index] += 1
        return json.dumps({
            "publish": {
                "channel": f"dao:{self.user_dao[account_index]['id']}",
                "data": {}
            },
            "id": self.counter[account_index]
        })

    def display_message(self, account_index):
        self.counter[account_index] += 1
        return json.dumps({
            "rpc":{
                "method":"sync",
                "data": {}
            },
            "id": self.counter[account_index]
        })
    
    async def start_async_mining(self, account_index):
        uri = 'wss://ws.production.tonxdao.app/ws'
        async with websockets.connect(uri) as websocket:
            # print("connected")
            while True:
                await websocket.send(self.auth_message(account_index))

                response = await websocket.recv()

                await websocket.send(self.click_message(account_index))

                time.sleep(config('delay_in_sending_message', .02))

                for _ in range(config('number_of_display_message', 2)):
                    await websocket.send(self.display_message(account_index))
                    response = await websocket.recv()
                    self.apply_changes(account_index, json.loads(response))
                    
    def run_websocket(self, account_index):
        asyncio.run(self.start_async_mining(account_index))
                

    def __mining(self):
        
        while True:
            try:
                with ThreadPoolExecutor(max_workers=len(self.tokens)) as executor:
                    futures = [executor.submit(self.run_websocket, account_index) for account_index in range(len(self.tokens))]
                    for future in futures:
                        future.result() 
                input()
            except KeyboardInterrupt:
                break
            except Exception as E:
                # print(E)
                pass
    
    def start_mining(self):
        
        
        # get dao for all accounts
        for i in range(len(self.tokens)):
            self.user_dao[i] = get_user_dao(self.tokens[i])
            time.sleep(1)
        
        # get socket tokens, username
        for i in range(len(self.tokens)):
            self.socket_tokens[i] = get_token(self.tokens[i])
            self.info[i]['name'] = get_username(self.tokens[i])
            time.sleep(1)
        
        self.__mining()

if __name__ == '__main__':
    banner()
    try:
        tokens = open('tokens.txt').read().strip().split('\n')
        
        TONxDAO = TONxDAO_Miner(tokens)
        
        Table = LiveTable(TONxDAO)

        Table.start()

        TONxDAO.start_mining()

        Table.stop()

        print("Exiting !")
    
    except KeyboardInterrupt:
        Table.stop()
        print("Exiting !")
        exit(0)
    