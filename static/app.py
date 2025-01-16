from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np
import ast
import json
import requests


# Predefined lists of valid countries and crops
countries = ['Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 
             'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 
             'Burundi', 'Cameroon', 'Canada', 'Central African Republic', 'Chile', 'Colombia', 'Croatia', 'Denmark', 
             'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Eritrea', 'Estonia', 'Finland', 'France', 
             'Germany', 'Ghana', 'Greece', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'India', 
             'Indonesia', 'Iraq', 'Ireland', 'Italy', 'Jamaica', 'Japan', 'Kazakhstan', 'Kenya', 'Latvia', 'Lebanon', 
             'Lesotho', 'Libya', 'Lithuania', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Mauritania', 'Mauritius', 
             'Mexico', 'Montenegro', 'Morocco', 'Mozambique', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 
             'Nicaragua', 'Niger', 'Norway', 'Pakistan', 'Papua New Guinea', 'Peru', 'Poland', 'Portugal', 'Qatar', 
             'Romania', 'Rwanda', 'Saudi Arabia', 'Senegal', 'Slovenia', 'South Africa', 'Spain', 'Sri Lanka', 
             'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Tajikistan', 'Thailand', 'Tunisia', 'Turkey', 'Uganda', 
             'Ukraine', 'United Kingdom', 'Uruguay', 'Zambia', 'Zimbabwe']

crops = ['Maize', 'Potatoes', 'Rice, paddy', 'Sorghum', 'Soybeans', 'Wheat',
         'Cassava', 'Sweet potatoes', 'Plantains and others', 'Yams']

# Load model and transformer
svc = pickle.load(open('svc.pkl','rb'))
knn = pickle.load(open('knn model.pkl', 'rb'))
t1 = pickle.load(open('tranform.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/crop')
def crop():
    return render_template('crop.html')

@app.route('/predict', methods=['POST'])
def CropYeild():
    if request.method == 'POST':
        # Get form data
        Year = request.form.get('year')
        Item = request.form.get('crop_name').strip()  # Normalize input
        Area = request.form.get('country_name').strip().title()  # Normalize input
        avg_temp = request.form.get('temp')
        average_rain_fall_mm_per_year = request.form.get('rain')
        pesticides_tonnes = request.form.get('tons')

        
        if not all([Year, Item, Area, avg_temp, average_rain_fall_mm_per_year, pesticides_tonnes]):
            error = "All fields are required. Please fill in all the details."
            return render_template('crop.html', error=error)

        # Validate crop and country
        if Item not in crops:
            error = f"No crop found with the name '{Item}'. Please enter a valid crop."
            return render_template('crop.html', error=error)
        
        if Area not in countries:
            error = f"No country found with the name '{Area}'. Please enter a valid country."
            return render_template('crop.html', error=error)

        if(int(average_rain_fall_mm_per_year)<0 or int(pesticides_tonnes) < 0):
            error = f"How can these things be -ve :,). Please enter a valid Number."
            return render_template('crop.html', error=error)
            
    

        # Convert numeric fields
        try:
            Year = int(Year)
            avg_temp = float(avg_temp)
            average_rain_fall_mm_per_year = float(average_rain_fall_mm_per_year)
            pesticides_tonnes = float(pesticides_tonnes)
        except ValueError:
            error = "Please ensure that Year, Avg Temp, Rainfall, and Pesticides are numeric values."
            return render_template('crop.html', error=error)

        # Create a DataFrame for the input features
        features = pd.DataFrame([[Area, Item, Year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp]],
                                columns=['Area', 'Item', 'Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp'])

        # Transform the features using the transformer
        try:
            features_transformed = t1.transform(features)
        except Exception as e:
            error = f"Error during data transformation: {e}"
            return render_template('crop.html', error=error)

    
        try:
            pred = knn.predict(features_transformed).reshape(1, -1)
        except Exception as e:
            error = f"Error during prediction: {e}"
            return render_template('crop.html', error=error)

        # Render the template with the prediction result
        return render_template('crop.html', pred_value=pred[0])
    


#disease recomdation
dis_list = {0: '(vertigo) Paroymsal  Positional Vertigo', 1: 'AIDS', 2: 'Acne', 3: 'Alcoholic hepatitis', 4: 'Allergy', 5: 'Arthritis', 6: 'Bronchial Asthma', 7: 'Cervical spondylosis', 8: 'Chicken pox', 9: 'Chronic cholestasis',
            10: 'Common Cold', 11: 'Dengue', 12: 'Diabetes ', 13: 'Dimorphic hemmorhoids(piles)', 14: 'Drug Reaction', 15: 'Fungal infection', 16: 'GERD', 17: 'Gastroenteritis', 18: 'Heart attack',
            19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 23: 'Hypertension ', 24: 'Hyperthyroidism', 25: 'Hypoglycemia',
            26: 'Hypothyroidism', 27: 'Impetigo', 28: 'Jaundice', 29: 'Malaria', 30: 'Migraine', 31: 'Osteoarthristis', 32: 'Paralysis (brain hemorrhage)',
            33: 'Peptic ulcer diseae', 34: 'Pneumonia', 35: 'Psoriasis', 36: 'Tuberculosis', 37: 'Typhoid', 38: 'Urinary tract infection', 39: 'Varicose veins', 40: 'hepatitis A'}


sym_list = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7,
            'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15,
            'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23,
            'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30,
            'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41,
            'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49,
            'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60,
            'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68,
            'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74,
            'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85,
            'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94,
            'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103,
            'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112,
            'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120,
            'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127,
            'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}

sym_mapping = {'itching': 'itching', 'skin rash': 'skin_rash', 'nodal skin eruptions': 'nodal_skin_eruptions', 'continuous sneezing': 'continuous_sneezing', 'shivering': 'shivering', 'chills': 'chills', 'joint pain': 'joint_pain', 'stomach pain': 'stomach_pain', 'acidity': 'acidity', 'ulcers on tongue': 'ulcers_on_tongue', 'muscle wasting': 'muscle_wasting', 'vomiting': 'vomiting',
            'burning micturition': 'burning_micturition', 'spotting  urination': 'spotting_ urination', 'fatigue': 'fatigue', 'weight gain': 'weight_gain', 'anxiety': 'anxiety', 'cold hands and feets': 'cold_hands_and_feets', 'mood swings': 'mood_swings', 'weight loss': 'weight_loss','restlessness': 'restlessness', 'lethargy': 'lethargy', 'patches in throat': 'patches_in_throat', 'irregular sugar level': 'irregular_sugar_level', 'cough': 'cough', 'high fever': 'high_fever', 'sunken eyes': 'sunken_eyes', 'breathlessness': 'breathlessness',
            'sweating': 'sweating', 'dehydration': 'dehydration', 'indigestion': 'indigestion', 'headache': 'headache', 'yellowish skin': 'yellowish_skin', 'dark urine': 'dark_urine', 'nausea': 'nausea', 'loss of appetite': 'loss_of_appetite', 'pain behind the eyes': 'pain_behind_the_eyes', 'back pain': 'back_pain', 'constipation': 'constipation', 'abdominal pain': 'abdominal_pain', 'diarrhoea': 'diarrhoea', 'mild fever': 'mild_fever', 'yellow urine': 'yellow_urine', 'yellowing of eyes': 'yellowing_of_eyes', 'acute liver failure': 'acute_liver_failure',
            'fluid overload': 'fluid_overload', 'swelling of stomach': 'swelling_of_stomach', 'swelled lymph nodes': 'swelled_lymph_nodes', 'malaise': 'malaise', 'blurred and distorted vision': 'blurred_and_distorted_vision', 'phlegm': 'phlegm', 'throat irritation': 'throat_irritation', 'redness of eyes': 'redness_of_eyes', 'sinus pressure': 'sinus_pressure', 'runny nose': 'runny_nose', 'congestion': 'congestion', 'chest pain': 'chest_pain', 'weakness in limbs': 'weakness_in_limbs', 'fast heart rate': 'fast_heart_rate', 'pain during bowel movements': 'pain_during_bowel_movements',
            'pain in anal region': 'pain_in_anal_region', 'bloody stool': 'bloody_stool', 'irritation in anus': 'irritation_in_anus', 'neck pain': 'neck_pain', 'dizziness': 'dizziness', 'cramps': 'cramps', 'bruising': 'bruising', 'obesity': 'obesity', 'swollen legs': 'swollen_legs',
            'swollen blood vessels': 'swollen_blood_vessels', 'puffy face and eyes': 'puffy_face_and_eyes', 'enlarged thyroid': 'enlarged_thyroid', 'brittle nails': 'brittle_nails', 'swollen extremeties': 'swollen_extremeties', 'excessive hunger': 'excessive_hunger', 'extra marital contacts': 'extra_marital_contacts', 'drying and tingling lips': 'drying_and_tingling_lips', 'slurred speech': 'slurred_speech', 'knee pain': 'knee_pain', 'hip joint pain': 'hip_joint_pain', 'muscle weakness': 'muscle_weakness',
            'stiff neck': 'stiff_neck', 'swelling joints': 'swelling_joints', 'movement stiffness': 'movement_stiffness', 'spinning movements': 'spinning_movements', 'loss of balance': 'loss_of_balance', 'unsteadiness': 'unsteadiness', 'weakness of one body side': 'weakness_of_one_body_side', 'loss of smell': 'loss_of_smell', 'bladder discomfort': 'bladder_discomfort', 'foul smell of urine': 'foul_smell_of urine', 'continuous feel of urine': 'continuous_feel_of_urine', 'passage of gases': 'passage_of_gases', 'internal itching': 'internal_itching', 'toxic look (typhos)': 'toxic_look_(typhos)', 'depression': 'depression', 'irritability': 'irritability', 'muscle pain': 'muscle_pain', 'altered sensorium': 'altered_sensorium', 'red spots over body': 'red_spots_over_body', 'belly pain': 'belly_pain', 'abnormal menstruation': 'abnormal_menstruation', 'dischromic  patches': 'dischromic _patches', 'watering from eyes': 'watering_from_eyes', 'increased appetite': 'increased_appetite',
            'polyuria': 'polyuria', 'family history': 'family_history', 'mucoid sputum': 'mucoid_sputum', 'rusty sputum': 'rusty_sputum', 'lack of concentration': 'lack_of_concentration', 'visual disturbances': 'visual_disturbances', 'receiving blood transfusion': 'receiving_blood_transfusion', 'receiving unsterile injections': 'receiving_unsterile_injections', 'coma': 'coma', 'stomach bleeding': 'stomach_bleeding', 'distention of abdomen': 'distention_of_abdomen', 'history of alcohol consumption': 'history_of_alcohol_consumption', 'fluid overload.1': 'fluid_overload.1', 'blood in sputum': 'blood_in_sputum', 'prominent veins on calf': 'prominent_veins_on_calf', 'palpitations': 'palpitations', 'painful walking': 'painful_walking', 'pus filled pimples': 'pus_filled_pimples', 'blackheads': 'blackheads',
            'scurring': 'scurring', 'skin peeling': 'skin_peeling', 'silver like dusting': 'silver_like_dusting', 'small dents in nails': 'small_dents_in_nails', 'inflammatory nails': 'inflammatory_nails', 'blister': 'blister', 'red sore around nose': 'red_sore_around_nose', 'yellow crust ooze': 'yellow_crust_ooze'}

#==============LOADING MODEL=================================
precaution = pd.read_csv("dataset/precautions_df.csv")
workout = pd.read_csv("dataset/workout_df.csv")
medication = pd.read_csv("dataset/medications.csv")
desc = pd.read_csv("dataset/description.csv")

#===============================defining function================================
def get_dis(symptoms):
    unlisted_sym = [i for i in symptoms if i not in sym_list]
    valid = [i for i in symptoms if i in sym_list]
    if unlisted_sym:
        print(f"These symptoms are not listed: {', '.join(unlisted_sym)}")
    
    if not valid:
        print("No valid symptoms provided.")
        return None
    
    input_ = np.zeros(len(sym_list))

    for i in valid:
        input_[sym_list[i]] = 1
    disease = dis_list[svc.predict([input_])[0]]
    return disease


def get_info(disease_name):
    # Get disease description
    disease_desc = desc.loc[desc['Disease'] == disease_name, 'Description'].values[0]
    
    # Get precautions for the disease
    precautions = precaution.loc[precaution['Disease'] == disease_name, 
                                 ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].values[0]
    
    # Get the workout details for the disease
    disease_workout = workout.loc[workout['disease'] == disease_name, 'workout'].values
    
    # Get the medication details as a string
    disease_medication = medication.loc[medication['Disease'] == disease_name, 'Medication'].values[0]
    
    # Convert the medication string to a list
    med = ast.literal_eval(disease_medication)
    
    # If the medication is a list, directly append to med_list
    med_list = []
    if isinstance(med, list):
        med_list.extend(med)
    
    return disease_desc, precautions, disease_workout, med_list



def normal_sym(user_sym , sym_mapping):
    
    normal_sym = sym_mapping.get(user_sym.lower())
    if not normal_sym:
        print(f"Warning: '{user_sym}' is not a recognized symptom.")
    return normal_sym

#===========================main fn-==========================================

@app.route('/disease', methods=['POST', 'GET'])
def disease():
    pred_disease = None  
    desc, precaution, workout, med = None, None, None, None  
    
    if request.method == 'POST':
        prob1 = request.form.get("symp1")
        prob2 = request.form.get("symp2")
        prob3 = request.form.get("symp3")
        prob = []
        if prob1:
            prob.append(prob1)
        if prob2:
            prob.append(prob2) 
        if prob3:
            prob.append(prob3)


        norm_list = []
        
        # Split the input by ',' and preserve multi-word symptoms
          # Split and strip whitespace

        # Map each symptom to normalized form
        for symptom in prob:
            normalized = normal_sym(symptom, sym_mapping)  # Normalize symptom
            if normalized:
                norm_list.append(normalized)
            else:
                print(f"Warning: '{symptom}' is not a recognized symptom.")
        
        print(4, norm_list)  # Debugging: Check normalized symptoms

        pred_disease = get_dis(norm_list)  # Predict the disease
        
        if pred_disease:  
            desc, precaution, workout, med = get_info(pred_disease)  # Fetch disease details
#==============================================================MOVIE RECOMENDATION==========================================================
    return render_template(
        'disease2.html', 
        pred_disease=pred_disease, 
        desc=desc, 
        precaution=precaution, 
        workout=workout, 
        med=med
    )

#==============================================================MOVIE RECOMENDATION==========================================================
df= pd.read_csv("dataset/movie_list.csv")
movies = []
for i in df['Movie_name']:
    movies.append(i)


def recommendation(movie):
    if movie not in df['Movie_name'].values:
        print("No such movie")
        return

    # Proceed if the movie exists
    index = df[df['Movie_name'] == movie].index[0]
    dis = similarity[index]
    mvlist = sorted(list(enumerate(dis)), reverse=True, key=lambda x: x[1])[1:6]
    return mvlist



def get_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8e2c59ef4b94591abf197826048ff517&language=en-US"
        response = requests.get(url)
        print(5,url)
        
        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            # Check if poster_path exists in the response
            if "poster_path" in data:
                return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
            else:
                return "No poster available."
        else:
            return f"Error: Unable to fetch data (Status Code: {response.status_code})"
    
    except Exception as e:
        return f"Error: {e}"



    


@app.route('/movie2', methods=['POST', 'GET'])
def movie():
    if request.method == 'POST':
        # Get the selected movie name from the form
        name = request.form.get('movie_name_input')
        if not name:
            return render_template('movie.html', error="Please select a movie.", movies=movies)

        # Call recommendation logic
        movie_list = recommendation(name)
        if not movie_list:
            return render_template('movie.html', error="No recommendations found.", movies=movies)
        
        movie_name = []
        images = []


       
        # Extract recommended movie names
        for i in movie_list:
            movie_id = df.iloc[i[0]]["movie_id"]
            movie_name.append(df.iloc[i[0]]['Movie_name'])
            img_url = get_poster(movie_id)
            images.append(img_url)


        return render_template('movie2.html', res=movie_name, movies=movies , images= images)

    # Default GET request
    return render_template('movie2.html', movies=movies)



if __name__ == "__main__":
    app.run(debug=True)


