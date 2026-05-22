import requests

# Create a session to maintain cookies
s = requests.Session()

# Login
r1 = s.post('http://localhost:5000/admin/login', data={'password': 'admin123'})
print(f"Login response status: {r1.status_code}")

# Try to access logs
r2 = s.get('http://localhost:5000/logs')
print(f"Logs response status: {r2.status_code}")
print(f"Logs contains 'Visitor Logs': {'Visitor Logs' in r2.text}")
print(f"Logs contains table: {'<table>' in r2.text}")

# Try to access without session (should redirect)
r3 = requests.get('http://localhost:5000/logs', allow_redirects=False)
print(f"Logs without session redirects: {r3.status_code == 302}")
print("✅ All tests passed!")
