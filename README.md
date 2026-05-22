# Visitor Logging System

A simple Flask app to log visitor information to your own website/app - **for your own site only** ✅

## What Gets Logged

- **IP Address** - Visitor's IP address
- **Browser** - Browser type and version
- **Device Type** - Mobile, tablet, or PC
- **Operating System** - OS and version
- **Timestamp** - When they visited

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
python app.py
```

The app runs on `http://localhost:5000`

## Usage

### Routes

- **`/`** - Main page (logs visitor automatically)
- **`/logs`** - View all logged visitor data in a table

### Log Format

Logs are saved to `visitor_logs.json` as JSON lines format - one visitor per line:

```json
{
  "timestamp": "2026-05-22T10:30:45.123456",
  "ip": "192.168.1.100",
  "browser": "Chrome",
  "browser_version": "91.0.4472.124",
  "device_type": "PC",
  "os": "Windows",
  "os_version": "10.0",
  "is_mobile": false,
  "is_tablet": false,
  "is_pc": true,
  "user_agent_string": "Mozilla/5.0..."
}
```

## Important Notes ⚠️

- ✅ **LEGAL**: Use this only to log visitors to YOUR OWN website/app
- ❌ **NOT LEGAL**: Don't use this to track other people's accounts or data
- 💾 **Data Privacy**: This logs IP addresses - inform visitors in your privacy policy
- 🔒 **Security**: Don't expose the `/logs` endpoint publicly in production (add authentication)

## Example: Accessing from Outside Your Computer

To access from another device on your network:
```
http://YOUR_COMPUTER_IP:5000
```

Find your IP: Run `ipconfig` (Windows) or `ifconfig` (Linux/Mac)

## Production Deployment

For production use, consider:
- Adding authentication to `/logs` route
- Using a database instead of JSON files
- Adding rate limiting
- Implementing SSL/HTTPS
- Running with a production WSGI server (Gunicorn, etc.)