import time
import json

class SimpleCache:
    def __init__(self, filename='cache.json'):
        self.cache = {}
        self.filename = filename
        self.load_cache()

    def add(self, key, value, ttl):
        expiry = time.time() + ttl
        self.cache[key] = (value, expiry)
        self.persist_cache()

    def fetch(self, key):
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            else:
                self.delete(key)
        return None

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
            self.persist_cache()

    def persist_cache(self):
        serializable_cache = {}
        for key, (value, expiry) in self.cache.items():
            serializable_cache[key] = {'value': value, 'expiry': expiry}
        with open(self.filename, 'w') as f:
            json.dump(serializable_cache, f)

    def load_cache(self):
        try:
            with open(self.filename, 'r') as f:
                items = json.load(f)
                for key, data in items.items():
                    self.cache[key] = (data['value'], data['expiry'])

                    # Automatically delete expired items upon loading
                    if time.time() > data['expiry']:
                        self.delete(key)

        except FileNotFoundError:
            self.cache = {}

# Example usage
cache = SimpleCache()
cache.add('test', 'Hello, World!', 10)  # TTL is 10 seconds

# Fetch the item immediately
print(cache.fetch('test'))  # Output: 'Hello, World!'

# Wait for 10 seconds to simulate the item expiry
time.sleep(10)

# Attempt to fetch the expired item
print(cache.fetch('test'))  # Output: None as the entry has expired

# Demonstrating persistence
# Restarting the script here would demonstrate loading from 'cache.json'
cache.add('test', 'Persistent data', 10)
cache = SimpleCache()

# Attempt to fetch the previously added item
print(cache.fetch('test'))