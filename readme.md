# Django Auth

This project is a Django-based backend application that includes user registration, login, password reset, and user detail retrieval functionalities using simpleJWT for secure authentication.

## Features

- User Registration
- User Login
- Password Reset
- User Detail Retrieval
- OTP Verification
- Send Password Reset OTP
- JWT-based Authentication

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/django-user-management.git
    cd django-user-management
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### User Registration

- **URL**: `/api/register/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "email": "user@example.com",
        "username": "username",
        "password": "password"
    }
    ```
- **Response**:
    ```json
    {
        "message": "User Registered Successfully.",
        "success": True
    }
    ```

### User Login

- **URL**: `/api/login/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "email": "user@example.com",
        "password": "password"
    }
    ```
- **Response**:
    ```json
    {
        "access_token": "access_token_value",
        "refresh_token": "refresh_token_value",
        "data": {
            "id": 1,
            "email": "user@example.com",
            "username": "username",
            "bio": "user bio"
        },
        "message": "User Login Success",
        "success": True
    }
    ```

### Password Reset

- **URL**: `/api/password-reset/`
- **Method**: `POST`
- **Request Headers**:
    - `Authorization`: `Bearer <access_token>`
- **Request Body**:
    ```json
    {
        "new_password": "new_password_value"
    }
    ```
- **Response**:
    ```json
    {
        "message": "Password updated successfully",
        "success": True
    }
    ```

### User Detail Retrieval

- **URL**: `/api/user-detail/`
- **Method**: `GET`
- **Request Headers**:
    - `Authorization`: `Bearer <access_token>`
- **Response**:
    ```json
    {
        "data": {
            "id": 1,
            "email": "user@example.com",
            "username": "username",
            "bio": "user bio"
        },
        "message": "User data retrieved successfully",
        "success": True
    }
    ```

### OTP Verification

- **URL**: `/api/otp-verify/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "email": "user@example.com",
        "otp": 123456
    }
    ```
- **Response**:
    ```json
    {
        "message": "OTP verified successfully.",
        "success": True
    }
    ```

### Send Password Reset OTP

- **URL**: `/api/send-password-reset-otp/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "email": "user@example.com"
    }
    ```
- **Response**:
    ```json
    {
        "message": "Password Reset OTP sent successfully.",
        "success": True
    }
    ```

## Authentication

This project uses simpleJWT for authentication. Obtain the access and refresh tokens from the login endpoint and use the access token in the `Authorization` header as a bearer token for protected endpoints.
