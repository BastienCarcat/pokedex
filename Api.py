import requests

# requête qui permet de recuperer une liste de pokemon comprise entre 0 et 151
r_liste_pokemon = requests.get(
    'https://pokeapi.co/api/v2/pokemon?limit=151&offset=0')
# verification que la requête est bien effectuée
if r_liste_pokemon.status_code == 200:
    #  on integre le resultat de la requête dans une variable
    result_rlp = r_liste_pokemon.json()
    i = 0
# Boucle qui permet d'afficher le nom des pokemons de notre liste
    while i < 151:
        print(result_rlp['results'][i]['name'])
        i += 1
