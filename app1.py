from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load CSV data with error handling
def load_csv():
    df = pd.read_csv('unlinked.csv', on_bad_lines='skip')
    df.columns = df.columns.str.strip().str.lower() # Normalize column names
    return df

@app.route('/')
def index():
    return render_template('index1.html', details=None)

@app.route('/allocate_schedule', methods=['POST'])
def allocate_schedule():
    crew_id = request.form.get('crew_id')

    if not crew_id:
        return 'Crew ID is required', 400

    # Load CSV data
    df = load_csv()

    if df.empty:
        return 'Error loading CSV or no data available', 500

    # Filter the DataFrame for the crew_id
    details = df[df['crew_id'] == crew_id]
    if details.empty:
        return 'No details found for the given Crew ID', 404

    # Convert the details to a dictionary
    details = details.to_dict(orient='records')

    return render_template('index1.html', details=details)

if __name__ == '__main__':
    app.run(debug=True)
