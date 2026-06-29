from datetime import datetime, timezone

def parse_vehicle_location_data(data: list) -> list:
    parsed_data = []
    update_time = datetime.now(timezone.utc).isoformat()
    for entity in data:
        # if label and license plate both empty, vehicle is irrelevant
        # if label is AMP ### and license plate empty, vehicle is train

        if (entity.get("trip_update")):
            nested_entity = entity.get("trip_update")
        elif (entity.get("vehicle")):
            # TODO add more fallbacks later

            nested_entity = entity["vehicle"]
            # From observation two types of inactive vehicles:
            # 1. vehicles with no label and license plate
            # 2. vehicles with no trip id (also includes 1.), however did see bus without trip id moving
            # Note: could try occupancy status but what about old bus
            if (not nested_entity.get("trip")):
                continue
            parsed_entity = {
                "vehicle_id": entity["id"],
                "trip_id": nested_entity.get("trip", {}).get("trip_id"),
                "route_id": nested_entity.get("trip", {}).get("route_id"),
                "is_active": True,
                "updated_at": update_time,
                "raw_data": nested_entity
            }
        elif (entity.get("alert")):
            nested_entity = entity.get("alert")
        
        parsed_data.append(parsed_entity)
    return parsed_data