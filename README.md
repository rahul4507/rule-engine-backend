# Rule Engine using AST

A Django REST Framework based backend service with JWT token authentication, that provides end-to-end authorization intelligence using Abstract Syntax Trees (AST), offering a complete 360-degree approach to creating, managing, and evaluating complex business rules.

# Frontend Repo Link : https://github.com/rahul4507/rule-engine-frontend

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package installer)

## Technology Stack

- Django 4.2
- Django REST Framework 3.15.1
- PostgreSQL (Database)
- JWT Authentication (Simple JWT)
- Python-environ (Environment Variables Management)
- Logging Service Integration

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd <your-project-directory>
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   - Install PostgreSQL if not already installed
   - Create a new PostgreSQL database:
     ```bash
     createdb <your_db_name>
     ```
   - Or using psql:
     ```sql
     CREATE DATABASE <your_db_name>;
     ```

5. **Environment Variables**
   Create a `.env` file in the root directory with the following variables:
   ```env
   DJANGO_DEBUG=True
   DJANGO_SECRET_KEY=<your-secret-key-here>
   DATABASE_URL=postgresql://<db_user>:<db_password>@<db_host>:<db_port>/<your_db_name>
   DJANGO_READ_DOT_ENV_FILE=True
   LOGGING_SERVICE_TOKEN=<your-logging-service-token>  # If using a logging service (optional)
   ```
   **Setting up Logtail (optional)**
      - Create Better Stack Account
      - Visit Better Stack Telemetry Sign up for a free account Verify your email address

      - Create a Source
      - After logging in, go to "Sources" in the dashboard
      - Click "Add new source"
      - Select "Django" as your source type
      - Name your source (e.g., "Django Backend")
      - Copy the provided source_token
   
7. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

8. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Server

1. **Start the development server**
   ```bash
   python manage.py runserver
   ```
   The server will start at http://localhost:8000

2. **Access the admin interface**
   Visit http://localhost:8000/admin/

## API Authentication

The project uses JWT (JSON Web Token) authentication. Here are the key configurations:

- Token lifetime: Access token expires in 120 minutes (configurable)
- Refresh token lifetime: 1 day (configurable)
- Authentication header format: `Bearer <token>`

## Available Endpoints

- Admin Interface: `/admin/`
- API endpoints will be prefixed with `/api/`
- Authentication endpoints:
  - Token obtain: `/api/token/`
  - Token refresh: `/api/token/refresh/`

## Project Structure

```
your_project_name/
├── config/               # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/               # User management app
├── manage.py
├── requirements.txt
└── .env
```

## Environmental Configurations

The project supports different environments through the `env` variable:
- Default environment: 'local'
- Supported environments: Set through `ENV_NAME` in environment variables

## Logging

- Logging can be configured with your preferred logging service
- Default log level: INFO and above
- Custom logger name: Configure in settings

## Security

- CORS settings are configurable in settings
- CSRF protection is enabled
- Custom password validators are configurable
- JWT tokens are used for API authentication

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## Troubleshooting

Common issues and solutions:

1. **Database Connection Issues**
   - Verify PostgreSQL is running
   - Check database credentials in .env file
   - Ensure database exists

2. **Migration Issues**
   ```bash
   python manage.py migrate --run-syncdb
   ```

3. **Permission Issues**
   - Verify PostgreSQL user permissions
   - Check file permissions for .env and log files

## Customization Notes

1. Replace the following placeholders with your specific values:
   - `<your-repository-url>`
   - `<your-project-directory>`
   - `<your_db_name>`
   - `<db_user>`, `<db_password>`, `<db_host>`, `<db_port>`
   - `<your-secret-key-here>`
   - `<your-logging-service-token>`
   - `<your-name>`
   - `<your-email>`

2. Adjust the configurations in settings.py according to your needs:
   - Database settings
   - JWT token lifetime
   - CORS settings
   - Logging configuration
   - Email settings (if needed)
