from flask import Flask, render_template, request, redirect, url_for
from src.inference.pipeline import load_pipeline, predict_from_dict

app = Flask(__name__)
pipeline = load_pipeline(model_dir="model")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.form.to_dict()
    try:
        result = predict_from_dict(pipeline, data)
    except Exception as e:
        return render_template("result.html", error=str(e))
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
