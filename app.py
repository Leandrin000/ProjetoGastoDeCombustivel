from flask import Flask, render_template, request
import openrouteservice

app = Flask(__name__)

client = openrouteservice.Client(key='5b3ce3597851110001cf624858207eb146a14d7e90de54edf816799c')

@app.route('/')
def home():
    return render_template('index.html')


def inverter_coords(texto):
    lat, lon = map(float, texto.split(','))
    return (lon, lat)

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        # Pegando dados do index
        origem = request.form['origem']
        destino = request.form['destino']
        consumo = float(request.form['consumo'])
        preco = float(request.form['preco'])

        # Convertendo strings em tuplas de floats (latitude, longitude)
        origem_coords = inverter_coords(request.form['origem'])
        destino_coords = inverter_coords(request.form['destino'])


        # Calculando a rota
        rota = client.directions((origem_coords, destino_coords))

        # Pegando distância em metros e convertendo para km
        distancia_metros = rota['routes'][0]['summary']['distance']
        distancia_km = distancia_metros / 1000

        # Cálculo de combustível
        litros = distancia_km / consumo
        custo = litros * preco

        return render_template('resultado.html', custo=custo, distancia=distancia_km)

    except Exception as e:
        return f"Ocorreu um erro: {e}"

if __name__ == '__main__':
    app.run(debug=True)
