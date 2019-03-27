import re
import json


TAGS = re.compile(r'<.*?>')
LINES = re.compile(r'\n|\t|\r')
STYLE = re.compile(r'<style.*?>.*?</style>', re.I)
SCRIPT = re.compile(r'<script.*?>.*?</script>', re.I)
BRACKET = re.compile(r'\(.*?\)')
NBSP = re.compile(r'&nbsp;')
AMP = re.compile(r'&amp;')
GT = re.compile(r'&gt;')
COMMAS = re.compile(r',')
NUMBER = re.compile(r'[^0-9]+')
PRICE = re.compile(r'[^0-9\.]+')
DATE_FIRST = re.compile(r'Date first', re.I) #定义排名后面字符串的去除规则
SHIPPING_WEIGHT = re.compile(r'Shipping Weight', re.I)
Customer_Reviews = re.compile(r'Customer Reviews', re.I)
SHIPPING_INFORMATION = re.compile(r'Shipping Information', re.I)
ASIN_LIST = re.compile(r'"dimensionValuesDisplayData" : {(.*?)},', re.I)


# 清洗HTML
def clean_html(html):
    html = LINES.sub('', html)
    html = STYLE.sub('', html)
    html = SCRIPT.sub('', html)
    html = BRACKET.sub('', html)
    html = TAGS.sub('', html)
    html = NBSP.sub(' ', html)
    html = AMP.sub('&', html)
    html = GT.sub('>', html)
    html = COMMAS.sub('', html)
    return html

# 获取排名
def get_rank(html):
    # print("HTML")
    # print(html)
    sales_rank = []
    ranks_list = html.split('#')
    # print(ranks_list)
    for ranks in ranks_list[1:]:
        # print("清晰")
        # print(ranks)
        try:
            rank, category = re.split(r'in', ranks, 1)
            rank=re.match(r'[0-9]{1,9}',rank).group()
            sales_rank.append((int(rank), category.strip()))
        except:
            for ranks in ranks_list[2:]:
                rank, category = re.split(r'in', ranks, 1)
                rank = re.match(r'[0-9]{1,9}', rank).group()
                sales_rank.append((int(rank), category.strip()))

    if sales_rank:
        # print("DATA_DFFFFFFFFF")
        sales_rank[-1] = (sales_rank[-1][0], DATE_FIRST.split(sales_rank[-1][1])[0].strip())
        if len(sales_rank[-1][1]) < 50:
            sales_rank[-1] = sales_rank[-1]
        else:
            sales_rank[-1] = (sales_rank[-1][0], SHIPPING_WEIGHT.split(sales_rank[-1][1])[0].strip())
            if len(sales_rank[-1][1]) < 50:
                sales_rank[-1] = sales_rank[-1]
            else:
                sales_rank[-1] = (sales_rank[-1][0], Customer_Reviews.split(sales_rank[-1][1])[0].strip())
                if len(sales_rank[-1][1]) < 50:
                    sales_rank[-1] = sales_rank[-1]
                else:
                    sales_rank[-1] = (sales_rank[-1][0], SHIPPING_INFORMATION.split(sales_rank[-1][1])[0].strip())

    return sales_rank

# 清洗价格
def get_price(text):
    return PRICE.sub('', text)


# 获取seller_id
def get_seller_id(url):
    reg = re.compile(r'.*?seller=([0-9a-zA-Z]+).*?')
    result = reg.search(url.split('/')[-1]).group(1)
    return result

def clean_asin(text):
    return text.split('/')[-2]


def get_first_img(text):
    data = json.loads(text)
    data = sorted(data.items(), key=lambda d:d[1][0], reverse=True)
    return data[0][0]
#q清晰url
def get_category_url(url):
    return url.split(r'ref=zg_bs')[0]

# 从js中获取asin列表
# def get_asin_list_from_text(text):
#     result = ASIN_LIST.findall(text)
#     asin_list = []
#     if len(result) > 0:
#         result = [x for x in result if x]
#         if result:
#             result = json.loads('{%s}' % result[0])
#             asin_list = [x for x in result]
#     return asin_list


def get_url_title(url):
    pp = ""
    a = pp.join(url)
    url = a.split('(')[0]
    return url

def get_url_product(url):
    # a = "https://www.amazon.com/Arizona-Diamondbacks-Mens-Clean-Black/dp/B00D4VEYN6/ref=zg_bs_7586165011_1?_encoding=UTF8&psc=1&refRID=60X1RB2WD4KB6FEVR3EM"
    aa = url.split('ref')[0].split('dp')[1].split('/')[1]
    old = 'https://www.amazon.com/dp/'
    url_product = old + aa
    # print(c)
    return url_product