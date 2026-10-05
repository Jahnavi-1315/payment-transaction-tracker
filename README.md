# Payment Transaction Tracker

A beginner-friendly backend application for managing payment transactions using Python, Flask and SQLite.

## Features

- Create payment transactions
- View all transactions
- View a transaction by ID
- Update transaction status
- Validate payment details
- Store transactions using SQLite
- Test REST APIs using Postman

## Technologies

- Python
- Flask
- SQLite
- SQL
- REST APIs
- JSON
- Postman

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /transactions | Get all transactions |
| GET | /transactions/<id> | Get one transaction |
| POST | /transactions | Create a transaction |
| PUT | /transactions/<id> | Update transaction status |

## Example Transaction

```json
{
    "amount": 1500,
    "payment_method": "UPI",
    "status": "SUCCESS"
}

