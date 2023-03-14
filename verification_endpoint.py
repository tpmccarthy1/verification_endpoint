from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/verify', methods=['GET','POST'])
def verify():
    content = request.get_json(silent=True)
    sig = content["sig"][2:]
    payload = content["payload"]
    result = False
    if (payload["platform"] == 'Ethereum'):
        if eth_account.Account.recover_message(json.dumps(payload).encode('utf-8'),signature=bytes.fromhex(sig).hex()) == payload["pk"]:
            result = True
    if (payload["platform"] == 'Algorand'):
        if algosdk.util.verify_bytes(json.dumps(payload).encode('utf-8'),sig,payload["pk"]):
            result = True


    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
