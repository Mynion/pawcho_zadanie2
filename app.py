from flask import Flask, request, render_template_string
import requests
import datetime
import os

app = Flask(__name__)

AUTHOR = "Nikodem Kamiński"
PORT = int(os.environ.get("PORT", 8080))

# Informacje zapisywane do logów
print(f"Data uruchomienia: {datetime.datetime.now()}")
print(f"Autor aplikacji: {AUTHOR}")
print(f"Port TCP: {PORT}")

# Predefiniowane miasta i współrzędne
CITIES = {
    "Warsaw": {"country": "Poland", "lat": 52.23, "lon": 21.01},
    "Berlin": {"country": "Germany", "lat": 52.52, "lon": 13.41},
    "Paris": {"country": "France", "lat": 48.85, "lon": 2.35},
    "Tokyo": {"country": "Japan", "lat": 35.68, "lon": 139.69},
    "New York": {"country": "USA", "lat": 40.71, "lon": -74.00}
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Aplikacja pogodowa</title>
</head>
<body>

    <h2>Sprawdź aktualną pogodę</h2>

    <form method="post">

        <label>Wybierz miasto:</label><br><br>

        <select name="city">
            {% for city in cities %}
                <option value="{{ city }}">{{ city }}</option>
            {% endfor %}
        </select>

        <br><br>

        <input type="submit" value="Sprawdź pogodę">

    </form>

    {% if weather %}
        <h3>Wynik:</h3>

        <p>Miasto: {{ weather.city }}</p>
        <p>Kraj: {{ weather.country }}</p>
        <p>Temperatura: {{ weather.temperature }} °C</p>
        <p>Prędkość wiatru: {{ weather.wind }} km/h</p>

    {% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    weather = None

    if request.method == "POST":

        city = request.form["city"]

        city_data = CITIES[city]

        lat = city_data["lat"]
        lon = city_data["lon"]

        # Pobieranie danych pogodowych z Open-Meteo
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true"
        )

        try:
            response = requests.get(url)
            data = response.json()

            current = data["current_weather"]

            weather = {
                "city": city,
                "country": city_data["country"],
                "temperature": current["temperature"],
                "wind": current["windspeed"]
            }

        except Exception as e:
            weather = {
                "city": city,
                "country": city_data["country"],
                "temperature": "Błąd",
                "wind": str(e)
            }

    return render_template_string(
        HTML,
        weather=weather,
        cities=CITIES.keys()
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)