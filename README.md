安装支持
'''
pip install web3 eth_account

pip install --upgrade web3
'''
参数配置：只能修改私匙和互跨次数，跨链金额不能更改。

不懂代码请不要修改每次跨链的1.只修改私匙和次数。

默认循环一轮为10分钟，可以自定义为其他时间

支持批量多号刷SWAP，把私匙添加到address.txt,一行一个

PRIVATE_KEY = "0x1234567890" #填写私匙

AMOUNT_ETH = 1 # 每次跨链金额（单位：ETH）

TIMES = 9999 # 互跨来回次数

time.sleep(1 * 60) # 等待 1 分钟，循环时间可修改

1 uni_arb_35.py ARB <-> UNI 互SWAP刷奖励
python3 uni_arb_35.py
