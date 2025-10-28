import os

ALLOWED_HOSTS = [
    'gamingstore-omf0.onrender.com',
    '.onrender.com',
    'localhost',
    '127.0.0.1', 
    '0.0.0.0',
]

# Also include any from environment variable
env_hosts = os.environ.get('ALLOWED_HOSTS', '')
if env_hosts:
    ALLOWED_HOSTS.extend(env_hosts.split(','))