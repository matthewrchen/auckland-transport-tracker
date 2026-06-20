import { useRef, useEffect, useState } from 'react'

import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

import '../App.css'

export default function Map() {
  const mapRef = useRef();
  const mapContainerRef = useRef();

  useEffect(() => {
    mapRef.current = new mapboxgl.Map({
      accessToken: import.meta.env.VITE_DEVELOPMENT_TOKEN,
      container: mapContainerRef.current,

      center: [174.76, -36.86], 
      zoom: 11.4
    });

    return () => {
      mapRef.current.remove()
    }
  });

  return (
    <>
      <div id='map-container' ref={mapContainerRef}></div>
    </>
  );
}