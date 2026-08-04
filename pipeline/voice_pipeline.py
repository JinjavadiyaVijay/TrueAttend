from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st
import logging

# ─── Config ───────────────────────────────────────────────────────
VOICE_THRESHOLD = 0.65    # Minimum cosine similarity for a match
MIN_SEGMENT_SECONDS = 0.5 # Minimum audio segment length in seconds

logger = logging.getLogger(__name__)


# ─── Model Loading ────────────────────────────────────────────────
@st.cache_resource
def load_voice_encoder():
    """Load the Resemblyzer voice encoder model."""
    logger.info("Loading voice encoder...")
    encoder = VoiceEncoder()
    logger.info("Voice encoder loaded successfully.")
    return encoder


# ─── Single Embedding ────────────────────────────────────────────
def get_voice_embedding(audio_bytes):
    """
    Extract a voice embedding from audio bytes.
    Returns list (JSON-serializable) or None on failure.
    """
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

        if len(audio) < sr * MIN_SEGMENT_SECONDS:
            logger.warning("Audio too short for voice embedding.")
            st.warning("Audio is too short. Please record at least 1 second.")
            return None

        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)

        logger.info(f"Voice embedding extracted: {embedding.shape}")
        return embedding.tolist()

    except Exception as e:
        logger.error(f"Voice embedding extraction failed: {e}")
        st.error(f"Voice processing error: {str(e)}")
        return None


# ─── Speaker Identification ──────────────────────────────────────
def identify_speaker(new_embedding, candidates_dict, threshold=VOICE_THRESHOLD):
    """
    Match a voice embedding against a dictionary of candidates.
    
    Args:
        new_embedding: numpy array or list
        candidates_dict: {student_id: stored_embedding}
        threshold: minimum cosine similarity
    
    Returns:
        (student_id, score) or (None, best_score)
    """
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    new_emb = np.array(new_embedding)
    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            stored_emb = np.array(stored_embedding)
            similarity = np.dot(new_emb, stored_emb)

            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    logger.info(f"Best voice match: student_id={best_sid}, score={best_score:.4f}, threshold={threshold}")

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


# ─── Bulk Audio Processing ───────────────────────────────────────
def process_bulk_audio(audio_bytes, candidates_dict, threshold=VOICE_THRESHOLD):
    """
    Process a bulk audio recording, splitting into segments and identifying speakers.
    
    Args:
        audio_bytes: raw audio bytes
        candidates_dict: {student_id: voice_embedding}
        threshold: minimum cosine similarity
    
    Returns:
        dict {student_id: best_score} for identified speakers
    """
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        logger.info(f"Bulk audio: {len(segments)} segments found.")

        identified_results = {}

        for start, end in segments:
            # Skip segments shorter than minimum
            if (end - start) < sr * MIN_SEGMENT_SECONDS:
                continue

            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(embedding, candidates_dict, threshold)

            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        logger.info(f"Bulk audio result: {len(identified_results)} speakers identified.")
        return identified_results

    except Exception as e:
        logger.error(f"Bulk audio processing failed: {e}")
        st.error(f"Voice processing error: {str(e)}")
        return {}