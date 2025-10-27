from flask import Flask, render_template, request, send_file, jsonify
from rembg import remove
from PIL import Image, ImageOps, ImageFilter
import pillow_heif
import io, time, os

pillow_heif.register_heif_opener()
app = Flask(__name__)

# simple helper
def remove_bg(image):
    image = ImageOps.exif_transpose(image)
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    output_bytes = remove(buf.read())
    output = Image.open(io.BytesIO(output_bytes))
    output = output.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=2))
    return output


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """Handle file upload + return processed image."""
    file = request.files["image"]
    image = Image.open(file).convert("RGB")

    # Simulate progress to frontend (realistic example)
    total_steps = 4
    progress_file = "progress.txt"
    with open(progress_file, "w") as f:
        f.write("0")

    # Step 1: start
    time.sleep(0.3)
    with open(progress_file, "w") as f:
        f.write("25")

    # Step 2: remove background
    output = remove_bg(image)
    with open(progress_file, "w") as f:
        f.write("75")

    # Step 3: finish up
    buf = io.BytesIO()
    output.save(buf, format="PNG")
    buf.seek(0)
    with open(progress_file, "w") as f:
        f.write("100")

    return send_file(buf, mimetype="image/png", as_attachment=False)


@app.route("/progress")
def progress():
    """Return current progress percentage."""
    progress_file = "progress.txt"
    if os.path.exists(progress_file):
        with open(progress_file) as f:
            return jsonify({"progress": int(f.read().strip())})
    return jsonify({"progress": 0})


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
