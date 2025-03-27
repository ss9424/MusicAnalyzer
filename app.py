from flask import Flask, request, jsonify, render_template
from google import genai
from MusicAnalyzer import MusicPiece, MusicTheoryAnalyzer, AiAnalyzer
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    return jsonify({"file_path": file_path})

@app.route("/analyze/<analysis_type>", methods=["POST"])
def analyze(analysis_type):
    file_path = request.form.get("file_path")
    if not file_path:
        return jsonify({"error": "No file path provided"}), 400

    music = MusicPiece(file_path)
    analyzer = MusicTheoryAnalyzer(music)
    ai_analyzer = AiAnalyzer(music)

    results = {
        "key": analyzer.detect_key(),
        "chords": analyzer.detect_chords(),
        "scales": analyzer.detect_scales(),
        "cadences": analyzer.detect_cadences(),
        "metadata": music.get_metadata(),
        "summary": ai_analyzer.summery(),
        "genre": ai_analyzer.genere(),
        "suggestions": ai_analyzer.give_suggestions()
    }

    return jsonify({analysis_type: results.get(analysis_type, "Invalid analysis type")})

if __name__ == "__main__":
    app.run(host="0.0.0.0" , port=5000)
