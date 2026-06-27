import { useRef, useEffect, useState } from 'react'

import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

import VehicleInfoModal from '../VehicleInfoModal/VehicleInfoModal'

import styles from './Map.module.css'

export default function Map() {
  const mapRef = useRef();
  const mapContainerRef = useRef();
  const wsRef = useRef();
  const geojsonRef = useRef({
    type: 'FeatureCollection',
    features: []
  });

  const [busId, setBusId] = useState(null);
  const [busLabel, setBusLabel] = useState(null);
  const [busLicensePlate, setBusLicensePlate] = useState(null);

  useEffect(() => {
    mapRef.current = new mapboxgl.Map({
      accessToken: import.meta.env.VITE_DEVELOPMENT_TOKEN,
      container: mapContainerRef.current,

      center: [174.76, -36.86], 
      zoom: 11.4
    });

    mapRef.current.on('load', () => {
      mapRef.current.addSource('buses-source', {type: 'geojson', data: geojsonRef.current});
      mapRef.current.addLayer({
        id: 'buses-layer',
        type: 'circle',
        source: 'buses-source',
        paint: {
          'circle-radius': 8,
          'circle-color': '#007cbf',
          'circle-stroke-width': 2,
          'circle-stroke-color': '#fff'
        }
      });
      mapRef.current.addInteraction('click', {
        type: 'click',
        target: { layerId: 'buses-layer' },
        handler: (feature) => {
          setBusId(feature.feature.properties['busId'])
          setBusLabel(feature.feature.properties['busLabel'])
          setBusLicensePlate(feature.feature.properties['busLicensePlate'])
        }
      });

      connectWebSocket();
    });

    return () => {
      if (mapRef.current) mapRef.current.remove();
      if (wsRef.current) wsRef.current.close();
    }
  }, []);

  const connectWebSocket = () => {
    const ws = new WebSocket('ws://127.0.0.1:8000/ws/buses');
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('[FRONTEND] Connected to backend');
    };

    ws.onmessage = (event) => {
      try {
        const rawPayload = JSON.parse(event.data);
        updateBuses(rawPayload)
      } catch (error) {
        console.error('[FRONTEND] Error parsing API frame: ', error);
      }
    };

    ws.onclose = (e) => {
      console.log(`[FRONTEND] Websocket closed. Code: ${e.code}`);
    }

    ws.onerror = (err) => {
      console.error('[FRONTEND] Websocket encountered error: ', err);
      ws.close();
    }
  };

  const updateBuses = (busData) => {
    const buses = busData['buses']
    geojsonRef.current.features = buses.map(bus => ({
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [bus['vehicle_longitude'], bus['vehicle_latitude']]
      },
      properties: {
        busId: bus['vehicle_id'],
        busLabel: bus['vehicle_label'],
        busLicensePlate: bus['vehicle_license_plate']
      }
    }));
    if (mapRef.current.getSource('buses-source')) {
      mapRef.current.getSource('buses-source').setData(geojsonRef.current);
    }
  };

  return (
    <>
      <div ref={mapContainerRef} className={styles.map}></div>
      <VehicleInfoModal vehicleID={busId} vehicleLabel={busLabel} vehicleLicensePlate={busLicensePlate} />
    </>
  );
}