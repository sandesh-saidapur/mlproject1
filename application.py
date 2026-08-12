from flask import Flask, request, render_template
import traceback

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():

    if request.method == 'GET':
        return render_template('home.html')

    try:

        print("=" * 80)
        print("FORM DATA")
        print(request.form)
        print(request.form.to_dict())
        print("=" * 80)

        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race_ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))
        )

        pred_df = data.get_data_as_dataframe()

        print("INPUT DATAFRAME")
        print(pred_df)

        predict_pipeline = PredictPipeline()

        print("Loading model...")

        results = predict_pipeline.predict(pred_df)

        print("Prediction:", results)

        return render_template(
            'home.html',
            results=results[0]
        )

    except Exception:

        error = traceback.format_exc()

        print("=" * 80)
        print("APPLICATION ERROR")
        print(error)
        print("=" * 80)

        return f"""
        <h1>Application Error</h1>
        <pre>{error}</pre>
        """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
