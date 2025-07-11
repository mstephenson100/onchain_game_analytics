from flask import Blueprint, request, Response, jsonify
from auth_utils import utils

authentication = Blueprint("authentication", __name__)

@authentication.route("/register", methods=["POST"])
async def register_user():

    print("request: %s" % request.json)
    user_wallet = request.json["wallet"]
    user_signature = request.json["signature"]
    account_type = request.json["account_type"]
    message_hash = utils.getMessageHash(user_wallet)
    if message_hash is None:
        return Response(status=400)

    if len(user_signature) == 2:
        old_user_signature = user_signature
        sig1 = int(user_signature[0])
        sig2 = int(user_signature[1])
        user_signature = [sig1, sig2]
    else:
        old_user_signature = user_signature
        sig1 = int(user_signature[0])
        sig2 = int(user_signature[1])
        sig3 = int(user_signature[2])
        user_signature = [sig1, sig2, sig3]

    print("old user_signature: %s" % old_user_signature)
    print("new_user_signature: %s" % user_signature)
    if account_type == 'argentx':
        verification = await utils.verifyArgentx(user_wallet, user_signature, message_hash)
    elif account_type == 'braavos':
        verification = await utils.verifyBraavos(user_wallet, user_signature, message_hash)
    else:
        return Response(status=409)

    if verification is True:
        signature_salt = utils.generate_salt()
        signature_hash = utils.generate_hash(user_wallet, signature_salt)

        user_exists = utils.getLogin(user_wallet)
        if user_exists > 0:
            sql = ("UPDATE users SET signature_salt = '%s', signature_hash = '%s' WHERE wallet = '%s'" % (signature_salt, signature_hash, user_wallet))
        else:
            sql = ("INSERT IGNORE INTO users (wallet, signature_salt, signature_hash) VALUES ('%s', '%s', '%s')" % (user_wallet, signature_salt, signature_hash))

        print(sql)
        write_response = utils.db_write(sql)
        if write_response is True:
            user_token = utils.validate_user(user_wallet, user_signature)
            print("user_token: %s" % user_token)
            if user_token:
                return jsonify({"jwt_token": user_token})
            else:
                return Response(status=401)

        else:
            return Response(status=409)

    else:
        return Response(status=400)


@authentication.route("/nonce", methods=["POST"])
def nonce():

    nonce = None
    print("request: %s" % request.json)
    wallet = request.json["wallet"]
    nonce = utils.generateNonce(wallet)
    if nonce is not None:
        return jsonify({"nonce": nonce})
    else:
        Response(status=401)

