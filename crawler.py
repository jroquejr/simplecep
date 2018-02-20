import requests
from bs4 import BeautifulSoup


CEPURL = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm?t"


ESTADOSBR = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins"
}


class NotFoundException(Exception):
    pass

def cep_retrieve(cep):
    response = requests.post(CEPURL, data = {
        "relaxation": cep,
        "Metodo": "listaLogradouro",
        "TipoConsulta": "relaxation",
        "StartRow": 1,
        "EndRow": 10,
    }, timeout=10)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as ex:
        raise ex

    return response.text


def cep_extract(html):

    soup = BeautifulSoup(html, 'html.parser')
    linhas = soup.select('.tmptabela tr')

    if len(linhas) <= 1:
        raise NotFoundException("Deu Ruim")

    linhas = linhas[1:]

    retorno = []

    for linha in linhas:

        colunas = linha.select('td')

        cidade = ""
        estado = ""

        cidade_uf = colunas[2].text
        if cidade_uf:
            cidade, estado = cidade_uf.split('/', 1)

        item = {
            'logradouro': colunas[0].text.strip(),
            'bairro': colunas[1].text.strip(),
            'cidade': cidade.strip(),
            'estado': ESTADOSBR.get(estado.strip()),
            'uf': estado.strip(),
            'cep': colunas[3].text.replace('-', '').strip()
        }

        retorno.append(item)

    return retorno

def get_this_cep(cep):
    html_doc = cep_retrieve(cep)
    return cep_extract(html_doc)

if __name__ == "__main__":

    print(get_this_cep(74093030))