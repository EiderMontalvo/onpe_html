from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')

def get_participacion_data(id):
    url = f'https://oaemdl.es/onpe_sweb_php/participacion/{id}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                return data
        return None
    except requests.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None

def pageNoFound(error):
    return render_template('index.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/participacion')
def participacion():
    return render_template('participacion.html')


@app.route('/participacion_total')
def ParticipacionTotal():
    IdParam = request.args.get('id')
    
    if IdParam == 'Nacional':
        Url = 'https://oaemdl.es/onpe_sweb_php/participacion/Nacional'
        Template = 'participacionN.html'
    elif IdParam == 'Extranjero':
        Url = 'https://oaemdl.es/onpe_sweb_php/participacion/Extranjero'
        Template = 'participacionE.html'
    else:
        return render_template('participacionN.html', id=IdParam, data=None)

    Response = requests.get(Url)
    DbData = Response.json()
    
    if DbData['success']:
        DataProcesada = {
            'Departamentos': [{
                'Nombre': d['DPD'],
                'TotalAsistentes': d['TV'],
                'PorcentajeAsistentes': d['PTV'].replace(' %', ''),
                'TotalAusentes': d['TA'],
                'PorcentajeAusentes': d['PTA'].replace(' %', ''),
                'ElectoresHabiles': d['EH']
            } for d in DbData['data']],
            'Totales': {}
        }
        TotalAsistentes = sum(int(d['TV'].replace(',', '')) for d in DbData['data'])
        TotalAusentes = sum(int(d['TA'].replace(',', '')) for d in DbData['data'])
        TotalHabiles = sum(int(d['EH'].replace(',', '')) for d in DbData['data'])
        PorcentajeAsistentes = (TotalAsistentes / TotalHabiles * 100) if TotalHabiles > 0 else 0
        PorcentajeAusentes = (TotalAusentes / TotalHabiles * 100) if TotalHabiles > 0 else 0
        DataProcesada['Totales'] = {
            'Asistentes': "{:,}".format(TotalAsistentes),
            'PorcentajeAsistentes': "{:.3f}".format(PorcentajeAsistentes),
            'Ausentes': "{:,}".format(TotalAusentes),
            'PorcentajeAusentes': "{:.3f}".format(PorcentajeAusentes),
            'TotalHabiles': "{:,}".format(TotalHabiles)
        }
    else:
        DataProcesada = None

    return render_template(Template, id=IdParam, data=DataProcesada)


@app.route('/actas_numero')
def actas_numero():
    return render_template('actas_numero.html', search_attempted=False)

@app.route('/actas_numero/<id>')
def actas_numero_id(id):
    try:
        response = requests.get(f'https://oaemdl.es/onpe_sweb_php/actas/numero/{id}')
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                return render_template('actas_numero.html', actas=data['data'], search_attempted=True)
        return render_template('actas_numero.html', search_attempted=True)
    except:
        return render_template('actas_numero.html', search_attempted=True)

app.register_error_handler(404, pageNoFound)

if __name__ == "__main__":
    app.run(debug=True)