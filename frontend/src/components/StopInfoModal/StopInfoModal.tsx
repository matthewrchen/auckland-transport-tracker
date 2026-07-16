import styles from './StopInfoModal.module.css'

import type { TripRecord } from '../Map/Map'

type prop = {
  stopProperties: Record<string, any>;
  closeModal: () => void;
  upcomingTrips: TripRecord[];
}

export default function StopInfoModal( { stopProperties, closeModal, upcomingTrips }: prop) {
  return (
    <div className={styles.modal}>
      <div className={styles.modalHeader}>
        <h1 className={styles.modalTitle}>{stopProperties["stopName"]}</h1>
        <button onClick={closeModal} className={styles.modalCloseButton}>x</button>
      </div>
      <div className={styles.modalBody}>
        <h2 className={styles.modalText}>{stopProperties["stopCode"] ? "Stop Code: " + stopProperties["stopCode"] : "Stop Code: Placeholder"}</h2>
        <h1 className={styles.modalText}>Upcoming trips</h1>
        <ul className={styles.tripsBody}>
          {upcomingTrips.map((trip) => (<li key={trip["trip_id"]} className={styles.tripsText}>{trip["route_short_name"]} {trip["route_long_name"]} {trip["arrival_time"]}</li>))}
        </ul>
      </div>
    </div>
  );
}