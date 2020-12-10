import requests
from Pokemon import *

def getAllPokemon():
    # requête qui permet de recuperer une liste de pokemon comprise entre 0 et 151
    r_liste_pokemon = requests.get('https://pokeapi.co/api/v2/pokemon?limit=151&offset=0')
    # verification que la requête est bien effectuée
    if r_liste_pokemon.status_code == 200:
        # on integre le resultat de la requête dans une variable
        result_rlp = r_liste_pokemon.json()
        # Boucle qui permet d'afficher le nom des pokemons de notre liste   
        for result in result_rlp["results"]:
            print(result['name'])
        return result_rlp

def getPokemon(url):
    r_pokemon = requests.get(url)
    if r_pokemon.status_code == 200:
        result_r_pokemon = r_pokemon.json()
        name = result_r_pokemon["name"]
        height = result_r_pokemon["height"]
        weight = result_r_pokemon["weight"]
        backImg = result_r_pokemon["sprites"]["back_default"]
        frontImg = result_r_pokemon["sprites"]["front_default"]
        pokemon = Pokemon(name, height, weight, frontImg, backImg)
        return pokemon