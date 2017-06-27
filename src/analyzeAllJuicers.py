import json
import numpy as np
import matplotlib.pyplot as plt

with open("../out/juicers.json", "r") as f:
    allJuicers = json.load(f)

priceListByBrand = {}
rankListByBrand = {}
juicersByAsin = {}
for cat, juicers in allJuicers.items():
    for juicer in juicers:
        asin = list(juicer.keys())[0]
        val = list(juicer.values())[0]
        val.update({"category":cat})
        if any(x in val['title'].lower() for x in ['juice','juicer']):
            juicersByAsin.update({asin: val})
        else:
            continue
        brand = val['brand']
        try:
            if brand.lower() == 'breville juicer':
                brand = 'breville'
        except:
            continue

        try:
            if brand.lower() == 'omega juicers':
                brand = 'omega'
        except:
            continue
        try:
            priceListByBrand.setdefault(brand, []).append(float(val['price'][1:]))
        except:
            pass

        try:
            if not val['sales_rank'] == 'None':
                rankListByBrand.setdefault(brand, []).append(int(val['sales_rank']))
        except:
            pass

print("total number of juicers = ", len(juicersByAsin))

juicerCountByBrand = {}
for brand, l in rankListByBrand.items():
    try:
        if brand.lower() == 'breville juicer':
            brand = 'breville'
    except:
        continue

    try:
        if brand.lower() == 'omega juicers':
            brand = 'omega'
    except:
        continue
    juicerCountByBrand.update({brand.lower():len(l)})

sortedJuicerCountByBrand = sorted(juicerCountByBrand.items(), key=lambda x:x[1], reverse=True)[:20]
fig, ax = plt.subplots()
fig.canvas.draw()
ax.bar(np.arange(len(sortedJuicerCountByBrand)), [x[1]for x in sortedJuicerCountByBrand])
ax.set_xticks(np.arange(len(sortedJuicerCountByBrand)))
ax.set_xticklabels((x[0] for x in sortedJuicerCountByBrand), rotation='vertical')
plt.xlabel('Brands')
plt.ylabel('# of juicers')
plt.title('# of juicers by Brands')
plt.show()

priceRrankList = []
priceRankListByCategory = {}
rankListByTitleByCategory = {}
rankListByTitle = []
colorList = []
juicerListByColor = {}
for asin, juicer in juicersByAsin.items():
    try:
        price = float(juicer['price'][1:])
    except:
        continue
    try:
        sales_rank = int(juicer['sales_rank'])
    except:
        continue
    title = juicer['title']
    cat = juicer['category']
    priceRrankList.append([price, sales_rank])
    rankListByTitle.append([title, sales_rank])
    priceRankListByCategory.setdefault(cat, []).append([price, sales_rank])
    rankListByTitleByCategory.setdefault(cat, []).append([title, sales_rank])
    color = juicer['color']
    try:
        if color.lower() == 'none':
            continue
    except:
        continue
    if color.lower() == 'stainless' or color.lower() == 'steel':
        color = 'Stainless Steel'
    colorList.append(color)
    juicerListByColor.setdefault(color, []).append(asin)

sortedRankListByTitle = sorted(rankListByTitle, key=lambda x:x[1])[:20]
mnrank = min([x[1] for x in sortedRankListByTitle])

fig, ax = plt.subplots()
fig.canvas.draw()
ax.bar(np.arange(len(sortedRankListByTitle)), [1 / x[1] * mnrank * 100 for x in sortedRankListByTitle])
ax.set_xticks(np.arange(len(sortedRankListByTitle)))
ax.set_xticklabels((" ".join(x[0].split(" ")[:4]) for x in sortedRankListByTitle), rotation='vertical')
plt.xlabel('Models')
plt.ylabel('rank (%)')
plt.title('Models by Sales Rank [All Categories]')
plt.show()

for cat, rlist in rankListByTitleByCategory.items():
    sortedrlist = sorted(rlist, key=lambda x:x[1])[:20]
    mnrank = min([x[1] for x in sortedrlist])

    fig, ax = plt.subplots()
    fig.canvas.draw()
    ax.bar(np.arange(len(sortedrlist)), [1 / x[1] * mnrank * 100 for x in sortedrlist])
    ax.set_xticks(np.arange(len(sortedrlist)))
    ax.set_xticklabels((" ".join(x[0].split(" ")[:4]) for x in sortedrlist), rotation='vertical')
    plt.xlabel('Models')
    plt.ylabel('rank (%)')
    plt.title('Models by Sales Rank [{0}]'.format(cat))
    plt.show()

uniqueColorList = list(set(colorList))
print("# of unique colors = ", len(uniqueColorList))
print("color list: ", uniqueColorList)

sortedJuicerListByColor = sorted(juicerListByColor.items(), key = lambda x:len(x[1]), reverse=True)

colorBinlist = []
for color, l in sortedJuicerListByColor[:20]:
    colorBinlist.append([color, len(l)])

fig, ax = plt.subplots()
fig.canvas.draw()
ax.bar(np.arange(len(colorBinlist)), [x[1] for x in colorBinlist])
#ax.xlabel('colors')
#ax.ylabel('# of juicers')
#ax.title('# of juicers by color')
ax.set_xticks(np.arange(len(colorBinlist)))
ax.set_xticklabels((x[0] for x in colorBinlist), rotation='vertical')
plt.show()

plt.scatter(np.array([x[0] for x in priceRrankList]), np.array([x[1] for x in priceRrankList]))
plt.xlabel('price($)')
plt.ylabel('sales rank')
plt.title('sales rank by price for all the juicers')
plt.show()

plt.hist([x[0] for x in priceRrankList], bins=100)
plt.xlabel('price($)')
plt.ylabel('# of juicers')
plt.title('price($) histogram for all the juicers')
plt.show()

plt.hist([x[1] for x in priceRrankList], bins=100)
plt.xlabel('sales rank')
plt.ylabel('# of juicers')
plt.title('sales rank histogram for all the juicers')
plt.show()

for cat, l in priceRankListByCategory.items():
    plt.hist([x[0] for x in l], bins=100)
    plt.xlabel('price($)')
    plt.ylabel('# of juicers')
    plt.title('price histogram for {0} juicers'.format(cat))
    plt.show()

    plt.hist([x[1] for x in l], bins=100)
    plt.xlabel('sales rank')
    plt.ylabel('# of juicers')
    plt.title('sales rank histogram for {0} juicers'.format(cat))
    plt.show()

juicersByAsinByCategory = {}
for asin, juicer in juicersByAsin.items():
    cat = juicer['category']
    juicersByAsinByCategory.setdefault(cat, {}).update({asin: juicer})

for cat, juicers in juicersByAsinByCategory.items():
    print("#juicers[{0}] = ".format(cat), len(juicers))

avgRankByCategory = {}
for cat, juicers in juicersByAsinByCategory.items():
    mn = np.mean(np.array([int(x['sales_rank']) for x in filter(lambda a: a['sales_rank'] != 'None', list(juicers.values()))]))
    print("mean_sales_rank[{0}] = ".format(cat), mn)

avgPriceByBrand = {}
for brand, l in priceListByBrand.items():
    avgPriceByBrand.update({brand:np.mean(np.array(l))})

def getSortedRankListByBrand(d):
    rankByBrand = {}
    avgByBrand = {}
    for asin, juicer in d.items():
        try:
            if not juicer['sales_rank'] == 'None':
                rankByBrand.setdefault(juicer['brand'], []).append(int(juicer['sales_rank']))
        except:
            pass

    for brand, l in rankByBrand.items():
        avg = np.mean(np.array(l))
        avgByBrand.update({brand: avg})

    sortedRankByBrand = sorted(avgByBrand.items(), key=lambda x: x[1])

    return sortedRankByBrand

sortedRankListByBrandByCategory = {}
for cat, juicers in juicersByAsinByCategory.items():
    sortedD = getSortedRankListByBrand(juicers)[:20]
    sortedRankListByBrandByCategory.update({cat: sortedD})
    mnrank = min([x[1] for x in sortedD])

    fig, ax = plt.subplots()
    fig.canvas.draw()
    ax.bar(np.arange(len(sortedD)), [1 / x[1] * mnrank * 100 for x in sortedD])
    ax.set_xticks(np.arange(len(colorBinlist)))
    ax.set_xticklabels((x[0] for x in sortedD), rotation='vertical')
    plt.xlabel('Brands')
    plt.ylabel('rank (%)')
    plt.title('Brands by Sales Rank [{0}]'.format(cat))
    plt.show()


avgRankByBrand = {}
for brand, l in rankListByBrand.items():
    avg = np.mean(np.array(l))
    avgRankByBrand.update({brand:avg})


print("number of brands = ", len(rankListByBrand))
print("brand list: ", rankListByBrand.keys())

pass
