# from fastapi import FastAPI, Query, Request, HTTPException
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# import joblib 

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")

# # Load the pickled XGBoost model
# xgb_model = joblib.load("xgb_model.joblib")

# @app.get("/display")
# def display_params(
#     request: Request,
#     prg: float = Query(..., description="Plasma glucose"),
#     pl: float = Query(..., description="Blood Work Result-1 (mu U/ml)"),
#     pr: float = Query(..., description="Blood Pressure (mm Hg)"),
#     sk: float = Query(..., description="Blood Work Result-2 (mm)"),
#     ts: float = Query(..., description="Blood Work Result-3 (mu U/ml)"),
#     m11: float = Query(..., description="Body mass index (weight in kg/(height in m)^2"),
#     bd2: float = Query(..., description="Blood Work Result-4 (mu U/ml)"),
#     age: int = Query(..., description="Patient's age (years)")
# ):
#     try:
#         # Prepare input features for prediction
#         input_features = [prg, pl, pr, sk, ts, m11, bd2, age]

#         # Make predictions using the loaded model
#         prediction = xgb_model.predict_proba([input_features])[0]

#         # Create a JSON response 
#         response = {
#             "request": {
#                 "prg": prg,
#                 "pl": pl,
#                 "pr": pr,
#                 "sk": sk,
#                 "ts": ts,
#                 "m11": m11,
#                 "bd2": bd2,
#                 "age": age
#             },
#             "prediction": {
#                 "class_0_probability": prediction[0],
#                 "class_1_probability": prediction[1]               
#             }
#         }

#         return templates.TemplateResponse(
#             "display_params.html",
#             {
#                 "request": request,
#                 "prg": prg,
#                 "pl": pl,
#                 "pr": pr,
#                 "sk": sk,
#                 "ts": ts,
#                 "m11": m11,
#                 "bd2": bd2,
#                 "age": age,
#                 "prediction": response["prediction"]
#             }
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="An error occurred while processing the request.")




# from fastapi import FastAPI, Query, Request, HTTPException
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# import joblib
# from sklearn.preprocessing import StandardScaler  # Import a standard scaler for data preprocessing

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")

# # Load the pickled XGBoost model
# xgb_model = joblib.load("xgb_model.joblib")

# # @app.get("/app")
# # async def read_root():
# #     return {"message": "Welcome to the XGBoost Diabetes Prediction API"}

# @app.get("/predict/")
# async def predict_diabetes(
#     request: Request,
#     prg: float = Query(..., description="Plasma glucose"),
#     pl: float = Query(..., description="Blood Work Result-1 (mu U/ml)"),
#     pr: float = Query(..., description="Blood Pressure (mm Hg)"),
#     sk: float = Query(..., description="Blood Work Result-2 (mm)"),
#     ts: float = Query(..., description="Blood Work Result-3 (mu U/ml)"),
#     m11: float = Query(..., description="Body mass index (weight in kg/(height in m)^2"),
#     bd2: float = Query(..., description="Blood Work Result-4 (mu U/ml)"),
#     age: int = Query(..., description="Patient's age (years)")
# ):
#     try:
#         # Prepare input features for prediction
#         input_features = [prg, pl, pr, sk, ts, m11, bd2, age]

#         # Make predictions using the loaded model
#         prediction = xgb_model.predict_proba([input_features])[0]

#         # Create a JSON response
#         response = {
#             "request": {
#                 "prg": prg,
#                 "pl": pl,
#                 "pr": pr,
#                 "sk": sk,
#                 "ts": ts,
#                 "m11": m11,
#                 "bd2": bd2,
#                 "age": age
#             },
#             "prediction": {
#                 "class_0_probability": prediction[0],
#                 "class_1_probability": prediction[1]
#             }
#         }

#         return templates.TemplateResponse(
#             "display_params.html",
#             {
#                 "request": request,
#                 "input_features": response["request"],
#                 "prediction": response["prediction"]
#             }
#         )
#     except Exception as e:
#        raise HTTPException(status_code=500, detail=(e))



# main.py
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler  # Import a standard scaler for data preprocessing

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load the pickled machine learning model
model = joblib.load("xgb_model.joblib")

# Load the scaler
scaler = joblib.load("scaler.joblib")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Machine Learning Prediction API"}

@app.get("/form/")
async def show_form():
    return templates.TemplateResponse("input_form.html", {"request": None})

@app.post("/predict/")
async def predict_ml(
    request: Request,
    prg: float = Query(..., description="Plasma glucose"),
    # ... (other input parameters)
):
    try:
        # Prepare input features for prediction as a DataFrame
        input_data = pd.DataFrame({
            "prg": [prg],
            "pl": [pl],
            "pr": [pr],
            "sk": [sk],
            "ts": [ts],
            "m11": [m11],
            "bd2": [bd2],
            "age": [age]
        })

        # Scale the input data using the loaded scaler
        scaled_input = scaler.transform(input_data)

        # Make predictions using the loaded machine learning model
        prediction = model.predict_proba(scaled_input)

        # Create a JSON response
        response = {
            "request": {
                "prg": prg,                
                "pl": pl,
                "pr": pr,
                "sk": sk,                 
                "ts": ts,
                "m11": m11,
                "bd2": bd2,
                "age": age
            },
            "prediction": {
                "class_0_probability": prediction[0][0],
                "class_1_probability": prediction[0][1]
            }
        }

        return templates.TemplateResponse(
            "display_params.html",
            {
                "request": request,
                "input_features": response["request"],
                "prediction": response["prediction"]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


