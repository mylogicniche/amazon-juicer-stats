import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

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

totalJuicers = len(juicersByAsin)

print("total number of juicers = ", totalJuicers)

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
fig.subplots_adjust(bottom=0.35)
#plt.show()
plt.savefig("../out/number-juicers-by-brand-name.png", dpi=300)

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
    if color.lower() == 'stainless' or color.lower() == 'steel' or color.lower() == 'brushed stainless steel':
        color = 'Stainless Steel'
    colorList.append(color)
    juicerListByColor.setdefault(color, []).append(asin)

colorByAvgPrice = {}
for color, asinlist in juicerListByColor.items():
    pricelist = []
    for asin in asinlist:
        try:
            pricelist.append(float(juicersByAsin[asin]['price'][1:]))
        except:
            continue

    avgprice = np.mean(np.array(pricelist))
    colorByAvgPrice.update({color: avgprice})


sortedRankListByTitle = sorted(rankListByTitle, key=lambda x:x[1])[:20]
mnrank = min([x[1] for x in sortedRankListByTitle])

fig, ax = plt.subplots()
fig.canvas.draw()
ax.bar(np.arange(len(sortedRankListByTitle)), [1 / x[1] * mnrank * 100 for x in sortedRankListByTitle])
ax.set_xticks(np.arange(len(sortedRankListByTitle)))
ax.set_xticklabels((" ".join(x[0].split(" ")[:2]) for x in sortedRankListByTitle), rotation='vertical')
plt.xlabel('Models')
plt.ylabel('rank (%)')
plt.title('Models by Sales Rank [All Categories]')
fig.subplots_adjust(bottom=0.45)
plt.savefig("../out/models-by-sales-rank-all-cats.png", dpi=300)

for cat, rlist in rankListByTitleByCategory.items():
    sortedrlist = sorted(rlist, key=lambda x:x[1])[:20]
    mnrank = min([x[1] for x in sortedrlist])

    fig, ax = plt.subplots()
    fig.canvas.draw()
    ax.bar(np.arange(len(sortedrlist)), [1 / x[1] * mnrank * 100 for x in sortedrlist])
    ax.set_xticks(np.arange(len(sortedrlist)))
    ax.set_xticklabels((" ".join(x[0].split(" ")[:2]) for x in sortedrlist), rotation='vertical')
    plt.xlabel('Models')
    plt.ylabel('rank (%)')
    plt.title('Models by Sales Rank [{0}]'.format(cat))
    fig.subplots_adjust(bottom=0.45)
    plt.savefig("../out/models-by-sales-rank-{0}.png".format(cat), dpi=300)

uniqueColorList = list(set(colorList))
print("# of unique colors = ", len(uniqueColorList))
print("color list: ", uniqueColorList)

totalJuicerWithColor = 0
for color, l in juicerListByColor.items():
    totalJuicerWithColor += len(l)

print("total juicers with color defined: ", totalJuicerWithColor)

sortedJuicerListByColor = sorted(juicerListByColor.items(), key = lambda x:len(x[1]), reverse=True)
percentJuicerByColor = [[x[0], int(len(x[1])/totalJuicerWithColor*100)] for x in sortedJuicerListByColor]
totalPer = 0
percentJuicerByColor = percentJuicerByColor[:8]
for color, per in percentJuicerByColor:
    print("{0}: {1} %".format(color, per))
    totalPer += per

otherColor = 100 - totalPer

print("other color: ", otherColor)

percentJuicerByColor.append(["other", otherColor])

sizes = [x[1] for x in percentJuicerByColor]
labels = [x[0] for x in percentJuicerByColor]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title('Juicer Colors Percentage')

plt.savefig("../out/color-percent.png", dpi=300)

favColorbyAvgPrice = []
for color, p in percentJuicerByColor:
    try:
        favColorbyAvgPrice.append([color, colorByAvgPrice[color]])
    except:
        pass

fig, ax = plt.subplots()
fig.canvas.draw()
ax.bar(np.arange(len(favColorbyAvgPrice)), [x[1] for x in favColorbyAvgPrice])d
ax.set_xticks(np.arange(len(favColorbyAvgPrice)))
ax.set_xticklabels((x[0] for x in favColorbyAvgPrice), rotation='vertical')
plt.xlabel('Colors')
plt.ylabel('Price ($)')
plt.title('Color vs. Price')
fig.subplots_adjust(bottom=0.35)
plt.savefig("../out/color-vs-price.png", dpi=300)

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
plt.xlabel('Colors')
plt.ylabel('# of the Juicers')
plt.title('Juicers by Color')
fig.subplots_adjust(bottom=0.35)
plt.savefig("../out/number-juicers-by-color.png", dpi=300)

plt.figure()
fig, ax = plt.subplots()
ax.scatter(np.array([x[0] for x in priceRrankList]), np.array([x[1] for x in priceRrankList]))
plt.xlabel('price($)')
plt.ylabel('sales rank')
plt.title('sales rank vs. price for all the juicers')
plt.savefig("../out/sales-rank-vs-price-for-all-juicers.png", dpi=300)

plt.figure()
fig, ax = plt.subplots()
pricelist = [x[0] for x in priceRrankList]
# the histogram of the data
n, bins, patches = ax.hist(pricelist, 100, facecolor='blue', alpha=0.75)
mu = np.mean(np.array(pricelist))
sigma = np.std(np.array(pricelist))

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
ax.plot(bins, y, linewidth=1)

plt.xlabel('price($)')
plt.ylabel('# of juicers')
plt.title('price($) histogram for all the juicers')
plt.savefig("../out/price-histogram-for-all-juicers.png", dpi=300)

#plt.show()

plt.figure()
fig, ax = plt.subplots()
ranklist = [x[1] for x in priceRrankList]
# the histogram of the data
n, bins, patches = ax.hist(ranklist, 100, facecolor='blue', alpha=0.75)
mu = np.mean(np.array(ranklist))
sigma = np.std(np.array(ranklist))

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
ax.plot(bins, y, linewidth=1)
plt.xlabel('sales rank')
plt.ylabel('# of juicers')
plt.title('sales rank histogram for all the juicers')
plt.savefig("../out/sales-rank-histogram-for-all-juicers.png", dpi=300)

for cat, l in priceRankListByCategory.items():
    plt.figure()
    fig, ax = plt.subplots()
    ranklist = [x[0] for x in l]
    # the histogram of the data
    n, bins, patches = ax.hist(ranklist, 100, facecolor='blue', alpha=0.75)
    mu = np.mean(np.array(ranklist))
    sigma = np.std(np.array(ranklist))

    # add a 'best fit' line
    y = mlab.normpdf(bins, mu, sigma)
    ax.plot(bins, y, linewidth=1)
    plt.xlabel('Price($)')
    plt.ylabel('# of juicers')
    plt.title('Price histogram for {0} juicers'.format(cat))
    plt.savefig("../out/price-histogram-for-{0}-juicers.png".format(cat), dpi=300)

    plt.figure()
    fig, ax = plt.subplots()
    ranklist = [x[1] for x in l]
    # the histogram of the data
    n, bins, patches = ax.hist(ranklist, 100, facecolor='blue', alpha=0.75)
    mu = np.mean(np.array(ranklist))
    sigma = np.std(np.array(ranklist))

    # add a 'best fit' line
    y = mlab.normpdf(bins, mu, sigma)
    ax.plot(bins, y, linewidth=1)
    plt.xlabel('sales rank')
    plt.ylabel('# of juicers')
    plt.title('sales rank histogram for {0} juicers'.format(cat))
    plt.savefig("../out/sales-rank-histogram-for-{0}-juicers.png".format(cat), dpi=300)


juicersByAsinByCategory = {}
for asin, juicer in juicersByAsin.items():
    cat = juicer['category']
    juicersByAsinByCategory.setdefault(cat, {}).update({asin: juicer})

juicerCountByCategory = {}
for cat, juicers in juicersByAsinByCategory.items():
    juicerCountByCategory.update({cat:len(juicers)})
    print("#juicers[{0}] = ".format(cat), len(juicers))

labels = list(juicerCountByCategory.keys())
mxJuicerCnt = max(list(juicerCountByCategory.values()))
sizes = [x/mxJuicerCnt * 100 for x in list(juicerCountByCategory.values())]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title('Juicer Counts by Category')

plt.savefig("../out/juicer-count-by-category.png", dpi=300)

avgRankByCategory = {}
for cat, juicers in juicersByAsinByCategory.items():
    mn = np.mean(np.array([int(x['sales_rank']) for x in filter(lambda a: a['sales_rank'] != 'None', list(juicers.values()))]))
    avgRankByCategory.update({cat:mn})
    print("mean_sales_rank[{0}] = ".format(cat), int(mn))

fig, ax = plt.subplots()
fig.canvas.draw()
ax.bar(np.arange(len(avgRankByCategory)), list(avgRankByCategory.values()))
ax.set_xticks(np.arange(len(avgRankByCategory)))
ax.set_xticklabels(list(avgRankByCategory.keys()))
plt.xlabel('Juicer Category')
plt.ylabel('Sales Rank')
plt.title('Sales Rank by Juicer Category')
plt.savefig("../out/sales-rank-by-category.png", dpi=300)

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
    fig.subplots_adjust(bottom=0.45)
    plt.savefig("../out/brands-by-sales-rank-for-{0}-juicers.png".format(cat), dpi=300)


avgRankByBrand = {}
for brand, l in rankListByBrand.items():
    avg = np.mean(np.array(l))
    avgRankByBrand.update({brand:avg})


print("number of brands = ", len(rankListByBrand))
print("brand list: ", rankListByBrand.keys())

pass
