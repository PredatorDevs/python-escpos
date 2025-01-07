from flask import Flask, request, jsonify

from print_slip_cf import print_slip_cf
from print_slip_ccf import print_slip_ccf
from print_receipt import print_receipt

app = Flask(__name__)

@app.route('/print/slip/cf', methods=['POST'])
def handle_print_slip_cf():
    try:
        data = request.json
        if not data or 'header' not in data:
            return jsonify({"status": "error", "message": "El campo 'header' es obligatorio."}), 400

        print_slip_cf(data['header'], data['details'])
        
        return jsonify({"status": "success", "message": "Printing success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/print/slip/ccf', methods=['POST'])
def handle_print_slip_ccf():
    try:
        data = request.json
        if not data or 'header' not in data:
            return jsonify({"status": "error", "message": "El campo 'header' es obligatorio."}), 400

        print_slip_ccf(data['header'], data['details'])
        
        return jsonify({"status": "success", "message": "Printing success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/print/receipt/ticket', methods=['POST'])
def handle_print_receipt():
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "El campo 'text' es obligatorio."}), 400

        print_receipt(data['text'])
        return jsonify({"status": "success", "message": "Printing success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
  # Ejecutar el servidor en el puerto 5000
  app.run(host='127.0.0.1', port=5006)
