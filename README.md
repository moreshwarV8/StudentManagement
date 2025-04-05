# Student Management System

A modern web-based Student Management System built with Django and PostgreSQL. This system helps educational institutions manage student records, attendance, and activities with a sleek, user-friendly interface.

![Student Management System](https://your-screenshot-url.com)

## ✨ Features

- **User Authentication**
  - Secure login and authentication
  - Role-based access control
  - Password protection

- **Student Management**
  - Add, edit, and delete student records
  - Store comprehensive student information
  - Search and filter capabilities
  - Bulk import/export functionality

- **Department Management**
  - Create and manage departments

## 🚀 AWS EC2 Deployment Guide

### 1. Launch EC2 Instance
- Launch an Ubuntu EC2 instance
- Configure Security Group to allow inbound traffic on ports 22 (SSH), 80 (HTTP), and 443 (HTTPS)
- Download your key pair (.pem file)

### 2. Connect to EC2
```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@ec2-13-60-162-30.eu-north-1.compute.amazonaws.com

```

### 3. Install Dependencies
```bash
# Update package list
sudo apt update

# Install Python and other dependencies
sudo apt install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx

# Install virtualenv
pip3 install virtualenv
```

### 4. Clone and Setup Project
```bash
# Clone repository
git clone <your-repo-url>
cd student_management

# Create virtual environment
virtualenv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 5. Setup PostgreSQL
```bash
# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell, create database and user
CREATE DATABASE student_management;
CREATE USER dbuser WITH PASSWORD 'your-secure-password';
ALTER ROLE dbuser SET client_encoding TO 'utf8';
ALTER ROLE dbuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE dbuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE student_management TO dbuser;
\q
```

### 6. Configure Environment Variables
```bash
# Create .env file
echo "DJANGO_SECRET_KEY='your-secure-secret-key'" > .env
echo "DATABASE_URL='postgresql://dbuser:your-secure-password@localhost:5432/student_management'" >> .env

# Apply database migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 7. Setup Gunicorn
```bash
# Create gunicorn service
sudo nano /etc/systemd/system/gunicorn.service
```

Add the following content:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/student_management
ExecStart=/home/ubuntu/student_management/venv/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/home/ubuntu/student_management/student_management.sock \
    student_management.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 8. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/student_management
```

Add the following content:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain or EC2 public IP

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/student_management;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/student_management/student_management.sock;
    }
}
```

### 9. Enable and Start Services
```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/student_management /etc/nginx/sites-enabled

# Test Nginx configuration
sudo nginx -t

# Start services
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart nginx
```

### 10. Collect Static Files
```bash
python manage.py collectstatic
```

### 11. Final Steps
- Update ALLOWED_HOSTS in settings.py with your EC2 public IP or domain
- Configure your domain DNS if using a custom domain
- Setup SSL with Let's Encrypt (recommended)

## 🔍 Monitoring and Maintenance
- Check logs: `sudo journalctl -u gunicorn`
- Restart services: `sudo systemctl restart gunicorn nginx`
- Monitor system resources: `htop`

## 🔒 Security Considerations
- Keep Django SECRET_KEY secure
- Regular system updates
- Configure firewall rules
- Use strong database passwords
- Enable SSL/HTTPS
  - Assign students to departments
  - Track department-wise statistics

- **Attendance System**
  - Mark daily attendance
  - View attendance reports
  - Track attendance patterns
  - Generate attendance summaries

- **Activity Tracking**
  - Monitor student activities
  - Record achievements and participation
  - Activity history and timeline

- **Modern UI/UX**
  - Clean and intuitive interface
  - Responsive design for all devices
  - Interactive dashboards
  - Real-time updates

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd student_management
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   .\venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL**
   - Install PostgreSQL if not already installed
   - Create a new database:
     ```sql
     CREATE DATABASE student_management;
     ```
   - Update `student_management/settings.py` with your database credentials:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'student_management',
             'USER': 'your_username',
             'PASSWORD': 'your_password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

5. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   # Follow the prompts to create an admin account
   ```

7. **Load Sample Data (Optional)**
   ```bash
   python manage.py setup_db
   ```

8. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

9. **Access the Application**
   - Main application: http://localhost:8000
   - Admin interface: http://localhost:8000/admin

## 📱 Usage Guide

### First-Time Setup

1. Log in with your superuser credentials
2. Create departments through the admin interface
3. Add initial student records
4. Set up user accounts for staff members

### Daily Operations

1. **Managing Students**
   - Navigate to Students section
   - Use the + button to add new students
   - Click on student cards to view/edit details
   - Use the search bar to find specific students

2. **Taking Attendance**
   - Go to Attendance section
   - Select the date and department
   - Mark present/absent for each student
   - Save the attendance record

3. **Recording Activities**
   - Visit the Activities section
   - Select students involved
   - Add activity details and date
   - Save the activity record

## 🛠️ Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check database credentials in settings.py
   - Ensure database exists

2. **Migration Issues**
   - Remove migration files if needed
   - Reset database and run migrations again

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT in settings.py

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Support

For support:
- Open an issue on GitHub
- Contact: your.email@example.com
- Documentation: [Wiki Link]

## 🙏 Acknowledgments

- Django Framework
- Bootstrap
- PostgreSQL
- Font Awesome
- All contributors

