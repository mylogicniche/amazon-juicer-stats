from amazon.api import AmazonAPI
import json

asinList = {
    "centrifugal": ['B01CQ4GJ5M', 'centrifugal juicer'],
    "masticating": ['B01M9GDTPJ', 'masticating juicer'],
    "citrus": ['B008BBCZ3K', 'citrus juicer']
}

amazon = AmazonAPI('AKIAIM5AOOMVJVPWCCSQ', "kupGH8IrcXAjb6NQF3Ns+MZAHT0yrMnnvApNd2ru", "adthomas-20")

total_device = 0
juicerDict = {}

for type, l in asinList.items():
    product = amazon.lookup(ItemId=l[0])
    id = product.browse_nodes[0].id

    juicerList = []
    for price in range(1000,300000,1000):
        products = amazon.search(Keywords=l[1], BrowseNode=str(id), SearchIndex='HomeGarden',
                                 MinimumPrice=price, MaximumPrice=price+1000)
        try:
            for i, product in enumerate(products):
                print("{0}. '{1}'".format(i, product.title))
                d = {
                    product.asin:
                    {
                        "brand": product.brand,
                        "color": product.color,
                        "features": product.features,
                        "price": product.formatted_price,
                        "sales_rank": str(product.sales_rank),
                        "title": product.title
                    }
                }
                juicerList.append(d)
                print(product.formatted_price)
                total_device += 1
        except:
            pass

    juicerDict.update({type: juicerList})

with open("../out/juicers.jason", "w") as f:
    json.dump(juicerDict, f, indent=4)

print("total device: ", total_device)
