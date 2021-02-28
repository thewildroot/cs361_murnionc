from adresses import generate_addresses
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/get', methods=['GET'])
def get():
    state = request.args.get("state").lower()
    number = int(request.args.get("number"))

    if not state:
        return "Error state parameter missing"
    if not number:
        return "Error number parameter missing"

    addresses = generate_addresses(state, number)
    address_lines = []

    for address in addresses:
        address_lines.append(address["output_content_value"])

    response = {"state": state,
                "number": number,
                "addresses": address_lines}

    return jsonify(response)


@app.route('/')
def home():
    return "Wrong format, please use the following: /get?state=ak&number=100"


if __name__ == "__main__":
    app.run(port=5002)
