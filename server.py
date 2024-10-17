from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from check import get_check
from db import Base, Operation, Card, Settings

app = Flask(__name__)
CORS(app)

engines = {
    "spb": create_engine('sqlite:///spb.db'),
    "tinkoff": create_engine('sqlite:///tinkoff.db'),
    "sber": create_engine('sqlite:///sber.db'),
}

Session = sessionmaker()
sessions = {bank: Session(bind=engine) for bank, engine in engines.items()}


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)


def remove_sa_instance_state(data):
    if isinstance(data, dict):
        data.pop('_sa_instance_state', None)
    return data


@app.route('/<db_name>/get_check', methods=['POST'])
def get_check_server(db_name):
    data = request.json
    return get_check(db_name, data)


@app.route('/<db_name>/get_card_balance/<int:card_id>', methods=['GET'])
def get_card_balance(db_name, card_id):
    card = sessions[db_name].query(Card).filter_by(id=card_id).first()
    return jsonify({"balance": card.balance if card else None})


@app.route('/<db_name>/get_card/<int:card_id>', methods=['GET'])
def get_card(db_name, card_id):
    card = sessions[db_name].query(Card).filter_by(id=card_id).first()
    return jsonify(remove_sa_instance_state(card.__dict__) if card else {})


@app.route('/<db_name>/get_history', methods=['GET'])
def get_history(db_name):
    history = sessions[db_name].query(Operation).all()
    return jsonify({"history": [remove_sa_instance_state(op.__dict__) for op in history]})


@app.route('/<db_name>/insert_operation', methods=['POST'])
def insert_operation(db_name):
    data = request.json
    operation = Operation(**data)
    sessions[db_name].add(operation)
    sessions[db_name].commit()
    return jsonify({"success": True})


@app.route('/<db_name>/get_settings', methods=['GET'])
def get_settings(db_name):
    settings = sessions[db_name].query(Settings).first()
    return jsonify(remove_sa_instance_state(settings.__dict__) if settings else {})


@app.route('/<db_name>/operations', methods=['GET'])
def get_operations(db_name):
    operations = sessions[db_name].query(Operation).all()
    return jsonify([remove_sa_instance_state(op.__dict__) for op in operations])


@app.route('/<db_name>/operations', methods=['POST'])
def add_operation(db_name):
    from datetime import datetime

    data = request.json
    data['timestamp'] = datetime.fromisoformat(data['timestamp'])
    new_operation = Operation(**data)
    sessions[db_name].add(new_operation)
    sessions[db_name].commit()
    return jsonify({"success": True, "id": new_operation.id})


@app.route('/<db_name>/operations/<int:operation_id>', methods=['DELETE'])
def delete_operation(db_name, operation_id):
    operation = sessions[db_name].query(Operation).filter_by(id=operation_id).first()
    if operation:
        sessions[db_name].delete(operation)
        sessions[db_name].commit()
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Operation not found"}), 404


@app.route('/<db_name>/cards', methods=['GET'])
def get_cards(db_name):
    cards = sessions[db_name].query(Card).all()
    return jsonify([remove_sa_instance_state(card.__dict__) for card in cards])


@app.route('/<db_name>/cards', methods=['POST'])
def add_card(db_name):
    data = request.json
    new_card = Card(**data)
    sessions[db_name].add(new_card)
    sessions[db_name].commit()
    return jsonify({"success": True, "id": new_card.id})


@app.route('/<db_name>/cards/<int:card_id>', methods=['DELETE'])
def delete_card(db_name, card_id):
    card = sessions[db_name].query(Card).filter_by(id=card_id).first()
    if card:
        sessions[db_name].delete(card)
        sessions[db_name].commit()
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Card not found"}), 404


@app.route('/<db_name>/cards/<int:card_id>', methods=['PUT'])
def update_card(db_name, card_id):
    data = request.json
    session = sessions[db_name]
    card = session.query(Card).filter_by(id=card_id).first()
    if card:
        card.balance = data.get('balance', card.balance)
        card.card_number = data.get('card_number', card.card_number)
        session.commit()
        return jsonify({"success": True, "message": "Card updated successfully"})
    return jsonify({"success": False, "message": "Card not found"}), 404


@app.route('/<db_name>/settings', methods=['POST'])
def update_settings(db_name):
    data = request.json
    settings = sessions[db_name].query(Settings).first()
    if settings:
        for key, value in data.items():
            setattr(settings, key, value)
    else:
        settings = Settings(**data)
        sessions[db_name].add(settings)
    sessions[db_name].commit()
    return jsonify({"success": True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
