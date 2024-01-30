from web3 import Web3
from json import load
from eth_account import Account
import json
import threading
import random
import sys
import tkinter as tk
from tkinter import messagebox

settings = load(open('settings.json'))
show_scan = settings['SHOW SCANNING']
scanning = True

# Loads the custom node
if 'wss' in settings['NODE'] or 'ws' in settings['NODE']:
    web3 = Web3(Web3.WebsocketProvider(settings['NODE']))
else:
    web3 = Web3(Web3.HTTPProvider(settings['NODE']))


def check_balance(wallet):
    try:
        balance = web3.eth.get_balance(wallet)
    except Exception as e:
        print(e)
        balance = 0
    return balance


def get_address(private):
    acct = Account.from_key(private).address
    return acct


def generate_random_key():
    choice = '1234567890abcdef'
    key = ''
    for x in range(0, 64):
        key = key + random.choice(choice)
    return key


def check_account():
    global scanning
    private_key = generate_random_key()
    wallet_address = get_address(private_key)
    balance = check_balance(wallet_address)

    if balance != 0:
        wallets = load(open('wallets.json'))

        def create_data():
            new_data = {}
            path = "./"
            filename = 'wallets.json'

            def write_to_json_file(path2, file_name, data2):
                file_path_name_wext = './' + path2 + '/' + file_name
                with open(file_path_name_wext, 'w') as fp:
                    json.dump(data2, fp, indent=2)

            new_data['WALLET ADDRESS'] = wallet_address
            new_data['PRIVATE KEY'] = private_key
            new_data['BALANCE'] = str(web3.from_wei(balance, 'ether'))
            wallets.append(new_data)
            write_to_json_file(path, filename, wallets)

        print('BALANCE DETECTED! SAVING WALLET')
        create_data()
        tk.messagebox.showinfo('Success', 'WALLET WITH BALANCE DETECTED!')
        scanning = False
        sys.exit()

    else:
        if show_scan == 'true':
            print(wallet_address + ' NO BALANCE | SCANNING AGAIN')


print('ETHEREUM WALLET MINER - AUSTIN-JS')
input('Press enter to start mining')
if show_scan != 'true':
    print('\nMining started!')

speed = int(settings['SPEED'])

while scanning:
    threads = []
    for i in range(speed):
        t = threading.Thread(target=check_account, daemon=True)
        threads.append(t)

    for i in range(speed):
        threads[i].start()

    for i in range(speed):
        threads[i].join()
