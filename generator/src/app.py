#!flask/bin/python
import json
from flask import Flask, request, abort, jsonify
from generator.interface import generate_all_material
from generator.constants import logger
app = Flask(__name__)

@app.route('/generator/api/v1.0/generate', methods=['POST'])
def generate():
    try: 
        data = json.loads(request.data.decode())
        generate_all_material(data)
    except Exception as e:
        logger.error(str(e))
        abort(400)
    return jsonify({'result': "material generated"}), 201

if __name__ == '__main__':
    app.run(debug=True)

