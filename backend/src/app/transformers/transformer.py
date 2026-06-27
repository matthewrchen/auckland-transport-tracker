from datetime import datetime, timezone

def parse_vehicle_location_data(data: list) -> list:
    parsed_data = []
    update_time = datetime.now(timezone.utc).isoformat()
    for vehicle in data:
        # if label and license plate both empty, vehicle is irrelevant
        # if label is AMP ### and license plate empty, vehicle is train
        if (not vehicle.get("vehicle", {}).get("vehicle", {}).get("label") and not vehicle.get("vehicle", {}).get("vehicle", {}).get("license_plate")):
            continue

        parsed_vehicle = {
            "id": int(vehicle.get("id")), 
            "vehicle_id": vehicle.get("vehicle", {}).get("vehicle", {}).get("id"), 
            "vehicle_label": vehicle.get("vehicle", {}).get("vehicle", {}).get("label"), 
            "vehicle_license_plate": vehicle.get("vehicle", {}).get("vehicle", {}).get("license_plate"), 
            "vehicle_longitude": float(vehicle.get("vehicle", {}).get("position", {}).get("longitude")), 
            "vehicle_latitude": float(vehicle.get("vehicle", {}).get("position", {}).get("latitude")),
            "last_updated": update_time
        }
        parsed_data.append(parsed_vehicle)
    return parsed_data