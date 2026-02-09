import os
import glob
import json
import numpy as np
import cv2
import easyocr
import pandas as pd
from PIL import Image
from sentence_transformers import SentenceTransformer, util

# Configuration
JSON_DATA_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "tenants_detailed.json")
IMAGES_DIR = "C:/Users/srira/Downloads/mall_img"

def main():
    print("--- CLI Mall Analysis Runner ---")
    
    # 1. Load Data
    if not os.path.exists(JSON_DATA_PATH):
        print(f"Error: JSON data file not found at {JSON_DATA_PATH}")
        return
    with open(JSON_DATA_PATH, 'r', encoding='utf-8') as f:
        tenants = json.load(f)
    print(f"Loaded {len(tenants)} tenants from JSON.")

    # 2. Load Images
    image_files = glob.glob(os.path.join(IMAGES_DIR, "*.png"))
    if not image_files:
        print(f"No PNG images found in {IMAGES_DIR}")
        return
    print(f"Found {len(image_files)} images to analyze.")

    # 3. Load Models
    print("Loading models (this may take a moment)...")
    reader = easyocr.Reader(['en'], gpu=False, verbose=False) # GPU=False and verbose=False to be safe
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

    # 4. Analyze
    json_names = [t['name'] for t in tenants if t['name']]
    if not json_names:
        print("No valid tenant names in JSON.")
        return

    json_embeddings = sbert_model.encode(json_names, convert_to_tensor=True)

    for img_path in image_files:
        print(f"\nAnalyzing: {os.path.basename(img_path)}")
        try:
            image = Image.open(img_path).convert("RGB")
            img_np = np.array(image)
            
            # OCR
            results = reader.readtext(img_np)
            ocr_texts = [res[1] for res in results if res[2] > 0.3]
            print(f"  > Detected {len(ocr_texts)} text regions.")
            
            if not ocr_texts:
                continue

            # Compare
            ocr_embeddings = sbert_model.encode(ocr_texts, convert_to_tensor=True)
            cosine_scores = util.cos_sim(json_embeddings, ocr_embeddings)
            
            verified_count = 0
            print("  > Verified Tenants:")
            for i, name in enumerate(json_names):
                best_score = float(cosine_scores[i].max())
                best_idx = int(cosine_scores[i].argmax())
                best_match = ocr_texts[best_idx]
                
                if best_score > 0.6:
                    print(f"    [OK] {name} (Match: '{best_match}', Score: {best_score:.2f})")
                    verified_count += 1
            
            print(f"  > Total Verified in this image: {verified_count}")

        except Exception as e:
            print(f"Error processing {img_path}: {e}")

if __name__ == "__main__":
    main()
