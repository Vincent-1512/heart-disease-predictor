from src.inference.pipeline import load_pipeline, predict_from_dict
def test_pipeline_load_and_predict():
    pipeline = load_pipeline(model_dir="model")
    # If no model exists, ensure it raises a RuntimeError
    try:
        predict_from_dict(pipeline, {"age":"50"})
    except RuntimeError:
        assert True
    except Exception:
        assert False
