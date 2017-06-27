from amazon_scraper import AmazonScraper
from time import sleep
import json
import time
import simplejson

amzn = AmazonScraper("AKIAIM5AOOMVJVPWCCSQ", "kupGH8IrcXAjb6NQF3Ns+MZAHT0yrMnnvApNd2ru", "adthomas-20", MaxQPS=0.5)

p = amzn.lookup(ItemId='B001L7OIVI')

whole_reviews = {}
f = open('data.json', 'w')

review_page_str = '/ref=cm_cr_getr_d_paging_btm_{pgno}?sortBy=bySubmissionDateDescending&pageNumber={pgno}'

dataDict = {}
total_comment = 0

for i in range(1,293):
    start_time = time.time()
    surl = p.reviews_url.split('/')
    s = 'https://' + surl[2] + '/' + surl[3] + '/' + surl[4] + review_page_str.replace('{pgno}', str(i))
    print(s)

    rs = amzn.reviews(URL=s)
    print(rs.ids)

    for ids in rs.ids:
        #try:
        r = amzn.review(Id=ids)
        whole_reviews.update({ids:r.text})
        d = {
            'asin':    r.asin,
            'date':    r.date.strftime("%c"),
            'rating':  r.rating,
            'title':   r.title,
            'text':    r.text,
            'user':    r.user,
            'user_id': r.user_id
        }
        dataDict.update({ids:d})
        total_comment += 1
        sleep(5)
        #except:
           # pass

    print("pageno = ",i)
    print("total comment = ", total_comment)
    elapsed_time = time.time() - start_time
    sleep(5)
    print(elapsed_time)

try:
    json.dump(dataDict, f, indent=4)
except:
    pass

f.close()
pass