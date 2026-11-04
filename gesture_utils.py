"""Shared MediaPipe landmark preprocessing.

Keep this preprocessing identical during collection and prediction.
"""
import numpy as np


def extract_landmarks(hand_landmarks):
    points = np.array(
        [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark],
        dtype=np.float32,
    )
    # Translate wrist to origin and normalize scale.
    points -= points[0]
    scale = float(np.max(np.abs(points)))
    if scale > 0:
        points /= scale
    return points.flatten()
