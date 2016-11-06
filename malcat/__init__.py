import os
import yaml

BASE_DIR = os.getcwd()
_CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'malcat.config.yaml')

with open(_CONFIG_FILE_PATH) as f:
    config = yaml.load(f)

# Add env_variables to the global config.

try:
    URLFETCH_TIMEOUT = int(os.getenv('URLFETCH_TIMEOUT'))
except TypeError:
    URLFETCH_TIMEOUT = None
finally:
    config['URLFETCH_TIMEOUT'] = URLFETCH_TIMEOUT

config['URLFETCH_USE_HTTPS'] = bool(os.getenv('URLFETCH_USE_HTTPS'))

try:
    MEMCACHE_TIMEOUT = int(os.getenv('MEMCACHE_TIMEOUT'))
except TypeError:
    MEMCACHE_TIMEOUT = None
finally:
    config['MEMCACHE_TIMEOUT'] = MEMCACHE_TIMEOUT
