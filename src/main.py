from amazon.api import AmazonAPI

AMAZON_ACCESS_KEY = 'AKIAIM5AOOMVJVPWCCSQ'
AMAZON_SECRET_KEY = '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'
AMAZON_ASSOC_TAG = 'adthomas-20'

amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

#product = amazon.lookup(ItemId='B00EOE0WKQ')

#products = amazon.search_n(100, Keywords = 'juicer', SearchIndex='All')

#for i, product in enumerate(products):
#    print("{0}. '{1}'".format(i, product.title))

product = amazon.lookup(ItemId='B001L7OIVI')
reviews = product.reviews[1]

pass