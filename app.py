from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "change_this_secret_key"

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URL)
db = client['IBM']
collection = db['demo_data']

@app.route("/")
def index():
    return redirect(url_for('review_case', case_id=str(0)))

@app.route("/search", methods=['POST'])
def search_case():
    case_id = request.form.get('search_id')
    if case_id:
        return redirect(url_for('review_case', case_id=case_id))
    return redirect(url_for('index'))

@app.route("/review/<int:case_id>", methods=['GET', 'POST'])
def review_case(case_id):
    
    # 1. Calc Nav IDs (Always available)
    prev_id = case_id - 1 if case_id > 0 else None
    next_id = case_id + 1

    # 2. Handle Save
    if request.method == 'POST':
        # Only process if data actually exists to update (safety check)
        if collection.count_documents({"case_id": str(case_id)}) > 0:
            diagnostic_steps = request.form.getlist('diagnostic_steps')
            observations = request.form.getlist('observations')
            rectification = request.form.getlist('rectification')
            
            is_repeat = True if request.form.get('repeat_failure') == 'yes' else False

            update_data = {
                "motor_id": request.form.get('motor_id'),
                "area": request.form.get('area'),
                "line": request.form.get('line'),
                "rating_kw": request.form.get('rating_kw'),
                "log_book_entry_date": request.form.get('log_book_entry_date'),
                "failure_type": request.form.get('failure_type'),
                "symptom_text": request.form.get('symptom_text'),
                "root_cause": request.form.get('root_cause'),
                "verification": request.form.get('verification'),
                "reasoning": request.form.get('reasoning'),
                "failure_bucket": request.form.get('failure_bucket'),
                "severity": request.form.get('severity'),
                "repeat_failure": is_repeat, 
                "diagnostic_steps": [x for x in diagnostic_steps if x.strip()],
                "observations": [x for x in observations if x.strip()],
                "rectification": [x for x in rectification if x.strip()],
            }

            collection.update_one({"case_id": str(case_id)}, {"$set": update_data})
            flash(f"✅ Case {case_id} Saved Successfully", "success")
        else:
            flash(f"Cannot save. Case {case_id} does not exist.", "danger")
        
        return redirect(url_for('review_case', case_id=case_id))

    # 3. Fetch Data
    data = collection.find_one({"case_id": str(case_id)})

    return render_template("review.html", data=data, case_id=case_id, next_id=next_id, prev_id=prev_id)

if __name__ == "__main__":
    app.run(debug=True)