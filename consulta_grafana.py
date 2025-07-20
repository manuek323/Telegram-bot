import requests
import json

# Desenvolvido por: Bee Solutions
# Autor: Fernando Almondes
# Data: 17/07/2025 14:04

from decouple import Config, RepositoryEnv

#env_path = '/opt/bee/beebot/.env'
env_path = '.env'
config = Config(RepositoryEnv(env_path))

url_grafana = config('GRAFANA_URL') # Chatid que pode requisitar no Beebot
token = config('GRAFANA_TOKEN')

def consulta_lista_dashboards():

    # Padrao de filtro para dashboards ativos com limite de ate 1000.
    url_consulta = f'{url_grafana}/api/search?limit=1000&deleted=false&type=dash-db'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    resultado = requests.get(url=url_consulta, headers=headers)

    #print(resultado.text)

    saida_json = json.loads(resultado.text)

    lista_uids = []
    lista_titles = []

    for i in saida_json:
        lista_uids.append(i['uid'])
        lista_titles.append(i['title'])

    lista_final = list(zip(lista_titles, lista_uids))

    resultado = ''

    for i in lista_final:
        uid = i[1]
        title = i[0]
        resultado += f'--> Dashboard: {title}\n'
        resultado += f'/dash {uid}\n\n'

    if resultado:
        return resultado
    else:
        return

    #print(json.dumps(saida_json, indent=4))

def gera_img(uid):

    # Padrao de resolucao FHD, Tela Cheia e escala de 50%...
    url_consulta = f'{url_grafana}/render/d/{uid}?width=1920&height=1080&scale=0.5&fullscreen&kiosk'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    resultado = requests.get(url=url_consulta, headers=headers)

    if resultado.status_code == 200:
        #with open(f'{uid}.png', 'wb') as f:
        #    f.write(resultado.content)
        return resultado.content
    else:
        print(f'--> Erro ao salvar imagem {resultado.status_code}!')
        return

#gera_img(uid='uidid')