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
    sig = content.get('sig')
    platform = content.get('payload').get('platform')
    pk = content.get('payload').get('pk')
    msg = content.get('payload').get('msg')
    print(msg)
    print(pk)
    print(platform)
    result = False
    if (platform == 'Ethereum'):
        if eth_account.Account.recover_message(msg,signature=sig.hex()) == pk:
            result = True
    elif (platform == 'Algorand'):
        if algosdk.util.verify_bytes(msg.encode('utf-8'),sig,pk):
            result = True

    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
