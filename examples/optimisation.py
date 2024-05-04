import time
from AminoLightPy import Client

email = "example_mail@gmail.com"
password = "example_password"

def measure_login_time(socket_enabled) -> int:
    client = Client(socket_enabled=socket_enabled)
    
    start_time = time.time()
    client.login(email, password)
    end_time = time.time()
    
    return end_time - start_time

time_with_socket_disabled = measure_login_time(socket_enabled=False)
time_with_default_settings = measure_login_time(socket_enabled=True)

# 0.4 "socket_enabled=False" better for scripts
print(f"Login time with socket_enabled=False: {time_with_socket_disabled:.2f} seconds")
# 0.9 without arguments better for bots
print(f"Login time with default settings: {time_with_default_settings:.2f} seconds")
