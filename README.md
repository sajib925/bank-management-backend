## Bank Management System: Backend with Role-Based Authentication

This backend project utilizes Django REST Framework to implement role-based authentication for managers and customers. Customers can perform operations such as deposits, withdrawals, balance transfers, and loan requests, while managers can oversee transactions and approve loan applications efficiently.



## Features

- ### Role-Based Authentication
  - **Managers** and **Customers** have distinct roles, with access to functionalities tailored to each user type.

- ### Customer Functionalities
  - **Deposits**: Make and manage deposits to their account.
  - **Withdrawals**: Withdraw funds from their account.
  - **Balance Transfer**: Transfer funds to other accounts.
  - **Loan Requests**: Apply for loans with flexible terms.

- ### Manager Functionalities
  - **Transaction Oversight**: Monitor and manage all transactions within the system.
  - **Loan Management**: Review, approve, or reject loan applications submitted by customers.


# API Endpoints

### User Management
- **Admin Users**:
  - **List/Create Admin Users**: `POST /api/manager/`
  - **Admin User Details**: `GET /api/manager/<int:pk>/`
- **Customers**:
  - **List/Create Customers**: `POST /api/customer/`
  - **Customer Details**: `GET /api/customer/<int:pk>/`

### Authentication
- **Register**: `POST /api/register/`
- **Login**: `POST /api/login/`
- **Profile Update**: `PUT /api/update-profile/`
- **Password Update**: `PUT /api/update-password/`
- **Logout**: `POST /api/logout/`

### Financial Transactions
- **Balance Transfer**: `POST /api/balance-transfer/`
- **Loans**:
  - **List/Create Loans**: `POST /api/loans/`
  - **Loan Details**: `GET /api/loans/<int:pk>/`
  - **Approve Loan**: `POST /api/loans/<int:pk>/approve/`
  - **Reject Loan**: `POST /api/loans/<int:pk>/reject/`
  - **Repay Loan**: `POST /api/loans/<int:pk>/repay/`
- **Deposits**: `POST /api/deposit/`
- **Withdrawals**: `POST /api/withdrawal/`

### Services
- **Service List/Create**: `POST /api/services/`

### Contact
- **Contact Us**: `POST /api/contact/`



**Base URL**: [https://bank-management-backend.onrender.com/](https://bank-management-backend.onrender.com/)

## Installation

To set up the backend on your local machine, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/sajib925/bank-management-backend.git
   cd bank-management-backend
