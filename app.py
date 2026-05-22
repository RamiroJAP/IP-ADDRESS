from flask import Flask, request
import json
from datetime import datetime
from user_agents import parse

app = Flask(__name__)

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
    <p>Check <strong>visitor_logs.json</strong> to see all visitor information.</p>
    """

@app.route('/logs')
def view_logs():
    """View all visitor logs (for admin purposes only)"""
    try:
        with open('visitor_logs.json', 'r') as f:
            logs = [json.loads(line) for line in f if line.strip()]
        
        # Display as formatted HTML table
        html = '<h1>Visitor Logs</h1><table border="1" cellpadding="10">'
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
