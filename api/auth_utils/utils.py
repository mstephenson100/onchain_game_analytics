import os
import sys
import pymysql
import warnings
import traceback
import configparser
import time
import jwt
import uuid
from datetime import datetime, timedelta
from eth_account.messages import encode_defunct
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.account.account import Account
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.utils.typed_data import TypedData
from starknet_py.contract import Contract

from hashlib import pbkdf2_hmac

filename = __file__
config_path = filename.split('/')[3]
config_file = "/home/bios/" + config_path + "/api.conf"

if os.path.exists(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    auth_db_user = config.get('authentication', 'db_user')
    auth_db_password = config.get('authentication', 'db_password')
    auth_db = config.get('authentication', 'db')
    jwt_secret_key = config.get('authentication', 'jwt_secret_key')
    network = config.get('blockchain', 'network')
    chain_id = config.get('blockchain', 'chain_id')
    pathfinder_url = config.get('blockchain', 'pathfinder_url')

else:
    raise Exception(config_file)


def generate_salt():
    salt = os.urandom(16)
    return salt.hex()


def generate_hash(wallet, signature_salt):
    password_hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(wallet, "utf-8"),
        b"%b" % bytes(signature_salt, "utf-8"),
        10000,
    )
    return password_hash.hex()


def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["wallet"]) <= 255 and len(kwargs["signature"]) <= 255:
            return True
        else:
            return False


def verifySignature(wallet, signature, nonce):

    w3 = Web3(Web3.HTTPProvider(""))
    mesage= encode_defunct(text=nonce)
    address = w3.eth.account.recover_message(mesage,signature=HexBytes(signature))
    print(address)
    return address


def getPublicKey(wallet):

    starknet = Starknet()
    account_info = starknet.account_info(wallet_address)
    public_key = account_info.public_key
    print(public_key)


def db_write(sql):

    con = pymysql.connect("127.0.0.1", auth_db_user, auth_db_password, auth_db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)

    cur.close()
    con.close()

    return True

def generateNonce(wallet):

    nonce_uuid = str(uuid.uuid4())
    nonce_hex = nonce_uuid.replace("-", "")
    nonce_hex = "0x" + nonce_hex
    wallet_int = int(wallet, 16)
    typed_data = generateTypedData(wallet, nonce_hex)
    data = TypedData.from_dict(typed_data)
    message_hash = data.message_hash(wallet_int)
    cacheAddress(wallet, nonce_hex, message_hash)
    return typed_data


def generateTypedData(wallet, nonce_hex):

    typed_data = {
        "types": {
            "StarkNetDomain": [
                { "name": "name", "type": "string" },
                { "name": "version", "type": "string" },
                { "name": "chainId", "type": "uint256" }
            ],
            "Message": [
                { "name": "from", "type": "address" },
                { "name": "content", "type": "string" }
            ]
        },
        "domain": {
            "name": "app_name",
            "version": "1",
            "chainId": chain_id
        },
        "primaryType": "Message",
        "message": {
            "from": wallet,
            "content": nonce_hex
        }
    }

    return typed_data


def checkNonce(wallet):

    count = 0
    con = pymysql.connect("127.0.0.1", auth_db_user, auth_db_password, auth_db)
    sql = ("SELECT COUNT(*) FROM nonce WHERE wallet = '%s'" % wallet)
    print(sql)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    return count


def getMessageHash(wallet):

    message_hash = None
    con = pymysql.connect("127.0.0.1", auth_db_user, auth_db_password, auth_db)
    sql = ("SELECT message_hash FROM nonce WHERE wallet = '%s'" % wallet)
    print(sql)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            return None
        else:
            message_hash=result[0]

    return message_hash


def getLogin(wallet):

    count = 0
    con = pymysql.connect("127.0.0.1", auth_db_user, auth_db_password, auth_db)
    sql = ("SELECT COUNT(*) FROM users WHERE wallet = '%s'" % wallet)
    print(sql)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    return count


def getWallet(wallet_id):

    wallet = None
    con = pymysql.connect("127.0.0.1", auth_db_user, auth_db_password, auth_db)
    sql = ("SELECT wallet FROM users WHERE id = %s" % wallet_id)
    print(sql)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            return wallet
        else:
            wallet=result[0]

    return wallet

    
def cacheAddress(wallet, nonce, message_hash):

    con = pymysql.connect("127.0.0.1", auth_db_user, auth_db_password, auth_db)
    check_nonce = checkNonce(wallet)
    if check_nonce == 0:
        sql = ("INSERT INTO nonce (wallet, nonce, message_hash) VALUES ('%s', '%s', '%s')" % (wallet, nonce, message_hash))
    else:
        sql = ("UPDATE nonce SET nonce = '%s', message_hash = '%s' WHERE wallet = '%s'" % (nonce, message_hash, wallet))

    print(sql) 
    db_write(sql)


def db_read(sql):

    content = []
    print(sql)
    con = pymysql.connect("127.0.0.1", auth_db_user, auth_db_password, auth_db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        for entry in rows:
            user_id = entry[0]
            wallet = entry[1]
            signature_salt = entry[2]
            signature_hash = entry[3]
            content.append({"id": user_id, "wallet": wallet, "signature_salt": signature_salt, "signature_hash": signature_hash})


    cur.close()
    con.close()
    return content


def generate_jwt_token(content):
    encoded_content = jwt.encode(content, jwt_secret_key, algorithm="HS256")
    token = str(encoded_content)
    return token


def validate_user(wallet, signature):
    
    sql = ("SELECT * FROM users WHERE wallet = '%s'" % wallet)
    print(sql)
    current_user = db_read(sql)

    if len(current_user) == 1:
        saved_signature_hash = current_user[0]["signature_hash"]
        saved_signature_salt = current_user[0]["signature_salt"]
        signature_hash = generate_hash(wallet, saved_signature_salt)

        if signature_hash == saved_signature_hash:
            user_id = current_user[0]["id"]
            expiration = datetime.now() + timedelta(days=3)
            jwt_token = generate_jwt_token({"id": user_id, "exp": expiration})
            return jwt_token
        else:
            return False

    else:
        return False


async def verifyArgentx(contract_address, user_signature, message_hash):

    node_url = 'http://176.9.126.173:9545'
    full_node_client = FullNodeClient(node_url=node_url)
    message_hash = int(message_hash)

    try:
        print("Verifying argentx %s with message_hash %s and signature %s" % (contract_address, message_hash, user_signature))
        contract = await Contract.from_address(contract_address, full_node_client)
        response = await contract.functions["is_valid_signature"].call(message_hash, user_signature)
        result = response[0]

    except:
        print("Verifying argentx %s with message_hash %s and signature %s failed" % (contract_address, message_hash, user_signature))
        result = False

    if result == 370462705988:
        result = True
    else:
        result = False

    return result


async def verifyBraavos(contract_address, user_signature, message_hash):

    node_url = 'http://176.9.126.173:9545'
    full_node_client = FullNodeClient(node_url=node_url)
    message_hash = int(message_hash)

    if len(user_signature) == 3:
        try:
            print("Verifying braavos %s with message_hash %s and signature %s" % (contract_address, message_hash, user_signature))
            contract = await Contract.from_address(contract_address, full_node_client)
            response = await contract.functions["is_valid_signature"].call(message_hash, user_signature)
            result = response[0]

        except:
            print("Verifying braavos %s with message_hash %s and signature %s failed" % (contract_address, message_hash, user_signature))
            result = False

        if result == 370462705988:
            result = True
        else:
            result = False

    else:
        try:
            print("Verifying braavos %s with message_hash %s and signature %s" % (contract_address, message_hash, user_signature))
            contract = await Contract.from_address(contract_address, full_node_client, proxy_config=True)
            response = await contract.functions["is_valid_signature"].call(message_hash, user_signature)
            result = response.is_valid

        except:
            print("Verifying braavos %s with message_hash %s and signature %s failed" % (contract_address, message_hash, user_signature))
            result = False

        if result == 1:
            result = True
        else:
            result = False

    return result

