def parse_vehicle_location_data(data: list) -> list:
    parsed_data = []
    for vehicle in data:
        parsed_vehicle = {
            "id": int(vehicle.get("id")), 
            "vehicle_id": vehicle.get("vehicle", {}).get("vehicle", {}).get("id"), 
            "vehicle_label": vehicle.get("vehicle", {}).get("vehicle", {}).get("label"), 
            "vehicle_license_plate": vehicle.get("vehicle", {}).get("vehicle", {}).get("license_plate"), 
            "vehicle_longitude": float(vehicle.get("vehicle", {}).get("position", {}).get("longitude")), 
            "vehicle_latitude": float(vehicle.get("vehicle", {}).get("position", {}).get("latitude"))
        }
        parsed_data.append(parsed_vehicle)
    return parsed_data