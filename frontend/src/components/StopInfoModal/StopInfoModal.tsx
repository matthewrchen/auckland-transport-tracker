import styles from './StopInfoModal.module.css'

type prop = {
  stopProperties: Record<string, any>
  closeModal: () => void;
}

export default function StopInfoModal( { stopProperties, closeModal }: prop) {
  return (
    <div className={styles.modal}>
      <div className={styles.modalHeader}>
        <h1 className={styles.modalTitle}>{stopProperties["stopName"]}</h1>
        <button onClick={closeModal} className={styles.modalCloseButton}>x</button>
      </div>
      <div className={styles.modalBody}>
        <h2 className={styles.modalText}>{stopProperties["stopCode"] ? "Stop Code: " + stopProperties["stopCode"] : "Stop Code: Placeholder"}</h2>
      </div>
    </div>
  );
}