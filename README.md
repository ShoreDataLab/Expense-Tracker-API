# Expense Tracker API

A robust RESTful API built with FastAPI and MySQL for comprehensive personal financial management.

## Overview

This Expense Tracker API provides a powerful backend solution for managing personal finances, offering a comprehensive suite of features to help users track, analyse, and optimise their financial activities.

## Key Features

- **User Management**: Secure user registration and profile management
- **Account Management**: Support for multiple account types (checking, savings, credit cards)
- **Transaction Tracking**: Record and manage both one-time and recurring transactions
- **Budget Management**: Create and track budgets by category
- **Category Management**: Flexible categorisation of expenses and income
- **Multi-Currency Support**: Handle transactions in different currencies
- **Recurring Transactions**: Schedule and manage recurring payments and income

- **User Management**

    1. Secure user registration and authentication
    2. Profile management with detailed personal information
    3. Role-based access control


- **Account Management**

    1. Support for multiple account types (checking, savings, credit cards)
    2. Ability to link and manage multiple financial accounts
    3. Account balance tracking and reconciliation


- **Transaction Tracking**

    1. Record and manage both one-time and recurring transactions
    2. Detailed transaction categorisation
    3. Advanced filtering and search capabilities
    4. Support for split transactions


- **Budget Management**

    1. Create and track budgets by category
    2. Set monthly, quarterly, and annual budget goals
    3. Real-time budget performance tracking
    4. Alerts and notifications for budget overruns

## Technical Stack

- **Backend Framework**: FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT-based authentication
- **API Documentation**: Automatic OpenAPI (Swagger) documentation
- **Validation**: Pydantic schemas
- **Asnyc Support**: Fully asynchronous architecture

## API Endpoints

- `/users`: User registration and management
- `/accounts`: Financial account management
- `/categories`: Expense/Income categories
- `/transactions`: Transaction tracking
- `/recurring-transactions`: Recurring payment management
- `/budgets`: Budget creation and tracking
- `/currencies`: Currency management

## Specialised Endpoints

### Expense API

* Depends on User, Category, and Account
* Special type of transaction specifically for expenses

### Goal API

* Depends on User
* Financial goals tracking

### Alert API

* Depends on User
* Notifications system for budgets, bills, and goals


## Configuration
Environment variables are managed through `config.py`, providing a centralised configuration approach for the application.

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