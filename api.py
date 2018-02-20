from flask import Flask, jsonify
from crawler import get_this_cep, NotFoundException

app = Flask(__name__)


@app.route('/<cep_to_find>')
def cep_route(cep_to_find):

    try:
        cep_to_find = int(cep_to_find.replace('-', ''))
        cep_to_find = get_this_cep(cep_to_find)
        return jsonify(cep_to_find)

    except NotFoundException as ee:
        return jsonify({}), 400
    except Exception as ex:
        return ex, 500


if __name__ == "__main__":
    app.run(port=5560)