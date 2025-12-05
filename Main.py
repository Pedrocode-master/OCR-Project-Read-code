# ============================
# OCR FOR DARK MODE SCREENSHOTS (Acode, VSCode, etc)
# Solution: Invert colors before processing and correct EXIF orientation
# ============================
try:
    from PIL import Image, ImageOps
    import cv2
    import pytesseract
    import numpy as np
except ImportError:
    print("📦 Installing libraries...")
    !pip install pillow opencv-python pytesseract --quiet
    from PIL import Image, ImageOps
    import cv2
    import pytesseract
    import numpy as np

from google.colab import files
from IPython.display import display
import matplotlib.pyplot as plt
import re
from datetime import datetime

# ============================
# FUNCTION TO CLEAN TEXT
# ============================
def clean_text(text: str, remove_chars=None) -> str:
    """
    Removes unwanted characters from the text while keeping line breaks.
    """
    remove_chars = remove_chars or ['|', ':']
    pattern = f"[{''.join(re.escape(c) for c in remove_chars)}]"
    cleaned = re.sub(pattern, '', text)
    # Keep line breaks and remove extra spaces
    cleaned = '\n'.join(re.sub(r'[ ]+', ' ', line).strip() for line in cleaned.splitlines())
    return cleaned

# ============================
# PART 1: UPLOAD
# ============================
print("📤 Upload your Acode screenshot:")
uploaded = files.upload()
file_name = list(uploaded.keys())[0]
img_raw = Image.open(file_name)
img_original = ImageOps.exif_transpose(img_raw)  # Correct rotation via EXIF
print(f"\n✅ File: {file_name}")
print(f"📏 Size: {img_original.size}")

# ============================
# PART 2: DETECT DARK MODE
# ============================
arr = np.array(img_original)
average_brightness = arr.mean()
print(f"\n🔍 Analysis: Average brightness = {average_brightness:.1f}")
is_dark_mode = average_brightness < 128
if is_dark_mode:
    print("🌙 DETECTED: Dark Mode (dark background, light text)")
    print("✨ Applying color inversion...")
else:
    print("☀️ DETECTED: Light Mode (light background, dark text)")

# ============================
# PART 3: INVERT COLORS IF NECESSARY
# ============================
if is_dark_mode:
    img_inverted = ImageOps.invert(img_original.convert('RGB'))
    img_to_process = img_inverted
    print("✅ Colors inverted!")
else:
    img_to_process = img_original

# Show comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].imshow(img_original)
axes[0].set_title('Original', fontsize=12)
axes[0].axis('off')
axes[1].imshow(img_to_process)
axes[1].set_title('After Inversion (ready for OCR)', fontsize=12)
axes[1].axis('off')
plt.tight_layout()
plt.show()

# ============================
# PART 4: ADVANCED PREPROCESSING
# ============================
processed_pil = img_to_process.convert('L')  # Convert to grayscale
processed_pil = np.array(processed_pil)
processed_pil = cv2.threshold(processed_pil, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
processed_pil = Image.fromarray(processed_pil)

# ============================
# PART 5: OCR WITH TESSERACT
# ============================
print("\n🤖 Executing OCR with Tesseract...")

configs = [
    ('Standard', r'--oem 3 --psm 6'),
    ('Source Code', r'--oem 3 --psm 6 -c preserve_interword_spaces=1'),
    ('Single Block', r'--oem 3 --psm 3'),
]

results = {}
for name, config in configs:
    try:
        text = pytesseract.image_to_string(processed_pil, config=config)
        text = clean_text(text)  # Clean unwanted characters while keeping line breaks
        results[name] = text
        print(f"✅ {name}: {len(text)} characters extracted")
    except Exception as e:
        print(f"❌ {name}: Error - {e}")
        results[name] = ""

# ============================
# PART 6: CHOOSE BEST RESULT
# ============================
print("\n📈 Analyzing results...")

def score_code(text):
    if not text or len(text.strip()) < 10:
        return 0
    score = 0
    keywords = ['function', 'const', 'let', 'var', 'if', 'else', 'for',
                'while', 'return', 'class', 'import', 'export', 'async',
                'await', 'new', 'this', 'document', 'window']
    for kw in keywords:
        if kw in text.lower():
            score += 5
    code_chars = ['{', '}', '(', ')', ';', '=', '[', ']', '/', '*']
    for char in code_chars:
        score += text.count(char) * 0.5
    lines = text.split('\n')
    non_empty = [l for l in lines if l.strip()]
    if len(non_empty) > 0:
        score += len(non_empty) * 2
    return score

scores = {name: score_code(text) for name, text in results.items()}
best_name = max(scores, key=scores.get)
best_text = results[best_name]

print(f"\n🏆 Best result after cleaning: {best_name}")
print(f"   Score: {scores[best_name]:.1f}")
for name, score in scores.items():
    print(f"   - {name}: {score:.1f}")

# ============================
# PART 7: DISPLAY RESULT
# ============================
print("\n" + "="*70)
print("📝 EXTRACTED TEXT")
print("="*70)
print(best_text)
print("="*70)

# ============================
# PART 8: SAVE RESULT
# ============================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"extracted_text_{timestamp}.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(best_text)
print(f"\n💾 Saved as: {output_file}")
files.download(output_file)

# Final statistics
print(f"\n📊 Statistics:")
print(f"   - Total characters: {len(best_text)}")
print(f"   - Total lines: {len(best_text.splitlines())}")
print(f"   - Non-empty lines: {len([l for l in best_text.splitlines() if l.strip()])}")
