"""
Local web server for uploading an image and getting measurements.
"""
from __future__ import annotations

import argparse
import uuid
from pathlib import Path

from flask import Flask, abort, render_template_string, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

from config import INPUT_DIR, OUTPUT_DIR
from main import IndustrialToolAnalyzer
from geometry_calculator import GeometryCalculator
from smart_calculator import SmartCalculator

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / INPUT_DIR
OUTPUT_DIR_PATH = BASE_DIR / OUTPUT_DIR

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 MB

analyzer: IndustrialToolAnalyzer | None = None
calculator = GeometryCalculator()
smart_calculator = SmartCalculator()
results_cache: dict[str, dict] = {}

DATASET_DIR = BASE_DIR / "Dataset"


def _is_allowed(filename: str) -> bool:
    suffix = Path(filename).suffix.lower()
    return suffix in ALLOWED_EXTENSIONS


def _save_upload(file_storage) -> str:
    filename = secure_filename(file_storage.filename or "")
    if not filename:
        raise ValueError("Missing filename.")
    if not _is_allowed(filename):
        raise ValueError("Unsupported file type.")

    suffix = Path(filename).suffix.lower()
    stem = Path(filename).stem
    unique_name = f"{stem}_{uuid.uuid4().hex}{suffix}"
    target = UPLOAD_DIR / unique_name
    file_storage.save(target)
    return unique_name


def _dataset_images() -> list[str]:
    if not DATASET_DIR.exists():
        return []
    files = []
    for p in DATASET_DIR.iterdir():
        if p.is_file() and p.suffix.lower() in ALLOWED_EXTENSIONS:
            files.append(p.name)
    return sorted(files)


def _to_mm(value: float, unit: str) -> float:
    if unit == "m":
        return value * 1000
    if unit == "cm":
        return value * 10
    return value


def _manual_calculation(form) -> dict:
    shape = (form.get("shape") or "").strip().lower()
    unit = (form.get("unit") or "mm").strip().lower()
    if unit not in {"mm", "cm", "m"}:
        unit = "mm"

    def _num(field: str) -> float | None:
        raw = (form.get(field) or "").strip()
        if not raw:
            return None
        try:
            return float(raw)
        except ValueError:
            return None

    include_top_bottom = (form.get("include_top_bottom") == "on")

    if shape == "cylinder":
        diameter = _num("cylinder_diameter")
        height = _num("cylinder_height")
        if diameter is None or height is None:
            raise ValueError("Cylinder requires diameter and height.")
        return calculator.calculate_cylinder_surface_area(
            _to_mm(diameter, unit),
            _to_mm(height, unit),
            include_top_bottom=include_top_bottom,
        )

    if shape == "rectangular":
        length = _num("rect_length")
        width = _num("rect_width")
        height = _num("rect_height")
        if length is None or width is None or height is None:
            raise ValueError("Rectangular requires length, width, and height.")
        return calculator.calculate_rectangular_surface_area(
            _to_mm(length, unit),
            _to_mm(width, unit),
            _to_mm(height, unit),
            include_top_bottom=include_top_bottom,
        )

    if shape == "frustum":
        top_d = _num("frustum_top_diameter")
        bottom_d = _num("frustum_bottom_diameter")
        height = _num("frustum_height")
        if top_d is None or bottom_d is None or height is None:
            raise ValueError("Frustum requires top diameter, bottom diameter, and height.")
        return calculator.calculate_frustum_surface_area(
            _to_mm(top_d, unit),
            _to_mm(bottom_d, unit),
            _to_mm(height, unit),
        )

    if shape == "bucket":
        top_d = _num("bucket_top_diameter")
        bottom_d = _num("bucket_bottom_diameter")
        height = _num("bucket_height")
        if top_d is None or bottom_d is None or height is None:
            raise ValueError("Bucket requires top diameter, bottom diameter, and height.")
        return calculator.calculate_bucket_surface_area(
            _to_mm(top_d, unit),
            _to_mm(bottom_d, unit),
            _to_mm(height, unit),
        )

    if shape == "scoop":
        top_d = _num("scoop_top_diameter")
        bottom_d = _num("scoop_bottom_diameter")
        height = _num("scoop_height")
        if top_d is None or bottom_d is None or height is None:
            raise ValueError("Scoop requires top diameter, bottom diameter, and height.")
        return calculator.calculate_scoop_surface_area(
            _to_mm(top_d, unit),
            _to_mm(bottom_d, unit),
            _to_mm(height, unit),
        )

    raise ValueError("Please choose a valid shape.")


def _get_analyzer() -> IndustrialToolAnalyzer:
    global analyzer
    if analyzer is None:
        analyzer = IndustrialToolAnalyzer()
    return analyzer


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None
    uploaded_name = None
    dataset_files = _dataset_images()

    if request.method == "POST":
        dataset_file = (request.form.get("dataset_file") or "").strip()
        file = request.files.get("image")
        try:
            if dataset_file:
                uploaded_name = dataset_file
                image_path = str(DATASET_DIR / dataset_file)
            else:
                if not file:
                    raise ValueError("Please choose an image to upload.")
                uploaded_name = _save_upload(file)
                image_path = str(UPLOAD_DIR / uploaded_name)

            result = _get_analyzer().process_image(image_path)
            if result is None:
                error = "Processing failed. Check the server logs for details."
            else:
                results_cache[uploaded_name] = result
        except Exception as exc:
            error = str(exc)

    return render_template_string(
        """
        <!doctype html>
        <html>
          <head>
            <meta charset="utf-8">
            <title>Equipment Measurement Studio</title>
            <style>
              :root {
                --bg: #0f172a;
                --panel: #111827;
                --card: #0b1220;
                --muted: #94a3b8;
                --accent: #38bdf8;
                --text: #e2e8f0;
              }
              body { font-family: "Segoe UI", Arial, sans-serif; margin: 0; background: var(--bg); color: var(--text); }
              .topbar { padding: 16px 24px; border-bottom: 1px solid #1f2937; display: flex; align-items: center; gap: 16px; }
              .brand { font-weight: 700; letter-spacing: 0.5px; }
              .nav a { text-decoration: none; color: var(--text); margin-right: 12px; padding: 6px 10px; border-radius: 6px; background: #1f2937; }
              .wrap { display: grid; grid-template-columns: 320px 1fr; gap: 18px; padding: 18px; }
              .sidebar, .content-card { background: var(--panel); border-radius: 12px; padding: 16px; border: 1px solid #1f2937; }
              .card { background: var(--card); border-radius: 12px; padding: 16px; border: 1px solid #1f2937; margin-bottom: 16px; }
              .btn { background: var(--accent); color: #00202b; border: none; padding: 8px 12px; border-radius: 8px; font-weight: 600; cursor: pointer; }
              .muted { color: var(--muted); font-size: 13px; }
              .error { color: #f87171; }
              img { max-width: 100%; height: auto; border-radius: 10px; }
              table { width: 100%; border-collapse: collapse; }
              th, td { border-bottom: 1px solid #1f2937; padding: 8px; text-align: left; }
              th { color: var(--muted); font-weight: 600; }
              select, input { width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #1f2937; background: #0b1220; color: var(--text); }
              .stack { display: grid; gap: 10px; }
            </style>
          </head>
          <body>
            <div class="topbar">
              <div class="brand">Equipment Measurement Studio</div>
              <div class="nav">
                <a href="{{ url_for('index') }}">OCR Studio</a>
                <a href="{{ url_for('manual_calculator') }}">Manual Calculator</a>
              </div>
            </div>

            <div class="wrap">
              <div class="sidebar">
                <div class="card">
                  <h3>Upload Image</h3>
                  <form method="post" enctype="multipart/form-data" class="stack">
                    <input type="file" name="image" accept="image/*" required>
                    <button class="btn" type="submit">Run OCR</button>
                    <span class="muted">Use clear images with visible dimensions.</span>
                  </form>
                </div>

                {% if dataset_files %}
                <div class="card">
                  <h3>Dataset Image</h3>
                  <form method="post" class="stack">
                    <select name="dataset_file" required>
                      {% for f in dataset_files %}
                        <option value="{{ f }}">{{ f }}</option>
                      {% endfor %}
                    </select>
                    <button class="btn" type="submit">Run OCR</button>
                  </form>
                </div>
                {% endif %}

                {% if error %}
                  <div class="card error">Error: {{ error }}</div>
                {% endif %}
              </div>

              <div class="content-card">
                {% if uploaded_name %}
                  <div class="card">
                    <h3>Input Image</h3>
                    <img src="{{ url_for('files', dir_key='input', filename=uploaded_name) }}" alt="uploaded">
                  </div>
                {% endif %}

                {% if result %}
                  <div class="card">
                    <h3>Labeled Output</h3>
                    <img src="{{ url_for('files', dir_key='output', filename=output_name) }}" alt="labeled">
                  </div>

                  <div class="card">
                    <h3>Detected Dimensions</h3>
                    <table>
                      <tr>
                        <th>Value</th>
                        <th>Unit</th>
                        <th>Value (mm)</th>
                        <th>Confidence</th>
                        <th>Text</th>
                      </tr>
                      {% for d in result['dimensions_extracted'] %}
                      <tr>
                        <td>{{ d['value'] }}</td>
                        <td>{{ d['unit'] }}</td>
                        <td>{{ d['value_mm'] }}</td>
                        <td>{{ "%.2f"|format(d['confidence']) }}</td>
                        <td>{{ d['text'] }}</td>
                      </tr>
                      {% endfor %}
                    </table>
                  </div>

                  <div class="card">
                    <h3>Calculated Surface Area</h3>
                    {% if result['calculations'] %}
                      {% for calc in result['calculations'] %}
                        <p><strong>Shape:</strong> {{ calc['shape'] }}</p>
                        <p><strong>Total Area:</strong> {{ "%.2f"|format(calc['total_area_cm2']) }} cm2</p>
                        <p><strong>Total Area:</strong> {{ "%.6f"|format(calc['total_area_m2']) }} m2</p>
                        <p><strong>Dimensions:</strong> {{ calc['dimensions'] }}</p>
                        <hr>
                      {% endfor %}
                    {% else %}
                      <p>No calculations available.</p>
                    {% endif %}
                  </div>
                {% else %}
                  <div class="card">
                    <h3>Waiting for Image</h3>
                    <p class="muted">Upload an image or choose one from the dataset to see results.</p>
                  </div>
                {% endif %}
              </div>
            </div>
          </body>
        </html>
        """,
        error=error,
        result=result,
        uploaded_name=uploaded_name,
        dataset_files=dataset_files,
        output_name=Path(result["visualization_path"]).name if result else "",
    )


@app.route("/manual", methods=["GET", "POST"])
def manual_calculator():
    error = None
    calculation = None
    if request.method == "POST":
        try:
            calculation = _manual_calculation(request.form)
        except Exception as exc:
            error = str(exc)

    return render_template_string(
        """
        <!doctype html>
        <html>
          <head>
            <meta charset="utf-8">
            <title>Manual Surface Area Calculator</title>
            <style>
              :root {
                --bg: #0f172a;
                --panel: #111827;
                --card: #0b1220;
                --muted: #94a3b8;
                --accent: #38bdf8;
                --text: #e2e8f0;
              }
              body { font-family: "Segoe UI", Arial, sans-serif; margin: 0; background: var(--bg); color: var(--text); }
              .topbar { padding: 16px 24px; border-bottom: 1px solid #1f2937; display: flex; align-items: center; gap: 16px; }
              .nav a { text-decoration: none; color: var(--text); margin-right: 12px; padding: 6px 10px; border-radius: 6px; background: #1f2937; }
              .wrap { padding: 18px; max-width: 1000px; margin: 0 auto; }
              .card { background: var(--panel); border-radius: 12px; padding: 16px; border: 1px solid #1f2937; margin-bottom: 16px; }
              .row { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
              .section { margin-top: 16px; }
              .btn { background: var(--accent); color: #00202b; border: none; padding: 8px 12px; border-radius: 8px; font-weight: 600; cursor: pointer; }
              select, input { width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #1f2937; background: #0b1220; color: var(--text); }
              .error { color: #f87171; }
              .muted { color: var(--muted); font-size: 13px; }
            </style>
            <script>
              function toggleFields() {
                const shape = document.getElementById("shape").value;
                document.querySelectorAll("[data-shape]").forEach(el => {
                  el.style.display = (el.dataset.shape === shape) ? "block" : "none";
                });
              }
              window.addEventListener("DOMContentLoaded", toggleFields);
            </script>
          </head>
          <body>
            <div class="topbar">
              <div class="nav">
                <a href="{{ url_for('index') }}">OCR Studio</a>
                <a href="{{ url_for('manual_calculator') }}">Manual Calculator</a>
              </div>
            </div>
            <div class="wrap">
              <div class="card">
                <h3>Manual Surface Area Calculator</h3>
                <p class="muted">Enter exact measurements to calculate surface area without OCR.</p>
                <form method="post">
                  <div class="row">
                    <div>
                      <label>Shape</label><br>
                      <select id="shape" name="shape" onchange="toggleFields()" required>
                        <option value="cylinder">Cylinder</option>
                        <option value="rectangular">Rectangular</option>
                        <option value="frustum">Frustum</option>
                        <option value="bucket">Bucket</option>
                        <option value="scoop">Scoop</option>
                      </select>
                    </div>
                    <div>
                      <label>Unit</label><br>
                      <select name="unit">
                        <option value="mm">mm</option>
                        <option value="cm">cm</option>
                        <option value="m">m</option>
                      </select>
                    </div>
                    <div>
                      <label>
                        <input type="checkbox" name="include_top_bottom">
                        Include top/bottom
                      </label>
                    </div>
                  </div>

                  <div class="section" data-shape="cylinder">
                    <h4>Cylinder</h4>
                    <div class="row">
                      <input type="text" name="cylinder_diameter" placeholder="Diameter">
                      <input type="text" name="cylinder_height" placeholder="Height">
                    </div>
                  </div>

                  <div class="section" data-shape="rectangular">
                    <h4>Rectangular</h4>
                    <div class="row">
                      <input type="text" name="rect_length" placeholder="Length">
                      <input type="text" name="rect_width" placeholder="Width">
                      <input type="text" name="rect_height" placeholder="Height">
                    </div>
                  </div>

                  <div class="section" data-shape="frustum">
                    <h4>Frustum</h4>
                    <div class="row">
                      <input type="text" name="frustum_top_diameter" placeholder="Top diameter">
                      <input type="text" name="frustum_bottom_diameter" placeholder="Bottom diameter">
                      <input type="text" name="frustum_height" placeholder="Height">
                    </div>
                  </div>

                  <div class="section" data-shape="bucket">
                    <h4>Bucket</h4>
                    <div class="row">
                      <input type="text" name="bucket_top_diameter" placeholder="Top diameter">
                      <input type="text" name="bucket_bottom_diameter" placeholder="Bottom diameter">
                      <input type="text" name="bucket_height" placeholder="Height">
                    </div>
                  </div>

                  <div class="section" data-shape="scoop">
                    <h4>Scoop</h4>
                    <div class="row">
                      <input type="text" name="scoop_top_diameter" placeholder="Top diameter">
                      <input type="text" name="scoop_bottom_diameter" placeholder="Bottom diameter">
                      <input type="text" name="scoop_height" placeholder="Height">
                    </div>
                  </div>

                  <div class="section">
                    <button class="btn" type="submit">Calculate</button>
                  </div>
                </form>
              </div>

              {% if error %}
                <p class="error">{{ error }}</p>
              {% endif %}

              {% if calculation %}
                <div class="card">
                  <h3>Result</h3>
                  <p><strong>Shape:</strong> {{ calculation['shape'] }}</p>
                  <p><strong>Total Area:</strong> {{ "%.2f"|format(calculation['total_area_cm2']) }} cm2</p>
                  <p><strong>Total Area:</strong> {{ "%.6f"|format(calculation['total_area_m2']) }} m2</p>
                  <p><strong>Dimensions:</strong> {{ calculation['dimensions'] }}</p>
                </div>
              {% endif %}
            </div>
          </body>
        </html>
        """,
        error=error,
        calculation=calculation,
    )


@app.route("/files/<dir_key>/<path:filename>")
def files(dir_key: str, filename: str):
    if dir_key == "input":
        base = UPLOAD_DIR
    elif dir_key == "output":
        base = OUTPUT_DIR_PATH
    else:
        abort(404)
    return send_from_directory(base, filename)


def main():
    import os
    parser = argparse.ArgumentParser(description="Local OCR measurement server")
    parser.add_argument("--host", default=None, help="Host address (default: 0.0.0.0 if PORT set, else 127.0.0.1)")
    parser.add_argument("--port", type=int, default=None, help="Port number (default: PORT env or 8000)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    port = args.port if args.port is not None else int(os.environ.get("PORT", "8000"))
    host = args.host if args.host is not None else ("0.0.0.0" if os.environ.get("PORT") else "127.0.0.1")

    app.run(host=host, port=port, debug=args.debug)


if __name__ == "__main__":
    main()
