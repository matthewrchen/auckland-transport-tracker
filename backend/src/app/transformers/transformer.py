from datetime import datetime, timezone

def parse_realtime_data(data: list) -> list:
    """Processes realtime data according to database requirements

    Args: 
        data: entity list

    Returns:
        [list of trips, list of vehicles, list of alerts]
    """

    parsed_trips = []
    parsed_vehicles = []
    parsed_alerts = []
    update_time = datetime.now(timezone.utc).isoformat()
    for entity in data:
        # if label and license plate both empty, vehicle is irrelevant
        # if label is AMP ### and license plate empty, vehicle is train

        if (entity.get("trip_update")):
            nested_entity = entity["trip_update"]
            parsed_entity = {
                "trip_id": entity["id"],
                "route_id": nested_entity["trip"]["route_id"],
                "stop_id": nested_entity.get("stop_time_update", {}).get("stop_id"),
                "updated_at": update_time
            }

            parsed_trips.append(parsed_entity)
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
                "vehicle_label": nested_entity["vehicle"]["label"],
                "vehicle_license_plate" : nested_entity["vehicle"].get("license_plate"),
                "trip_id": nested_entity["trip"]["trip_id"],
                "route_id": nested_entity["trip"]["route_id"],
                "occupancy_status": nested_entity.get("occupancy_status"),
                "latitude": nested_entity["position"]["latitude"],
                "longitude": nested_entity["position"]["longitude"],
                "bearing": nested_entity["position"].get("bearing"),
                "odometer": nested_entity["position"].get("odometer"),
                "speed": int(nested_entity["position"]["speed"]),
                "updated_at": update_time
            }

            parsed_vehicles.append(parsed_entity)
        elif (entity.get("alert")):
            nested_entity = entity["alert"]
            parsed_entity = {
                "alert_id": entity["id"],
                "cause": nested_entity["cause"],
                "effect": nested_entity["effect"],
                "header_text": nested_entity["header_text"]["translation"][0]["text"],
                "effect_text": nested_entity.get("effect_detail", {}).get("translation", [{}])[0].get("text"),
                "description_text": nested_entity["description_text"]["translation"][0]["text"],
                "severity_level": nested_entity.get("severity_level"),
                "active_period": nested_entity["active_period"],
                "affected_stops": nested_entity["informed_entity"],
                "updated_at": update_time
            }

            parsed_alerts.append(parsed_entity)
    return [parsed_trips, parsed_vehicles, parsed_alerts]