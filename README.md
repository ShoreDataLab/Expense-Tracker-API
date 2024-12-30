# Expense Tracker API

A robust RESTful API built with FastAPI and MySQL for managing personal finances and expense tracking.

## Overview

This API serves as the backend for an expense tracking application, providing endpoints for managing users, accounts, transactions, budgets, and more. Built with FastAPI and SQLAlchemy, it offers a comprehensive suite of financial management features.

## Key Features

- **User Management**: Secure user registration and profile management
- **Account Management**: Support for multiple account types (checking, savings, credit cards)
- **Transaction Tracking**: Record and manage both one-time and recurring transactions
- **Budget Management**: Create and track budgets by category
- **Category Management**: Flexible categorization of expenses and income
- **Multi-Currency Support**: Handle transactions in different currencies
- **Recurring Transactions**: Schedule and manage recurring payments and income

## Technical Stack

- **Framework**: FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT-based authentication
- **Documentation**: Automatic OpenAPI (Swagger) documentation

## API Endpoints

- `/users`: User registration and management
- `/accounts`: Financial account management
- `/categories`: Expense/Income categories
- `/transactions`: Transaction tracking
- `/recurring-transactions`: Recurring payment management
- `/budgets`: Budget creation and tracking
- `/currencies`: Currency management

## Getting Started

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy .env.example to .env
- Update variables as needed

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Documentation

API documentation is available at `/docs` when running the server (Swagger UI).


## Project Structure
```
expense-tracker-api/
├── app/
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic schemas
├── routers/         # API endpoints
├── services/        # Business logic
├── utils/          # Helper functions
├── requirements.txt # Project dependencies
└── main.py         # Application entry point
```