# Bank Management System: Backend with Role-Based Authentication

This backend project utilizes Django REST Framework to implement role-based authentication for managers and customers. Customers can perform operations such as deposits, withdrawals, balance transfers, and loan requests, while managers can oversee transactions and approve loan applications efficiently.

## Table of Contents

- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- Role-based authentication for managers and customers
- Customer functionalities:
  - Manage deposits
  - Make withdrawals
  - Transfer balances
  - Request loans
- Manager functionalities:
  - Oversee transactions
  - Approve loan applications

## API Endpoints

Here are the available API endpoints:

- **Admin**: `/admin/`
- **Authentication**: 
  - `/api-auth/`
  - `/api/auth/`
- **Transactions**: `/api/transactions/`
- **Account Management**: `/api/account/`
- **Services**: `/api/services/`
- **Contact**: `/api/contact/`

**Base URL**: [https://bank-management-backend.onrender.com/](https://bank-management-backend.onrender.com/)

## Installation

To set up the backend on your local machine, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bank-management-backend.git
   cd bank-management-backend
