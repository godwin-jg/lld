import time

class TokenBucket: #23
    def __init__(self, capacity, refill_rate):
        self.clients = {}
        self.capacity = capacity
        self.refill_rate = refill_rate
        
    def refill_and_check(self, user_id, endpoint):
        client_key = f'{user_id}:{endpoint}'
        
        now = time.time()
        if client_key not in self.clients:
            self.clients[client_key] = {
                "capacity": self.capacity,
                "last_refill": now,
            }
        
        bucket = self.clients[client_key] 
        
        last_refill = bucket['last_refill']
        capacity = bucket['capacity']
        
        time_elapsed = now - last_refill
        
        refill = capacity + time_elapsed * self.refill_rate
        
        bucket['capacity'] = refill
        bucket['last_refill'] = now
        
        if bucket['capacity'] >= 1.0:
            bucket['capacity'] -= 1.0
            return True

        return False
    
    def is_allowed(self, user_id, endpoint):
        return self.refill_and_check(user_id, endpoint)
    


    
limiter = TokenBucket(capacity=2, refill_rate=1.0)

user_ip = "192.168.1.50"

print("--- Simulating Heavy Traffic on /search Endpoint ---")
# First 2 requests should pass (utilizing the burst capacity)
print(f"Hit 1 (/search): {'ALLOWED ✅' if limiter.is_allowed(user_ip, '/search') else 'BLOCKED ❌'}")
print(f"Hit 2 (/search): {'ALLOWED ✅' if limiter.is_allowed(user_ip, '/search') else 'BLOCKED ❌'}")
# 3rd request fails because the /search bucket for this IP is empty
print(f"Hit 3 (/search): {'ALLOWED ✅' if limiter.is_allowed(user_ip, '/search') else 'BLOCKED ❌'}")

print("\n--- Simulating Immediate Hit on a DIFFERENT Endpoint (/checkout) ---")
# This passes instantly! Even though /search is blocked, /checkout has its own isolated bucket.
print(f"Hit 1 (/checkout): {'ALLOWED ✅' if limiter.is_allowed(user_ip, '/checkout') else 'BLOCKED ❌'}")

print("\n... Waiting 1.0 second for /search tokens to refill ...\n")
time.sleep(1.0)

print("--- Retrying /search Endpoint After Refill ---")
# This passes now because 1 token refilled during the sleep period
print(f"Hit 4 (/search): {'ALLOWED ✅' if limiter.is_allowed(user_ip, '/search') else 'BLOCKED ❌'}")

        
    