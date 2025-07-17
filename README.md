# URL Shortener API

A professional RESTful API service for creating and managing shortened URLs, built with Flask and MySQL. This service provides comprehensive URL shortening capabilities with access tracking, validation, and full CRUD operations.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/jaweriafayyaz/jaweria-innovaxel-fayyaz.git
cd jaweria-innovaxel-fayyaz

# Switch to development branch
git checkout dev

# Install dependencies
pip install flask flask-sqlalchemy pymysql python-dotenv cryptography

# Configure MySQL database (see Database Setup below)
# Update .env file with your credentials

# Run the application
python run.py
```

The API will be available at `http://localhost:5000`

## 📋 Prerequisites

* **Python 3.7+**
* **MySQL Server 5.7+**
* **pip package manager**
* **Git**

## 🗄️ Database Setup

### 1. Install MySQL
Download and install MySQL from [official website](https://dev.mysql.com/downloads/)

### 2. Create Database
```sql
-- Connect to MySQL
mysql -u root -p

-- Create database and user
CREATE DATABASE url_shortener CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'url_shortener_user'@'localhost' IDENTIFIED BY 'secure_password_123';
GRANT ALL PRIVILEGES ON url_shortener.* TO 'url_shortener_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Environment Configuration
Create `.env` file in project root:
```env
SECRET_KEY=your-super-secret-key-change-this
MYSQL_HOST=localhost
MYSQL_USER=url_shortener_user
MYSQL_PASSWORD=secure_password_123
MYSQL_DB=url_shortener
MYSQL_PORT=3306
```

## 📡 API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/shorten` | Create new short URL | `201`, `400` |
| `GET` | `/shorten/{code}` | Retrieve original URL | `200`, `404` |
| `PUT` | `/shorten/{code}` | Update existing URL | `200`, `400`, `404` |
| `DELETE` | `/shorten/{code}` | Delete short URL | `204`, `404` |
| `GET` | `/shorten/{code}/stats` | Get URL statistics | `200`, `404` |

## 🔧 Usage Examples

### Create Short URL
```bash
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

**Response:**
```json
{
  "id": "1",
  "url": "https://www.google.com",
  "shortCode": "PX8Vcf",
  "createdAt": "2025-07-17T12:13:14.000000Z",
  "updatedAt": "2025-07-17T12:13:14.000000Z",
  "accessCount": 0
}
```

### Retrieve Original URL
```bash
curl -X GET http://localhost:5000/shorten/PX8Vcf
```

### Update Short URL
```bash
curl -X PUT http://localhost:5000/shorten/PX8Vcf \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com"}'
```

### Get Statistics
```bash
curl -X GET http://localhost:5000/shorten/PX8Vcf/stats
```

### Delete Short URL
```bash
curl -X DELETE http://localhost:5000/shorten/PX8Vcf
```

## 🏗️ Architecture

```
url-shortener/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── url.py           # URL database model
│   ├── routes/
│   │   ├── __init__.py
│   │   └── api.py           # API endpoints
│   └── utils/
│       ├── __init__.py
│       └── validators.py    # URL validation
├── config.py                # App configuration
├── run.py                   # Application entry point
├── .env                     # Environment variables
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## 🛠️ Technology Stack

* **Backend Framework:** Flask
* **Database:** MySQL 8.0
* **ORM:** SQLAlchemy
* **Database Driver:** PyMySQL
* **Environment Management:** python-dotenv
* **Validation:** Custom regex + urllib

## ✨ Features

* ✅ **RESTful API Design** - Clean, intuitive endpoints
* ✅ **URL Validation** - Comprehensive format checking
* ✅ **Unique Short Codes** - 6-character alphanumeric codes
* ✅ **Access Tracking** - Real-time click statistics
* ✅ **Error Handling** - Proper HTTP status codes
* ✅ **Database Optimization** - Indexed queries for performance
* ✅ **Security** - Input validation and sanitization

## 🧪 Testing

The API has been thoroughly tested with all endpoints returning proper HTTP status codes:

* **Create:** Returns `201 Created` with URL data
* **Retrieve:** Returns `200 OK` with access count increment
* **Update:** Returns `200 OK` with updated timestamp
* **Delete:** Returns `204 No Content` on success
* **Stats:** Returns `200 OK` without count increment
* **Errors:** Returns appropriate `400`/`404`/`500` codes

## 📊 Database Schema

**URLs Table:**
```sql
CREATE TABLE urls (
    id INT PRIMARY KEY AUTO_INCREMENT,
    original_url TEXT NOT NULL,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    access_count INT DEFAULT 0,
    INDEX idx_short_code (short_code)
);
```

## 🚀 Deployment

### Development
```bash
python run.py
```

### Production
Use a production WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## 🔒 Security Considerations

* Input validation on all endpoints
* SQL injection prevention via ORM
* Rate limiting recommended for production
* HTTPS required for production deployment
* Environment variables for sensitive data

## 📈 Performance

* Database indexing on short_code column
* Connection pooling enabled
* Efficient query patterns
* Minimal memory footprint

## 🤝 Development Workflow

1. **Main Branch:** Contains only README.md and setup instructions
2. **Dev Branch:** Contains all application code and development history
3. **Code Review:** Professional code documentation and comments

## 📞 API Health Check

Visit `http://localhost:5000/` for API status and endpoint information.

## 👨‍💻 Developer Information

* **Project Type:** Take-home Assignment
* **Framework:** Flask (Python)
* **Database:** MySQL
* **API Style:** RESTful
* **Documentation:** Comprehensive inline comments

## 📝 Requirements Compliance

✅ **5 API Endpoints** - Create, Read, Update, Delete, Stats  
✅ **MySQL Database** - Full integration with proper schema  
✅ **Error Handling** - Comprehensive validation and responses  
✅ **URL Validation** - Regex and urllib-based checking  
✅ **Access Tracking** - Real-time statistics and counting  
✅ **Professional Code** - Clean architecture and documentation  

---

**Note:** Switch to the `dev` branch to access the complete application code and development history.
