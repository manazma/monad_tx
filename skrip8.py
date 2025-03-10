import os
import random
import time
import logging
from web3 import Web3
from dotenv import load_dotenv

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Watermark
WATERMARK = """


███╗░░░███╗░█████╗░███╗░░██╗░█████╗░███████╗███╗░░░███╗░█████╗░
████╗░████║██╔══██╗████╗░██║██╔══██╗╚════██║████╗░████║██╔══██╗
██╔████╔██║███████║██╔██╗██║███████║░░███╔═╝██╔████╔██║███████║
██║╚██╔╝██║██╔══██║██║╚████║██╔══██║██╔══╝░░██║╚██╔╝██║██╔══██║
██║░╚═╝░██║██║░░██║██║░╚███║██║░░██║███████╗██║░╚═╝░██║██║░░██║
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝╚══════╝╚═╝░░░░░╚═╝╚═╝░░╚═╝  

🚀 Script by: @MEIMEIZK 🚀
"""

print(WATERMARK)

# Load environment variables dari .env
load_dotenv()

# Konfigurasi RPC Monad Testnet
RPC_URL = "https://testnet-rpc.monad.xyz/"
web3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={'timeout': 60}))

if web3.is_connected():
    logging.info("Berhasil terhubung ke RPC Monad Testnet!")
else:
    logging.error("Gagal terhubung ke RPC Monad Testnet!")
    exit()

# Ambil private key dari .env
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    logging.error("PRIVATE_KEY tidak ditemukan di .env!")
    exit()

WALLET_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY).address
logging.info(f"Wallet Address: {WALLET_ADDRESS}")

# Konversi alamat ke checksum
MAGMA_STAKING_CONTRACT = Web3.to_checksum_address("0x2c9C959516e9AAEdB2C748224a41249202ca8BE7")
WMONAD_CONTRACT = Web3.to_checksum_address("0x760AfE86e5de5fa0Ee542fc7B7B713e1c5425701")

# ABI untuk kontrak
MAGMA_STAKING_ABI = '[{"inputs":[],"name":"depositMon","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdrawMon","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
WMONAD_ABI = '[{"inputs":[],"name":"deposit","outputs":[],"stateMutability":"payable","type":"function"}]'

# Inisialisasi kontrak
staking_contract = web3.eth.contract(address=MAGMA_STAKING_CONTRACT, abi=MAGMA_STAKING_ABI)
WMONAD_contract = web3.eth.contract(address=WMONAD_CONTRACT, abi=WMONAD_ABI)

def get_mon_balance():
    return web3.eth.get_balance(WALLET_ADDRESS) / 10**18

def human_like_delay():
    delay = random.uniform(10, 31)
    logging.info(f"Menunggu {delay:.2f} detik sebelum transaksi berikutnya...")
    time.sleep(delay)

def stake_mon():
    try:
        amount_wei = web3.to_wei(random.uniform(0.01, 0.05), 'ether')
        tx = staking_contract.functions.depositMon().build_transaction({
            'from': WALLET_ADDRESS,
            'value': amount_wei,
            'gas': random.randint(100000, 150000),
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(WALLET_ADDRESS)
        })
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        logging.info(f"Staking berhasil! TX Hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        logging.error(f"Gagal staking: {str(e)}")
    human_like_delay()

def unstake_mon():
    try:
        amount_wei = web3.to_wei(random.uniform(0.001, 0.005), 'ether')
        tx = staking_contract.functions.withdrawMon(amount_wei).build_transaction({
            'from': WALLET_ADDRESS,
            'gas': random.randint(100000, 150000),
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(WALLET_ADDRESS)
        })
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        logging.info(f"Unstake berhasil! TX Hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        logging.error(f"Gagal unstake: {str(e)}")
    human_like_delay()

def wrap_monad():
    try:
        amount = random.uniform(0.0001, 0.01)  # Random di bawah 0.001 MONAD
        logging.info(f"Mencoba melakukan wrap {amount:.6f} MONAD ke wMONAD...")

        tx = WMONAD_contract.functions.deposit().build_transaction({
            'from': WALLET_ADDRESS,
            'value': web3.to_wei(amount, 'ether'),
            'gas': random.randint(90000, 110000),  # Variasi gas agar lebih realistis
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(WALLET_ADDRESS)
        })

        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        logging.info(f"wMONAD berhasil! TX Hash: {web3.to_hex(tx_hash)}")

    except Exception as e:
        logging.error(f"Gagal melakukan wrap: {str(e)}")

    human_like_delay()

# Loop transaksi otomatis
tx_counter = 0  # Inisialisasi variabel hitungan transaksi

while True:
    mon_balance = get_mon_balance()
    logging.info(f"Saldo MON saat ini: {mon_balance:.5f} MON")

    if mon_balance <= 0.2:
        logging.warning("Saldo MON kurang dari 0.2 MON, menghentikan semua transaksi!")
        break

    # Pilih transaksi secara acak
    random.choice([stake_mon, unstake_mon, wrap_monad])()
    tx_counter += 1  

    # Atur jeda panjang setelah beberapa transaksi
    if tx_counter >= random.randint(10, 15):
        sleep_time = random.randint(28800, 86400)  # Jeda antara 8-24 jam
        logging.info(f"Jeda panjang selama {sleep_time / 3600:.2f} jam...")
        time.sleep(sleep_time)
        tx_counter = 0  # Reset tx_counter setelah jeda panjang
