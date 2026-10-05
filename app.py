from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def get_database_connection():
    connection = sqlite3.connect("transactions.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    return "Payment Transaction Tracker is running!"


# GET ALL TRANSACTIONS
@app.route("/transactions", methods=["GET"])
def get_transactions():
    connection = get_database_connection()

    transactions = connection.execute(
        "SELECT * FROM transactions"
    ).fetchall()

    connection.close()

    return jsonify([dict(transaction) for transaction in transactions])


# GET ONE TRANSACTION
@app.route("/transactions/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    connection = get_database_connection()

    transaction = connection.execute(
        "SELECT * FROM transactions WHERE id = ?",
        (transaction_id,)
    ).fetchone()

    connection.close()

    if transaction is None:
        return jsonify({"error": "Transaction not found"}), 404

    return jsonify(dict(transaction))


# CREATE TRANSACTION
@app.route("/transactions", methods=["POST"])
def create_transaction():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "amount" not in data or "payment_method" not in data or "status" not in data:
        return jsonify({
            "error": "amount, payment_method and status are required"
        }), 400

    if data["amount"] <= 0:
        return jsonify({
            "error": "Amount must be greater than zero"
        }), 400

    allowed_methods = ["UPI", "Card", "NetBanking", "Wallet"]
    allowed_statuses = ["SUCCESS", "FAILED", "PENDING", "REFUNDED"]

    if data["payment_method"] not in allowed_methods:
        return jsonify({
            "error": "Invalid payment method"
        }), 400

    if data["status"] not in allowed_statuses:
        return jsonify({
            "error": "Invalid transaction status"
        }), 400

    connection = get_database_connection()

    cursor = connection.execute(
        """
        INSERT INTO transactions (amount, payment_method, status)
        VALUES (?, ?, ?)
        """,
        (
            data["amount"],
            data["payment_method"],
            data["status"]
        )
    )

    connection.commit()

    transaction_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "id": transaction_id,
        "amount": data["amount"],
        "payment_method": data["payment_method"],
        "status": data["status"]
    }), 201


# UPDATE TRANSACTION STATUS
@app.route("/transactions/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    data = request.get_json()

    connection = get_database_connection()

    transaction = connection.execute(
        "SELECT * FROM transactions WHERE id = ?",
        (transaction_id,)
    ).fetchone()

    if transaction is None:
        connection.close()
        return jsonify({"error": "Transaction not found"}), 404

    connection.execute(
        """
        UPDATE transactions
        SET status = ?
        WHERE id = ?
        """,
        (data["status"], transaction_id)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Transaction status updated successfully",
        "id": transaction_id,
        "status": data["status"]
    })


if __name__ == "__main__":
    app.run(debug=True)