from amazonproduct import API

api = API(locale='de')
for product in api.item_search('Books', Publisher='Galileo Press'):
    print(product)