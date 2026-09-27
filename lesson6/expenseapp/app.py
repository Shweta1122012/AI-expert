from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "expenses.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


@app.route("/api/expenses", methods=["POST"])
def add_expense():

    data = request.get_json()

    title = str(data.get("title", "")).strip()
    category = str(data.get("category", "Other")).strip()
    amount = data.get("amount")

    if not title or amount is None:
        return jsonify({
            "error": "Title and amount are required."
        }), 400

    try:
        amount = float(amount)

        if amount <= 0:
            raise ValueError

    except (ValueError, TypeError):
        return jsonify({
            "error": "Amount must be a positive number."
        }), 400

    date = data.get("date") or datetime.now().strftime("%Y-%m-%d")

    conn = get_db()

    cursor = conn.execute(
        """
        INSERT INTO expenses
        (title, amount, category, date)
        VALUES (?, ?, ?, ?)
        """,
        (title, amount, category, date)
    )

    conn.commit()

    expense_id = cursor.lastrowid

    row = conn.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    conn.close()

    return jsonify(dict(row)), 201


@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):

    conn = get_db()

    cursor = conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({
            "error": "Expense not found."
        }), 404

    return jsonify({
        "success": True
    })


@app.route("/api/expenses", methods=["DELETE"])
def delete_all():

    conn = get_db()

    conn.execute("DELETE FROM expenses")

    conn.commit()
    conn.close()

    return jsonify({
        "success": True
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)