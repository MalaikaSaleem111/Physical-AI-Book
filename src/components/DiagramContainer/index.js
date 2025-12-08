import React from 'react';
import styles from './styles.module.css';

/**
 * Component for containing ASCII diagrams and other conceptual diagrams
 * This component provides a styled container for diagrams in the book
 */
function DiagramContainer({title, children, type = "diagram"}) {
  return (
    <div className={`${styles.diagramContainer} ${styles[type]}`}>
      {title && <div className={styles.diagramTitle}>{title}</div>}
      <pre className={styles.diagramContent}>
        {children}
      </pre>
    </div>
  );
}

export default DiagramContainer;