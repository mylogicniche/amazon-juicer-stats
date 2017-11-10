import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pandas as pd
import re
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from collections import Counter
from nltk.corpus import stopwords
import string
import operator

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

df_all = pd.DataFrame(juicersByAsin)
df_all = df_all.transpose()
df_all = df_all[~df_all['price'].isnull()]
df_all = df_all[~df_all['color'].isnull()]
df_all = df_all[~(df_all['sales_rank'] == 'None')]
print("{0} number of juicers available with price info".format(df_all.shape[0]))

df_all = df_all.dropna()
print(df_all.shape[0])

def clean_price(s):
    s = re.findall("\d+\.\d+",s)
    if s:
        return s[0]
    return 0

df_all['price'] = df_all['price'].apply(clean_price).astype(float)

df_all = df_all[df_all['price']!=0]

df_all = df_all.dropna()

def clean_brand(s):
    return s.split(" ")[0]

df_all["new_brands"] = df_all["brand"].apply(clean_brand)

allbrands = df_all["new_brands"].unique()

print(df_all)

bybrands = df_all.pivot_table(index=["new_brands"], values=["price"], aggfunc=np.mean)
bycategory = df_all.pivot_table(index=["category"], values=["price"], aggfunc=np.mean)
bybrands = bybrands.sort_values(by="price", ascending=False)
brandprice = dict(bybrands['price']/max(bybrands['price']))
catprice = dict(bycategory['price']/max(bycategory['price']))

def calc_price_weights(brand):
    for key,val in brandprice.items():
        if key == brand:
            return val
    return 0

def calc_price_weights_by_cat(cat):
    for key,val in catprice.items():
        if key == cat:
            return val
    return 0

df_all['brand weight'] = df_all['brand'].apply(calc_price_weights)
df_all['category weight'] = df_all['category'].apply(calc_price_weights_by_cat)

df_all['sales_rank'] = df_all['sales_rank'].astype(int)
df_all['price'].hist()
plt.show()

def sale_rank_weight(s):
    if s > 480000:
        return  0
    else:
        return 1
df_all['sales rank weight'] = df_all['sales_rank'].apply(sale_rank_weight)

def clean_color(s):
    excep = ['stainless', 'steel', 'brushed stainless steel']
    if s.lower() in excep:
        return 'stainless steel'
    return s.lower()

df_all['color'] = df_all['color'].apply(clean_color)

bycolor = df_all.pivot_table(index=["color"], values=["price"], aggfunc=np.mean)
print(bycolor)
colorprice = dict(bycolor['price']/max(bycolor['price']))

def calc_price_weights_by_color(color):
    for key,val in colorprice.items():
        if key == color:
            return val
    return 0

df_all['color weight'] = df_all['color'].apply(calc_price_weights_by_color)

print(bybrands)
print(bycategory)

print(len(allbrands))

print(df_all.columns)

print(df_all.head())
plt.scatter(df_all['sales_rank'], df_all['price'])
plt.show()

def get_words(df):
    words = []
    for lis in df['features'].values:
        for l in lis:
            words.extend(l.split(" "))
    return [w.lower() for w in words]

all_words = get_words(df_all)

high_words = set(get_words(df_all[df_all['price'] > 100]))
low_words = set(get_words(df_all[df_all['price'] <= 100]))

print(high_words & low_words)

high_only = list(high_words - (high_words & low_words))

d = {}
for word in high_only:
    l = get_words(df_all[df_all['price'] > 100])
    d.update({word: l.count(word)})

print("cool", sorted(d.items(), key=operator.itemgetter(1), reverse=True))

cachedStopWords = stopwords.words("english")
all_words = [w.lower() for w in all_words if not w in cachedStopWords]
all_words = [''.join(c for c in s if c not in string.punctuation) for s in all_words]
print(Counter(all_words))

def featuring(lis):
    for l in lis:
        if "nut" in l:
            return 1
    else:
        return 0

df_all['features weight'] = df_all['features'].apply(featuring)
print(df_all.pivot_table(index='features weight', values='price', aggfunc=np.mean))

X = df_all[['brand weight', 'category weight', 'color weight', 'features weight']]
y = df_all['price']

print(X)

lr = linear_model.LinearRegression()
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=.33)
model = lr.fit(X_train, y_train)
print ("R^2 is: \n", model.score(X_test, y_test))

