from flask import Flask, request, session, redirect, url_for
import json
from datetime import datetime
from user_agents import parse

app = Flask(__name__)
app.secret_key = 'visitor-logger-secret-key-change-me'
ADMIN_PASSWORD = 'admin123'

def log_visitor():
    """Log visitor information to a JSON file"""
    try:
        ip = request.remote_addr
        user_agent_string = request.headers.get('User-Agent', 'Unknown')
        user_agent = parse(user_agent_string)
        
        visitor_data = {
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'browser': str(user_agent.browser.family),
            'browser_version': str(user_agent.browser.version_string),
            'device_type': str(user_agent.device.family),
            'os': str(user_agent.os.family),
            'os_version': str(user_agent.os.version_string),
            'is_mobile': user_agent.is_mobile,
            'is_tablet': user_agent.is_tablet,
            'is_pc': user_agent.is_pc,
            'user_agent_string': user_agent_string
        }
        
        # Append to JSON log file
        with open('visitor_logs.json', 'a') as f:
            f.write(json.dumps(visitor_data) + '\n')
            
    except Exception as e:
        print(f"Error logging visitor: {e}")

@app.route('/')
def home():
    log_visitor()
    # If user is admin, show dashboard; otherwise show welcome page
    if session.get('admin'):
        return view_logs()
    return """
    <html>
    <head>
        <title>Visitor Log</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <h1>Welcome</h1>
        <p>Your visit has been logged!</p>
        <hr>
        <p><a href="/admin/login">Admin Login</a></p>
    </body>
    </html>
    """

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('view_logs'))
        else:
            return """
            <html>
            <head>
                <title>Admin Login</title>
                <style>
                    body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
                    .login-box { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }
                    h1 { text-align: center; color: #333; }
                    input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px; }
                    button { width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: bold; }
                    button:hover { background: #764ba2; }
                    .error { color: #dc3545; text-align: center; margin-bottom: 15px; }
                </style>
            </head>
            <body>
                <div class="login-box">
                    <h1>🔐 Admin Login</h1>
                    <p class="error"><strong>❌ Wrong password!</strong></p>
                    <form method="post">
                        <input type="password" name="password" placeholder="Enter admin password" required autofocus>
                        <button type="submit">Login</button>
                    </form>
                </div>
            </body>
            </html>
            """
    
    return """
    <html>
    <head>
        <title>Admin Login</title>
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            .login-box { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }
            h1 { text-align: center; color: #333; }
            input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px; }
            button { width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: bold; }
            button:hover { background: #764ba2; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h1>🔐 Admin Login</h1>
            <form method="post">
                <input type="password" name="password" placeholder="Enter admin password" required autofocus>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route('/logs')
def view_logs():
    """View all visitor logs (admin only)"""
    # Check if admin is logged in
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    try:
        with open('visitor_logs.json', 'r') as f:
            logs = [json.loads(line) for line in f if line.strip()]
        
        # Reverse to show newest first
        logs.reverse()
        
        # Display as formatted HTML table
        html = """
        <html>
        <head>
            <title>Visitor Logs - Admin</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
                h1 { color: #333; }
                table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                th { background: #007bff; color: white; padding: 12px; text-align: left; }
                td { padding: 12px; border-bottom: 1px solid #ddd; }
                tr:hover { background: #f9f9f9; }
                .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
                .logout { background: #dc3545; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; }
                .logout:hover { background: #c82333; }
                .stats { display: flex; gap: 20px; margin-bottom: 20px; }
                .stat-box { background: white; padding: 20px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); flex: 1; }
                .stat-number { font-size: 24px; font-weight: bold; color: #007bff; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔐 Visitor Logs</h1>
                <a href="/admin/logout" class="logout">Logout</a>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <div>Total Visits</div>
                    <div class="stat-number">""" + str(len(logs)) + """</div>
                </div>
                <div class="stat-box">
                    <div>Unique IPs</div>
                    <div class="stat-number">""" + str(len(set([log.get('ip', 'Unknown') for log in logs]))) + """</div>
                </div>
            </div>
            
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>IP Address</th>
                    <th>Browser</th>
                    <th>Device</th>
                    <th>OS</th>
                </tr>
        """
        
        for log in logs:
            html += f"""<tr>
                <td>{log.get("timestamp", "N/A")}</td>
                <td><code>{log.get("ip", "N/A")}</code></td>
                <td>{log.get("browser", "N/A")} {log.get("browser_version", "")}</td>
                <td>{log.get("device_type", "N/A")}</td>
                <td>{log.get("os", "N/A")} {log.get("os_version", "")}</td>
            </tr>"""
        
        html += """
            </table>
        </body>
        </html>
        """
        return html
    except FileNotFoundError:
        if not session.get('admin'):
            return redirect(url_for('login'))
        return """
        <html>
        <head><title>Visitor Logs - Admin</title></head>
        <body>
            <h1>🔐 Visitor Logs</h1>
            <a href="/admin/logout">Logout</a>
            <p>No visitor logs yet.</p>
        </body>
        </html>
        """
    except Exception as e:
        return f"<p>Error loading logs: {e}</p>"

@app.route('/admin/logout')
def logout():
    """Logout admin"""
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
