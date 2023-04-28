from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

api_key = "acf7a99cb229a4757a40312c25af3171"

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route("/weather", methods=['GET', 'POST'])
def weather():
    if request.method == "POST":
        city = request.form["city"]

        # API endpoint url
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

        # Make API request and save response
        response = requests.get(url.format(city))

        # Parse response data
        data = response.json()

        current_weather = {
            "description": data["list"][0]["weather"][0]["description"],
            "temperature": data["list"][0]["main"]["temp"],
            "humidity": data["list"][0]["main"]["humidity"],
            "windspeed": data["list"][0]["wind"]["speed"],
            "icon": data["list"][0]["weather"][0]["icon"]
        }

        forecasts = []
        for i in range(1, len(data["list"]), 2):
            forecast = {
                "description": data["list"][i]["weather"][0]["description"],
                "date": data["list"][i]["dt_txt"],
                "temperature": data["list"][i]["main"]["temp"],
                "humidity": data["list"][i]["main"]["humidity"],
                "icon": data["list"][i]["weather"][0]["icon"]
            }
            forecasts.append(forecast)

        # Render template with data
        return render_template("weather.html",city=city.title(), current_weather=current_weather, forecasts=forecasts)

    else:
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
