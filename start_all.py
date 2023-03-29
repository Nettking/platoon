from PlatoonVehicle import *


# Create an instance of PlatoonVehicle class
vehicle = PlatoonVehicle()
common_ip = "158.39.162."
unique_ip = ["127","157","181","197"]        
for ip in unique_ip:
    full_ip = common_ip + ip
    vehicle.start_script_on_other_vehicle(full_ip)