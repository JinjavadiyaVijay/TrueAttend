import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
import logging

from database.db import get_all_students

# ─── Config ───────────────────────────────────────────────────────
FACE_THRESHOLD = 0.6      # Max L2 distance to consider a match
MIN_STUDENTS_FOR_SVM = 2  # Need at least 2 classes for SVM

logger = logging.getLogger(__name__)


# ─── Model Loading ────────────────────────────────────────────────
@st.cache_resource
def load_dlib_model():
    """Load dlib face detector, shape predictor, and face recognition model."""
    logger.info("Loading dlib models...")

    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    logger.info("Dlib models loaded successfully.")
    return detector, sp, facerec


# ─── Embedding Extraction ────────────────────────────────────────
def get_face_embeddings(image_np):
    """
    Extract 128-dim face embeddings from an image.
    Returns list of numpy arrays, one per detected face.
    """
    try:
        detector, sp, facerec = load_dlib_model()
        faces = detector(image_np, 1)

        logger.info(f"Detected {len(faces)} face(s) in image.")

        encodings = []
        for face in faces:
            shape = sp(image_np, face)
            face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
            encodings.append(np.array(face_descriptor))

        return encodings
    except Exception as e:
        logger.error(f"Face embedding extraction failed: {e}")
        return []


# ─── Classifier Training ─────────────────────────────────────────
@st.cache_resource
def get_trained_model():
    """
    Train an SVM classifier on all registered students' face embeddings.
    Returns dict with 'clf', 'x', 'y' or None if insufficient data.
    """
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        logger.warning("No students in database — cannot train model.")
        return None

    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) == 0:
        logger.warning("No face embeddings found — cannot train model.")
        return None

    unique_classes = len(set(y))
    logger.info(f"Training classifier with {len(X)} samples, {unique_classes} classes.")

    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    if unique_classes >= MIN_STUDENTS_FOR_SVM:
        try:
            clf.fit(X, y)
            logger.info("SVM classifier trained successfully.")
        except ValueError as e:
            logger.error(f"SVM training failed: {e}")
            return {'clf': None, 'x': X, 'y': y}
    else:
        logger.info(f"Only {unique_classes} class(es) — SVM skipped, using distance-only matching.")

    return {'clf': clf if unique_classes >= MIN_STUDENTS_FOR_SVM else None, 'x': X, 'y': y}


def train_classifier():
    """Clear cached model and retrain."""
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


# ─── Prediction ───────────────────────────────────────────────────
def predict_attendance(class_image_np):
    """
    Detect faces and match against trained model.
    
    Returns:
        detected: dict {student_id: True} for matched students
        all_students: sorted list of all known student IDs
        num_faces: number of faces detected in the image
    """
    try:
        embeddings = get_face_embeddings(class_image_np)
    except Exception as e:
        logger.error(f"Face detection failed: {e}")
        return {}, [], 0

    detected_student = {}
    model_data = get_trained_model()

    if not model_data:
        return {}, [], len(embeddings)

    clf = model_data.get('clf')
    x_train = model_data['x']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for embedding in embeddings:
        predicted_id = None

        if clf is not None and len(all_students) >= MIN_STUDENTS_FOR_SVM:
            # Use SVM for prediction
            predicted_id = int(clf.predict([embedding])[0])
        elif len(all_students) == 1:
            # Only one student — use distance matching directly
            predicted_id = int(all_students[0])
        else:
            continue

        # Verify with L2 distance
        try:
            idx = y_train.index(predicted_id)
            student_embedding = x_train[idx]
            distance = np.linalg.norm(student_embedding - embedding)

            logger.info(f"Student {predicted_id}: distance={distance:.4f}, threshold={FACE_THRESHOLD}")

            if distance <= FACE_THRESHOLD:
                detected_student[predicted_id] = True
        except (ValueError, IndexError) as e:
            logger.error(f"Matching error for ID {predicted_id}: {e}")
            continue

    logger.info(f"Attendance result: {len(detected_student)} matched out of {len(embeddings)} faces.")
    return detected_student, all_students, len(embeddings)