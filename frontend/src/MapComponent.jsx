import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icon issue with Leaflet
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow
});

L.Marker.prototype.options.icon = DefaultIcon;

const MapComponent = ({ token }) => {
  const [encroachments, setEncroachments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // We will use a dummy fetch call for now as the API needs a file upload.
    // This demonstrates the authentication and data retrieval flow.
    const fetchEncroachmentData = async () => {
      setLoading(true);
      try {
        const dummyData = [
          { "type": "building", "location": "POINT (-73.99549999999999 40.735400000000006)", "affected_area_sq_m": 0.0009492, "nearest_boundary_id": "Main Road" },
          { "type": "shed", "location": "POINT (-74.006 40.7128)", "affected_area_sq_m": 4.000000000009777e-07, "nearest_boundary_id": "Main Road" }
        ];
        
        // This is where you would make a real API call
        // const response = await fetch('http://localhost:8000/protected-data', {
        //   headers: {
        //     Authorization: `Bearer ${token}`
        //   }
        // });
        // const data = await response.json();
        // setEncroachments(data.encroachments);

        // For this PoC, we will simulate the data retrieval
        setEncroachments(dummyData);
      } catch (error) {
        console.error("Failed to fetch data", error);
        alert("Failed to fetch data from API. See console for details.");
      }
      setLoading(false);
    };

    if (token) {
      fetchEncroachmentData();
    }
  }, [token]);

  if (loading) {
    return <div>Loading map data...</div>;
  }
  
  // Parse the location string "POINT (lon lat)" into a Leaflet-friendly [lat, lon] array
  const parsePoint = (locationStr) => {
    const coords = locationStr.match(/\(([^)]+)\)/)[1].split(' ').map(parseFloat);
    return [coords[1], coords[0]];
  };

  const center = encroachments.length > 0 ? parsePoint(encroachments[0].location) : [40.7128, -74.006];

  return (
    <MapContainer center={center} zoom={13} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      />
      {encroachments.map((enc, index) => (
        <Marker key={index} position={parsePoint(enc.location)}>
          <Popup>
            <b>Encroachment Detected</b><br />
            Type: {enc.type}<br />
            Area: {enc.affected_area_sq_m.toFixed(4)} sq m<br />
            Near: {enc.nearest_boundary_id}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default MapComponent;