"""Clean up raw class labels from training to readable Crop + Disease names."""
import json
import os

LABELS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'class_labels.json')

with open(LABELS_PATH) as f:
    labels = json.load(f)

clean = {}
for idx, raw in labels.items():
    parts = raw.lower()

    # Determine crop
    if parts.startswith('chilli') or parts.startswith('chili'):
        crop = 'Chilli'
    elif parts.startswith('coffee'):
        crop = 'Coffee'
    elif parts.startswith('paddy'):
        crop = 'Paddy'
    else:
        crop = 'Unknown'

    # Determine disease
    if 'healthy' in parts:
        disease = 'Healthy'
    elif 'anthracnose' in parts or 'anthacnose' in parts:
        disease = 'Anthracnose'
    elif 'red_spider_mite' in parts:
        disease = 'Red Spider Mite'
    elif 'rust' in parts:
        disease = 'Leaf Rust'
    elif 'bacterial_blight' in parts or 'bacterial leaf blight' in parts:
        disease = 'Bacterial Leaf Blight'
    elif 'brown_spot' in parts or 'brown spot' in parts:
        disease = 'Brown Spot'
    elif 'leaf_smut' in parts or 'leaf smut' in parts:
        disease = 'Leaf Smut'
    elif 'blast' in parts:
        disease = 'Blast Disease'
    elif 'leaf_scald' in parts:
        disease = 'Leaf Scald'
    elif 'tungro' in parts:
        disease = 'Tungro Virus'
    else:
        disease = raw.split('_')[-1]

    clean[idx] = f'{crop} {disease}'

# Fix redundant words
for idx in clean:
    clean[idx] = clean[idx].replace('Coffee Coffee ', 'Coffee ')
    clean[idx] = clean[idx].replace('Paddy Paddy ', 'Paddy ')

with open(LABELS_PATH, 'w') as f:
    json.dump(clean, f, indent=2)

print('Cleaned labels:')
for k, v in sorted(clean.items(), key=lambda x: int(x[0])):
    print(f'  {k}: {v}')
