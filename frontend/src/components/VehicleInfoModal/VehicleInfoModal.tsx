import styles from './VehicleInfoModal.module.css'

type prop = {
  vehicleProperties: Record<string, any>
  closeModal: () => void;
}

export default function VehicleInfoModal( { vehicleProperties, closeModal }: prop) {
  return (
    <div className={styles.modal}>
      <div className={styles.modalHeader}>
        <h1 className={styles.modalTitle}>Vehicle Information</h1>
        <button onClick={closeModal} className={styles.modalCloseButton}>x</button>
      </div>
      <div className={styles.modalBody}>
        <h2 className={styles.modalText}>{vehicleProperties["vehicleId"] ? "Vehicle ID: " + vehicleProperties["vehicleId"] : "Vehicle ID: Placeholder"}</h2>
        <h2 className={styles.modalText}>{vehicleProperties["vehicleLabel"] ? "Vehicle Label: " + vehicleProperties["vehicleLabel"] : "Vehicle Label: Placeholder"}</h2>
        <h2 className={styles.modalText}>{vehicleProperties["vehicleLicensePlate"] ? "Vehicle License Plate: " + vehicleProperties["vehicleLicensePlate"] : "Vehicle License Plate: Placeholder"}</h2>
        <h2 className={styles.modalText}>{vehicleProperties["vehicleRoute"] ? "Vehicle Route: " + vehicleProperties["vehicleRoute"] : "Vehicle Route: Placeholder"}</h2>
      </div>
    </div>
  );
}