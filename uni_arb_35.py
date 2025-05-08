from web3 import Web3
import time
import random

# 跨链eth
AMOUNT_ETH = 1
# 跨链次数
TIMES = 99999

UNI_RPC_URL = "https://unichain-sepolia.drpc.org"
ARB_RPC_URL = "https://sepolia-rollup.arbitrum.io/rpc"

UNI_TO_ARB_CONTRACT = "0x1cEAb5967E5f078Fa0FEC3DFfD0394Af1fEeBCC9"
ARB_TO_UNI_CONTRACT = "0x22B65d0B9b59af4D3Ed59F18b9Ad53f5F4908B54"

UNI_TO_ARB_BASE_DATA = "0x56591d5961726274000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000{address}0000000000000000000000000000000000000000000000000de08e51f0c04e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000de0b6b3a7640000"
ARB_TO_UNI_BASE_DATA = "0x56591d59756e6974000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000{address}0000000000000000000000000000000000000000000000000de06a4dded38400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000de0b6b3a7640000"

w3_uni = Web3(Web3.HTTPProvider(UNI_RPC_URL))
w3_arb = Web3(Web3.HTTPProvider(ARB_RPC_URL))

if not w3_uni.is_connected():
    raise Exception("无法连接到 UNI 测试网")
if not w3_arb.is_connected():
    raise Exception("无法连接到 ARB 测试网")

def load_private_keys():
    with open("address.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def bridge_uni_to_arb(amount_eth, account):
    try:
        amount_wei = w3_uni.to_wei(amount_eth, 'ether')
        nonce = w3_uni.eth.get_transaction_count(account.address)
        data = UNI_TO_ARB_BASE_DATA.format(address=account.address[2:])
        
        tx = {
            'from': account.address,
            'to': UNI_TO_ARB_CONTRACT,
            'value': amount_wei,
            'nonce': nonce,
            'gas': 400000,
            'gasPrice': w3_uni.to_wei(0.16, 'gwei'), #降低gas，之前设置太高
            'chainId': 1301,
            'data': data
        }
        print(f"UNI -> ARB: Sending {amount_eth} ETH from {account.address}")
        signed_tx = w3_uni.eth.account.sign_transaction(tx, account.key)  # 修改为 account.key
        tx_hash = w3_uni.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"UNI -> ARB 交易已发送，交易哈希: {w3_uni.to_hex(tx_hash)}")
        tx_receipt = w3_uni.eth.wait_for_transaction_receipt(tx_hash)
        print(f"交易已确认，区块号: {tx_receipt.blockNumber}")
        return True
    except Exception as e:
        print(f"UNI -> ARB 跨链失败，错误: {e}")
        return False

def bridge_arb_to_uni(amount_eth, account):
    try:
        amount_wei = w3_arb.to_wei(amount_eth, 'ether')
        nonce = w3_arb.eth.get_transaction_count(account.address)
        data = ARB_TO_UNI_BASE_DATA.format(address=account.address[2:])
        
        tx = {
            'from': account.address,
            'to': ARB_TO_UNI_CONTRACT,
            'value': amount_wei,
            'nonce': nonce,
            'gas': 400000,
            'gasPrice': w3_arb.to_wei(0.1, 'gwei'),
            'chainId': 421614,
            'data': data
        }
        print(f"ARB -> UNI: Sending {amount_eth} ETH from {account.address}")
        signed_tx = w3_arb.eth.account.sign_transaction(tx, account.key)  # 修改为 account.key
        tx_hash = w3_arb.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"ARB -> UNI 交易已发送，交易哈希: {w3_arb.to_hex(tx_hash)}")
        tx_receipt = w3_arb.eth.wait_for_transaction_receipt(tx_hash)
        print(f"交易已确认，区块号: {tx_receipt.blockNumber}")
        return True
    except Exception as e:
        print(f"ARB -> UNI 跨链失败，错误: {e}")
        return False

def main():
    private_keys = load_private_keys()
    accounts = [w3_uni.eth.account.from_key(pk) for pk in private_keys]
    
    print(f"加载了 {len(accounts)} 个账户")
    
    # 无限循环，每轮结束后等待 10 分钟
    round_count = 0
    while True:
        round_count += 1
        print(f"\n第 {round_count} 轮跨链操作开始，当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"开始 UNI 和 ARB 互跨 {TIMES} 次，每次 {AMOUNT_ETH} ETH")
        
        for i in range(TIMES):
            print(f"\n第 {i+1} 次互跨：")
            for idx, account in enumerate(accounts):
                # UNI -> ARB
                bridge_uni_to_arb(AMOUNT_ETH, account)
                
                #delay = random.uniform(1, 2)
                #print(f"等待 {delay:.2f} 秒后进行 ARB -> UNI 跨链...")
                #time.sleep(delay)
                
                # ARB -> UNI
                bridge_arb_to_uni(AMOUNT_ETH, account)
   
            print(f"第 {i+1} 次互跨完成")
        
        print(f"\n第 {round_count} 轮跨链操作完成，等待1分钟后开始下一轮...")
        time.sleep(1 * 60)  # 等待 1 分钟，循环一轮时间可自定义修改

if __name__ == "__main__":
    main()
