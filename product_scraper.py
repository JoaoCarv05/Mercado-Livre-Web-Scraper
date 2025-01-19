import requests
from bs4 import BeautifulSoup
from utils import get_text_or_default

def fetch_page(product, page_offset):
    """
    Busca o conteúdo HTML de uma página de listagem de produtos do Mercado Livre.

    Args:
        product (str): O nome dos produtos a ser pesquisado.
        page_offset (int): O deslocamento para paginação (em qual página os produtos serão buscados).

    Returns:
        str: O conteúdo HTML da página buscada.
    """
    url = f'https://lista.mercadolivre.com.br/{product}_Desde_{page_offset}_NoIndex_True'
    response = requests.get(url)
    return response.text

def extract_product_details(html):
    """
    Extrai detalhes dos produtos do conteúdo HTML de uma página de listagem de produtos do Mercado Livre.

    Args:
        html (str): O conteúdo HTML da página de listagem de produtos na qual será extraido as informações do produto.

    Returns:
        list: Uma lista de dicionários, cada um contendo detalhes de um produto.
    """
    products = []
    soup = BeautifulSoup(html, 'html.parser')

    product_names = soup.find_all('a', class_='poly-component__title')
    product_prices = soup.find_all('span', class_='andes-money-amount__fraction')
    product_links = soup.find_all('a', class_='poly-component__title')
    product_sellers = soup.find_all('span', class_='poly-component__seller')
    product_reviews = soup.find_all('span', class_='poly-reviews__total')
    product_ratings = soup.find_all('span', class_='poly-reviews__rating')

    for i in range(len(product_names)):
        product_details = {
            'nome do produto': get_text_or_default(product_names, i),
            'preço': get_text_or_default(product_prices, i),
            'link': get_text_or_default(product_links, i, attribute='href'),
            'vendedor': get_text_or_default(product_sellers, i).strip('Por '),
            'avaliações': get_text_or_default(product_reviews, i).strip('()'),
            'classificação': get_text_or_default(product_ratings, i)
        }
        products.append(product_details)
    return products