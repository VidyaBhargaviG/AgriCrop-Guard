#!/usr/bin/env python3
"""Quick test of the hybrid detector."""
import os, sys

sys.path.insert(0, '.')
from backend.ai_model.detector import _load_model, _predict_with_cnn, _analyze_colors, predict_disease

_load_model()

test_images = [
    os.path.expanduser('~/Downloads/healthy.jpeg'),
    os.path.expanduser('~/Downloads/a.jpeg'),
    os.path.expanduser('~/Downloads/b.jpeg'),
    os.path.expanduser('~/Downloads/c.jpeg'),
]

for img in test_images:
    if not os.path.exists(img):
        continue
    print(f"\n{'='*60}")
    print(f"IMAGE: {os.path.basename(img)}")
    print('='*60)

    cnn = _predict_with_cnn(img)
    print("CNN top-3:", [(lbl, f"{c*100:.1f}%") for lbl, c in cnn[:3]])

    colors = _analyze_colors(img)
    print("Color top-3:", [(n, f"{c*100:.1f}%") for n, c in colors[:3]])

    for crop in ['Paddy', 'Chilli', 'Coffee', None]:
        r = predict_disease(img, crop_filter=crop)
        tag = crop or 'ALL'
        preds = r.get('predictions', [])
        if preds:
            top = preds[0]
            print(f"  [{tag:6s}] {top['crop']} {top['disease']}: {top['confidence']*100:.1f}%")
        else:
            print(f"  [{tag:6s}] No predictions")
