import styles from './VehicleInfoModal.module.css'

type prop = {
  vehicleID: string;
  vehicleLabel: string;
  vehicleLicensePlate: string;
}

export default function VehicleInfoModal( {vehicleID, vehicleLabel, vehicleLicensePlate}: prop) {
  return (
    <div className={styles.modal}>
      <div className={styles.modalHeader}>
        <h1 className={styles.modalTitle}>Vehicle Information</h1>
        <button className={styles.modalCloseButton}>x</button>
      </div>
      <div className={styles.modalBody}>
        <h2 className={styles.modalText}>{vehicleID ? "Vehicle ID: " + vehicleID : "Vehicle ID: Placeholder"}</h2>
        <h2 className={styles.modalText}>{vehicleLabel ? "Vehicle Label: " + vehicleLabel : "Vehicle Label: Placeholder"}</h2>
        <h2 className={styles.modalText}>{vehicleLicensePlate ? "Vehicle License Plate: " + vehicleLicensePlate : "Vehicle License Plate: Placeholder"}</h2>
      </div>
    </div>
  );
}