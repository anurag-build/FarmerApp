from flask import Flask, render_template, request
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import random

app = Flask(__name__)

# ------------------------------------
# 20 Crops (Auto Generated 30 Days Data)
# ------------------------------------
crops_list = [
    "Wheat","Rice","Onion","Tomato","Maize","Barley","Soybean",
    "Potato","Cotton","Sugarcane","Chili","Mustard","Groundnut",
    "Bajra","Jowar","Moong","Urad","Tur","Gram","Cabbage"
]

price_data = {}

for crop in crops_list:
    base = random.randint(800, 3000)
    trend = random.randint(5, 25)
    prices = [base + i*trend + random.randint(-50,50) for i in range(30)]
    price_data[crop] = prices


# ------------------------------------
# All Major States + Famous Cities
# ------------------------------------
state_city = {
    "Andhra Pradesh":"Visakhapatnam",
    "Arunachal Pradesh":"Itanagar",
    "Assam":"Guwahati",
    "Bihar":"Patna",
    "Chhattisgarh":"Raipur",
    "Goa":"Panaji",
    "Gujarat":"Ahmedabad",
    "Haryana":"Karnal",
    "Himachal Pradesh":"Shimla",
    "Jharkhand":"Ranchi",
    "Karnataka":"Bengaluru",
    "Kerala":"Kochi",
    "Madhya Pradesh":"Indore",
    "Maharashtra":"Mumbai",
    "Manipur":"Imphal",
    "Meghalaya":"Shillong",
    "Mizoram":"Aizawl",
    "Nagaland":"Kohima",
    "Odisha":"Bhubaneswar",
    "Punjab":"Ludhiana",
    "Rajasthan":"Jaipur",
    "Sikkim":"Gangtok",
    "Tamil Nadu":"Chennai",
    "Telangana":"Hyderabad",
    "Tripura":"Agartala",
    "Uttar Pradesh":"Lucknow",
    "Uttarakhand":"Dehradun",
    "West Bengal":"Kolkata"
}

# ------------------------------------
# ML Prediction
# ------------------------------------
def predict_next_price(prices):
    X = np.array(range(len(prices))).reshape(-1, 1)
    y = np.array(prices)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X, y)

    next_day = np.array([[len(prices)]])
    prediction = model.predict(next_day)

    return round(prediction[0], 2)


@app.route("/", methods=["GET","POST"])
def home():

    prices=[]
    predicted_price=None
    recommendation=""
    nearby_mandis=[]
    highest_mandi=None

    if request.method=="POST":

        selected_crop=request.form["crop"]
        selected_state=request.form["state"]
        quantity=float(request.form["quantity"])

        prices=price_data[selected_crop]
        predicted_price=predict_next_price(prices)

        current_price=prices[-1]

        if predicted_price>current_price:
            recommendation="📈 Prices expected to rise. Consider waiting."
        else:
            recommendation="📉 Prices may fall. Consider selling soon."

        # Generate mandi for selected state
        city=state_city[selected_state]
        distance=random.randint(5,30)

        mandi_price=predicted_price+random.randint(-100,200)
        transport=distance*10
        net=(mandi_price*quantity)-transport

        mandi_entry={
            "name": city+" Mandi",
            "state":selected_state,
            "distance":distance,
            "price":mandi_price,
            "transport":transport,
            "net":round(net,2),
            "maps_query":city+" Mandi "+selected_state
        }

        nearby_mandis.append(mandi_entry)
        highest_mandi=mandi_entry

    return render_template("index.html",
                           crops=crops_list,
                           states=state_city.keys(),
                           prices=prices,
                           predicted_price=predicted_price,
                           recommendation=recommendation,
                           nearby_mandis=nearby_mandis,
                           highest_mandi=highest_mandi)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)