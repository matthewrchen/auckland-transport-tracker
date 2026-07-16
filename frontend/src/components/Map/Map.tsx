import { useRef, useEffect, useState } from 'react'

import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

import VehicleInfoModal from '../VehicleInfoModal/VehicleInfoModal'
import StopInfoModal from '../StopInfoModal/StopInfoModal'

import styles from './Map.module.css'

type VehicleProperties = Record<string, any>;

type VehicleRecord = {
  vehicle_longitude: number;
  vehicle_latitude: number;
  vehicle_label?: string;
  vehicle_license_plate?: string;
  vehicle_route?: string;
  vehicle_headsign?: string;
  vehicle_next_stop?: string;
  [key: string]: any;
};

type VehicleData = {
  vehicles: VehicleRecord[];
};

type StopProperties = Record<string, any>;

type StopRecord = {
  stop_longitude: number;
  stop_latitude: number;
  stop_id?: string;
  stop_name?: string;
  stop_code?: number;
  [key: string]: any;
};

type StopData = {
  stops: StopRecord[];
};

export type TripRecord = {
  trip_id?: string;
  arrival_time?: string;
  route_long_name?: string;
  route_short_name?: string;
  [key: string]: any;
}

type TripData = {
  trips: TripRecord[];
}

export default function Map() {
  const mapRef = useRef<mapboxgl.Map | null>(null);
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const vehicleGeojsonRef = useRef<any>({
    type: 'FeatureCollection',
    features: []
  });
  const stopGeojsonRef = useRef<any>({
    type: 'FeatureCollection',
    features: []
  });

  const [vehicleModalOpen, setVehicleModal] = useState(false);
  const [vehicleProperties, setVehicleProperties] = useState<VehicleProperties>({});
  const [stopModalOpen, setStopModal] = useState(false);
  const [stopProperties, setStopProperties] = useState<StopProperties>({});
  const [upcomingTrips, setUpcomingTrips] = useState<TripRecord[]>([]);

  useEffect(() => {
    if (!mapContainerRef.current) {
      return;
    }

    const map = new mapboxgl.Map({
      accessToken: import.meta.env.VITE_DEVELOPMENT_TOKEN,
      container: mapContainerRef.current,

      center: [174.76, -36.86],
      zoom: 11.4
    });

    mapRef.current = map;

    map.on('load', () => {

      map.addSource('vehicles-source', { type: 'geojson', data: vehicleGeojsonRef.current });
      map.addLayer({
        id: 'vehicles-layer',
        type: 'circle',
        source: 'vehicles-source',
        paint: {
          'circle-radius': 8,
          'circle-color': '#007cbf',
          'circle-stroke-width': 2,
          'circle-stroke-color': '#fff'
        }
      });

      map.addSource('stops-source', { type: 'geojson', data: stopGeojsonRef.current });
      map.addLayer({
        id: 'stops-layer',
        type: 'circle',
        source: 'stops-source',
        paint: {
          'circle-radius': 4,
          'circle-color': '#bf0000',
          'circle-stroke-width': 2,
          'circle-stroke-color': '#fff'
        }
      });

      map.addInteraction('clickVehicle', {
        type: 'click',
        target: { layerId: 'vehicles-layer' },
        handler: (feature: mapboxgl.InteractionEvent) => {
          setVehicleProperties((feature.feature?.properties as VehicleProperties | undefined) ?? {});

          setVehicleModal(true);
        }
      });
      map.addInteraction('clickStop', {
        type: 'click',
        target: { layerId: 'stops-layer' },
        handler: (feature: mapboxgl.InteractionEvent) => {
          setStopProperties((feature.feature?.properties as StopProperties | undefined) ?? {});

          sendMessage({"stop_id": feature.feature?.properties.stopId});
          setStopModal(true);
        }
      });

      connectWebSocket();
    });

    return () => {
      map.remove();
      wsRef.current?.close();
    };
  }, []);

  const connectWebSocket = () => {
    const ws = new WebSocket('ws://127.0.0.1:8000/ws/vehicles');
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('[FRONTEND] Connected to backend');
    };

    ws.onmessage = (event) => {
      try {
        const rawPayload: VehicleData | StopData | TripData = JSON.parse(event.data);
        if ('vehicles' in rawPayload) {
          updateBuses(rawPayload);
        }
        if ('stops' in rawPayload) {
          loadStops(rawPayload);
        }
        if ('trips' in rawPayload) {
          updateTrips(rawPayload)
        }
      } catch (error) {
        console.error('[FRONTEND] Error parsing API frame: ', error);
      }
    };

    ws.onclose = (e) => {
      console.log(`[FRONTEND] Websocket closed. Code: ${e.code}`);
    };

    ws.onerror = (err) => {
      console.error('[FRONTEND] Websocket encountered error: ', err);
      ws.close();
    };
  };

  const sendMessage = (payload: any) => { // maybe add type object for payload later
    const ws = wsRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(payload));
      console.log("Message sent");
    } else {
      console.log("Websocket not open");
    }
  }

  const updateBuses = (vehicleData: VehicleData) => {
    const vehicles = vehicleData['vehicles'];
    vehicleGeojsonRef.current.features = vehicles.map(vehicle => ({
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [vehicle['vehicle_longitude'], vehicle['vehicle_latitude']]
      },
      properties: {
        vehicleLabel: vehicle['vehicle_label'],
        vehicleLicensePlate: vehicle['vehicle_license_plate'],
        vehicleRoute: vehicle['vehicle_route'],
        vehicleHeadsign: vehicle['vehicle_headsign'],
        vehicleNextStop: vehicle['vehicle_next_stop']
      }
    }));

    const source = mapRef.current?.getSource('vehicles-source') as mapboxgl.GeoJSONSource | undefined;

    if (source) {
      source.setData(vehicleGeojsonRef.current);
    }
  };

  const loadStops = (stopData: StopData) => {
    const stops = stopData['stops'];
    stopGeojsonRef.current.features = stops.map(stop => ({
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [stop['stop_longitude'], stop['stop_latitude']]
      },
      properties: {
        stopId: stop['stop_id'],
        stopName: stop['stop_name'],
        stopCode: stop['stop_code']
      }
    }));

    const source = mapRef.current?.getSource('stops-source') as mapboxgl.GeoJSONSource | undefined;

    if (source) {
      source.setData(stopGeojsonRef.current)
    }
  };

  const updateTrips = (tripData: TripData) => {
    const trips = tripData['trips'];
    setUpcomingTrips(trips);
  };

  return (
    <>
      <div ref={mapContainerRef} className={styles.map}></div>

      {vehicleModalOpen && <VehicleInfoModal vehicleProperties={vehicleProperties} closeModal={() => setVehicleModal(false)} />}

      {stopModalOpen && <StopInfoModal stopProperties={stopProperties} upcomingTrips={upcomingTrips} closeModal={() => setStopModal(false)} />}
    </>
  );
}