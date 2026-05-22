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
    return """
    <h1>Welcome</h1>
    <p>Your visit has been logged!</p>
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
            <h1>Admin Login</h1>
            <form method="post">
                <p style="color: red;"><strong>Wrong password!</strong></p>
                <input type="password" name="password" placeholder="Enter admin password" required>
                <button type="submit">Login</button>
            </form>
            """
    
    return """
    <h1>Admin Login</h1>
    <form method="post">
        <input type="password" name="password" placeholder="Enter admin password" required>
        <button type="submit">Login</button>
    </form>
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
        
        # Display as formatted HTML table
        html = '<h1>Visitor Logs</h1>'
        html += '<a href="/admin/logout" style="float: right; color: red;"><strong>Logout</strong></a>'
        html += '<table border="1" cellpadding="10" style="width: 100%; margin-top: 20px;">'
        html += '<tr><th>Timestamp</th><th>IP Address</th><th>Browser</th><th>Device</th><th>OS</th></tr>'
        
        for log in logs:
            html += f'<tr>'
            html += f'<td>{log["timestamp"]}</td>'
            html += f'<td>{log["ip"]}</td>'
            html += f'<td>{log["browser"]} {log["browser_version"]}</td>'
            html += f'<td>{log["device_type"]} (Mobile: {log["is_mobile"]})</td>'
            html += f'<td>{log["os"]} {log["os_version"]}</td>'
            html += f'</tr>'
        
        html += '</table>'
        return html
    except Exception as e:
        return f"<h1>Error reading logs</h1><p>{e}</p>"

@app.route('/admin/logout')
def logout():
    """Logout admin"""
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
