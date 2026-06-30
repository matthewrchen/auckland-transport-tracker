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
                "trip_id": nested_entity["trip"]["trip_id"],
                "route_id": nested_entity["trip"]["route_id"],
                "updated_at": update_time,
                "raw_data": nested_entity
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
                "updated_at": update_time,
                "raw_data": nested_entity
            }

            parsed_alerts.append(parsed_entity)
    return [parsed_trips, parsed_vehicles, parsed_alerts]

parse_realtime_data