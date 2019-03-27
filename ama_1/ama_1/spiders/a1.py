# -*- coding: utf-8 -*-
import scrapy

import re
import scrapy
import pymysql
# from parsing import settings

import re
# from parsing.items import ParsingItem
# from usa_ama.clean1.clean_product import clean_html, get_rank, get_seller_id, clean_asin, get_first_img
from ama_1.clean.clean_product import get_url_product,get_url_title,clean_html, get_rank, get_seller_id, clean_asin, get_first_img
class A1Spider(scrapy.Spider):
    name = 'a1'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/dp/B01J6RPDWC']

    def parse(self, response):
        print(response.url)
        # 标题
        title_old = response.xpath(".//span[@id='productTitle']/text()").extract_first()
        if title_old is not None:
            title_old = title_old.strip()
        else:
            title_old = response.xpath(".//span[@id='ebooksProductTitle']/text()").extract_first()
            if title_old is not None:
                title_old = title_old.strip()
            else:
                title_old = response.xpath("//span[@id='btAsinTitle']/text()").extract_first()
                title_old = title_old
        title_onew = '' if title_old is None else title_old
        print("标题")
        print(title_old)
        img_url = response.xpath('//div[@id="imgTagWrapperId"]/img/@data-a-dynamic-image').extract_first()
        if img_url is not None:
            print("图片1")
            img_url = get_first_img(img_url)
            if img_url is not None:
                img_url = img_url
            else:
                img_url = response.xpath("//div[@class='a-section gc-design-image-wrapper']//img/@src").extract_first()
        else:
            print("图片2")
            img_url = response.xpath("//div[@id='imageBlockThumbs']/span/div/img/@src").extract_first()
            if img_url is not None:
                img_url = img_url
            else:
                img_url = response.xpath("//div[@class='image-wrapper']//img/@src").extract_first()
                if img_url is not None:
                    img_url = img_url
                else:
                    img_url = response.xpath(".//div[@id='ebooks-img-wrapper']/div/img/@src").extract_first()
                    if img_url is not None:
                        img_url = img_url
                    else:
                        img_url = response.xpath("//img[@id='gc-standard-design-image']/@src").extract_first()
        img_url = '' if img_url is None else img_url
        print("图片")
        print(img_url)
        # 价格
        price = response.xpath('//span[@id="priceblock_saleprice"]/text()').extract_first()
        if price is None:
            price = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract_first()
        if price is None:
            price = response.xpath('//span[starts-with(@id, "priceblock")]/text()').extract_first()
        if price is None:
            price = response.xpath("//div[@id='buyNew_noncbb']/span/text()").extract_first()
        if price is None:
            price = response.xpath("//div[@class='inlineBlock-display']/span/text()").extract_first()
        if price is None:
            price = response.xpath(
                "//div[@class='a-column a-span3 a-text-right a-span-last']/span/text()").extract_first()
        if price is None:
            price = response.xpath("//tr[@class='digital-list-price']/td/span/text()").extract_first()
        if price is None:
            price = response.xpath(
                "//tr[@class='kindle-price']/td[@class='a-color-price a-size-medium a-align-bottom']/text()").extract_first()
        if price is None:
            # print("价格")
            price = response.xpath(
                "//p[@class='a-spacing-medium a-text-center']/span[@class='a-color-price a-text-bold']/text()").extract_first()
        if price is None:
            # print("价格")
            price = response.xpath("//span[@class='p13n-sc-price']/text()").extract_first()
            # price = response.xpath("//span[@class='gc-live-preview-amount']/text()").extract_first()

        # price = '' if price is None else price.strip()
        if price is not None:
            price_s = re.compile(r'[^0-9\.]+')
            price = price_s.sub('', price)
            # price=re.search("\d+(\.\d+)?",price).group()#d第一次写的正则
        print("价格")
        print(price)

        # 卖家名字
        seller_name = response.xpath('//div[@id="merchant-info"]/a[1]/text()').extract_first()
        if seller_name is not None:
            seller_name = seller_name
            # seller_name = response.xpath('//span[@id="merchant-info"]/a[1]/text()').extract_first()
        else:
            seller_name = response.xpath("//div[@id='merchant-info']/text()").extract_first()
            if seller_name is not None:
                # print(seller_name)
                seller_name = seller_name.strip()
                seller_name_re = re.compile(r'sold by', re.I)
                try:
                    seller_name = seller_name_re.split(seller_name)[1]
                except:
                    seller_name = response.xpath(
                        "//div[@class='a-section a-spacing-base']/div[@class='a-row']/a[@class='a-link-normal']/text()").extract_first()


            else:
                seller_name = response.xpath('//a[@id="bylineInfo"]/text()').extract_first()
                if seller_name is not None:
                    seller_name = seller_name
                else:
                    seller_name = response.xpath("//div[@class='a-box-inner a-padding-none']/p/text()").extract_first()
                    if seller_name is not None:
                        seller_name = seller_name.strip()
                        seller_name_re = re.compile(r'by', re.I)
                        seller_name = seller_name_re.split(seller_name)[1]
                        seller_name_re = re.compile(r',', re.I)
                        seller_name = seller_name_re.split(seller_name)[0]
                    else:
                        print("去哪里")
                        seller_name = response.xpath(
                            "//div[starts-with(@class, 'content')]//b[contains(text(),'by')]/..").extract_first()
                        if seller_name is not None:
                            seller_name = clean_html(seller_name)
                            seller_name = seller_name.strip()
                            seller_name = seller_name.split(":")[1]
                        else:
                            seller_name = response.xpath("//div[@id='gc-brand-name']/a/text()").extract_first()
                            seller_name = seller_name
        if seller_name is None:
            seller_name = response.xpath("//span[@class='author notFaded']/a/text()").extract_first()

        seller_name = '' if seller_name is None else seller_name.strip()
        # store_name_1 = response.xpath("//div[@class='feature']/div/a/text()").extract_first()
        # store_name='' if store_name_1 is None else store_name_1.strip()
        print("卖家名字")
        print(seller_name)
        # 评论数量
        reivews = response.xpath(".//span[@id='acrCustomerReviewText']/text()").extract_first()
        if reivews is not None:
            reivews = reivews.strip()
            reivews = re.search("^\d{1,9}(,\d{1,9})|\d+", reivews).group()
        else:
            if reivews is not None:
                reivews = response.xpath(
                    "//span[@class='a-size-small']/a[@class='a-link-normal']/text()").extract_first()
                reivews = reivews.strip()
                reivews = re.search("^\d{1,9}(,\d{1,9})", reivews).group()
        reivews = '' if reivews is None else reivews

        print("评价数量")
        print(reivews)
        # 等级
        rating = response.xpath(".//span[@class='arp-rating-out-of-text a-color-base']/text()").extract_first()
        if rating is not None:
            rating = '' if rating is None else rating.strip()
            rating = re.search("\d+(\.\d+)?", rating).group()
        # rating=re.search("[1-9]{1}(\.\d{0,1})?",reivews_2).group()  ##?#/\d{1,8}(\.\d{0,2})?/???
        rating = '' if rating is None else rating
        print('星级')
        print(rating)
        # 排名
        rank_htm = response.xpath('//table[@id="productDetails_detailBullets_sections1"]').extract_first()  # 排名
        if rank_htm is not None:
            # print("zaina在哪")
            # print(rank_htm)
            rank_htm = rank_htm
        else:
            rank_htm = response.xpath('//li[@id="SalesRank"]').extract_first()
        # print(html_rank)
        if rank_htm is not None:
            rank_htm = clean_html(rank_htm)
            # print(rank_htm)

            rank_htm = get_rank(rank_htm)
        else:

            rank_htm = response.xpath('//tr[@id="SalesRank"]').extract_first()
            if rank_htm is not None:
                rank_htm = clean_html(rank_htm)
                rank_htm = get_rank(rank_htm)
            else:
                rank_htm = []
        print("各排名")
        print(rank_htm)
        # 尺寸
        size_html = response.xpath('//table[@id="productDetails_detailBullets_sections1"]').extract_first()  # 尺寸
        if size_html is not None:
            size_html_1 = response.xpath(
                "//table[@id='productDetails_detailBullets_sections1']//th[contains(text(),'Dimensions')]/../td/text()").extract_first()  # 查看是否有尺寸数据
            if size_html_1 is not None:
                # print("111")
                size_html = clean_html(size_html_1)
                size_html = size_html.split('Dimensions')
                for size_html in size_html[0:]:
                    size_html, w_size_1 = re.split(r'inches', size_html, 1)
                    size_html = '' if size_html is None else size_html.strip()
            else:
                # print("222")
                size_html = response.xpath(
                    "//table[@id='productDetails_techSpec_section_1']//th[contains(text(),'Dimensions')]/../td/text()").extract_first()  # 第二种情况
                if size_html is not None:
                    size_html = clean_html(size_html)
                    size_html = size_html.split('Dimensions')
                    for size_html in size_html[0:]:
                        # print("尽量")
                        size_html, w_size_2 = re.split(r'inches', size_html, 1)
                        size_html = '' if size_html is None else size_html.strip()
                else:
                    size_html = response.xpath(
                        "//table[@id='productDetails_techSpec_section_2']//th[contains(text(),'Dimensions')]/../td/text()").extract_first()
                    if size_html is not None:

                        size_html = clean_html(size_html)
                        size_html = size_html.split('Dimensions')
                        for size_html in size_html[0:]:
                            # print("尽量")
                            size_html, w_size_2 = re.split(r'inches', size_html, 1)
                            size_html = '' if size_html is None else size_html.strip()

        else:
            size_html = response.xpath(
                "//div[starts-with(@class, 'content')]//b[contains(text(),'Dimensions')]/../..").extract_first()
            if size_html is not None:

                size_html = clean_html(size_html)
                size_html = size_html.split('Dimensions')
                for size_html in size_html[1:]:
                    size_html, w = re.split(r'inches', size_html, 1)
                    size_html = '' if size_html is None else size_html.strip()
                    size_html = size_html.split(':')[1]
                    size_html = '' if size_html is None else size_html.strip()
            else:
                size_html = response.xpath("//div[@class='pdTab']//td[contains(text(),'Dimensions')]").extract_first()
                # size_html = response.xpath("//div[starts-with(@class,'pdTab')]/table/tbody").extract_first() #有问题
                if size_html is not None:
                    size_html = response.xpath("//div[@class='pdTab']").extract_first()
                    print(size_html)

                    size_html = clean_html(size_html)
                    # size_html=re.search(r'(?="inches")',size_html)
                    size_html = size_html.split('Dimensions')
                    print(size_html)
                    for size_html in size_html[1:]:
                        size_html, w = re.split(r'inches', size_html, 1)
                        size_html = '' if size_html is None else size_html.strip()
                else:
                    size_html = response.xpath(
                        "//table[@id='tech-specs-table-left']//p[contains(text(),'Size')]/../..").extract_first()
                    # print(size_html)
                    if size_html is not None:

                        size_html = clean_html(size_html)
                        # print(size_html)
                        size_html = size_html.split('Size')[1]
                        # print(size_html)
                        we = "x"
                        size_html = re.findall(r'(\d+\.\d+)', size_html)
                        # print(size_html)
                        size_html = we.join(size_html)
                        if len(size_html) < 10:
                            size_html = response.xpath(
                                "//table[@id='tech-specs-table-left']//p[contains(text(),'Size')]/../..").extract_first()
                            size_html = clean_html(size_html)
                            size_html = size_html.split('Size')[1]
                            we = "x"
                            size_html = size_html.split("|")[1]
                            size_html = re.findall(r'([0-9][0-9])', size_html)
                            size_html = we.join(size_html)

        print("尺寸")
        print(size_html)
        # html_size = re.search("([0-9]+)\n [x]([0-9]+)\n [x]([0-9]+)", html_size) #正则匹配去掉尺寸单位
        # 重量
        html_weight = response.xpath('//table[@id="productDetails_detailBullets_sections1"]').extract_first()  # 尺寸
        if html_weight is not None:
            print("重量1")
            html_weight_shipp = response.xpath(
                "//table[@id='productDetails_detailBullets_sections1']//th[contains(text(),'Shipping Weight')]/../td/text()").extract_first()  # 查看是有有重量数据
            if html_weight_shipp is not None:
                print("重量2")
                html_weight_ounces = response.xpath(
                    "//table[@id='productDetails_detailBullets_sections1']//td[contains(text(),'ounces')]/../td/text()").extract_first()  # 查看单位是什么？
                if html_weight_ounces is not None:
                    html_weight = clean_html(html_weight)
                    html_weight = html_weight.split('Shipping Weight ')  # Item Weight 用哪个字符串分裂 还要看情况
                    for html_weight in html_weight[1:]:
                        # print("重量 onces")
                        # print(html_weight)
                        try:
                            html_weight, w_ounces_2 = re.split(r'ounces', html_weight, 1)  # 有pounds和ounces两种
                            html_weight = '' if html_weight is None else html_weight.strip()
                        except:
                            html_weight, w_ounces_2 = re.split(r'pounds ', html_weight, 1)  # 有pounds和ounces两种
                            html_weight = '' if html_weight is None else html_weight.strip()

                else:
                    html_weight = clean_html(html_weight)
                    html_weight = html_weight.split('Weight ')  # 拿到文本还没解析
                    for html_weight in html_weight[1:]:
                        html_weight, w2 = re.split(r'pounds', html_weight, 1)  # 有pounds和ounces两种
                        html_weight = '' if html_weight is None else html_weight.strip()
            else:
                print("重量3")
                html_weight_Item = response.xpath(
                    "//table[@id='productDetails_detailBullets_sections1']//th[contains(text(),'Item Weight')]/../td/text()").extract_first()
                if html_weight_Item is not None:
                    print("重量3+1")
                    html_weight_ounces = response.xpath(
                        "//table[@id='productDetails_detailBullets_sections1']//td[contains(text(),'ounces')]/../td/text()").extract_first()  # 查看单位是什么？
                    if html_weight_ounces is not None:
                        print("3+2")
                        html_weight = clean_html(html_weight)
                        html_weight = html_weight.split('Item Weight ')  # Item Weight 用哪个字符串分裂 还要看情况
                        for html_weight in html_weight[1:]:
                            # print("重量 onces")
                            # print(html_weight)
                            html_weight, w_ounces_2 = re.split(r'ounces', html_weight, 1)  # 有pounds和ounces两种
                            html_weight = '' if html_weight is None else html_weight.strip()
                    else:
                        print("3+3")
                        html_weight = clean_html(html_weight)
                        html_weight = html_weight.split('Weight ')  # 拿到文本还没解析
                        for html_weight in html_weight[1:]:
                            html_weight, w2 = re.split(r'pounds', html_weight, 1)  # 有pounds和ounces两种
                            html_weight = '' if html_weight is None else html_weight.strip()
                else:
                    html_weight = []

        else:
            # html_weight = response.xpath("//div[starts-with(@class, 'content')]//b[contains(text(),'Product ')]/../text()").extract_first()
            # html_weight = html_weight.split(';')[1] #正则去去重量单位
            # html_weight = '' if html_weight is None else html_weight.strip()
            print("zho重量4")
            html_weight = response.xpath(
                "//div[starts-with(@class, 'content')]//b[contains(text(),'Weight')]/../..").extract_first()
            if html_weight is not None:
                html_weight_text = response.xpath(
                    "//div[starts-with(@class, 'content')]//b[contains(text(),'Weight')]/../..").extract_first()
                if html_weight_text is not None:
                    html_weight = clean_html(html_weight)
                    # size_html=re.search(r'(?="inches")',size_html)
                    # print("到周六")
                    html_weight = html_weight.split('Weight')  # 拿到文本还没解析
                    # print(html_weight)
                    for html_weight in html_weight[1:]:
                        # print(html_weight)
                        try:
                            html_weight, w = re.split(r'pounds', html_weight, 1)
                            html_weight = '' if html_weight is None else html_weight.strip()
                            html_weight = html_weight.split(':')[1]
                            html_weight = '' if html_weight is None else html_weight.strip()
                        except:
                            html_weight, w = re.split(r'ounces', html_weight, 1)
                            html_weight = '' if html_weight is None else html_weight.strip()
                            html_weight = html_weight.split(':')[1]
                            html_weight = '' if html_weight is None else html_weight.strip()
            else:
                html_weight = response.xpath("//div[@class='pdTab']").extract_first()

                if html_weight is not None:
                    html_weight = response.xpath("//div[@class='pdTab']//td[contains(text(),'pounds')]").extract_first()
                    if html_weight is not None:
                        # print(html_weight)
                        html_weight = clean_html(html_weight)
                        # size_html=re.search(r'(?="inches")',size_html)
                        html_weight = html_weight.split('Weight')
                        # print(html_weight)
                        for html_weight in html_weight[0:]:
                            html_weight, w = re.split(r'pounds', html_weight, 1)
                            html_weight = '' if html_weight is None else html_weight.strip()
                    else:
                        html_weight = response.xpath(
                            "//div[@class='pdTab']//td[contains(text(),'ounces')]").extract_first()
                        if html_weight is not None:
                            html_weight = clean_html(html_weight)
                            # size_html=re.search(r'(?="inches")',size_html)
                            html_weight = html_weight.split('Weight')
                            for html_weight in html_weight[1:]:
                                html_weight, w = re.split(r'ounces', html_weight, 1)
                                html_weight = '' if html_weight is None else html_weight.strip()
                else:
                    html_weight = response.xpath(
                        "//table[@id='tech-specs-table-left']//p[contains(text(),'Weight')]/../..").extract_first()
                    if html_weight is not None:
                        html_weight = clean_html(html_weight)
                        html_weight = (html_weight.split('Weight')[1]).split('ounces')[0].strip()
        print("重量")
        print(html_weight)
        # ------------------------------------------------------------------------------------------------------------
        # asin 方法一
        # asin_html=response.xpath('//table[@id="productDetails_detailBullets_sections1"]').extract_first()
        # if asin_html is not None:
        #     print("as1")
        #     asin_html = clean_html(asin_html)
        #     asin_html =asin_html.split('ASIN')
        #     for asin_html in asin_html[1:]:
        #         asin_html,w3= re.split(r'Item', asin_html,1)
        #         asin_html='' if asin_html is None else asin_html.strip()
        # else:
        #     print("as2")
        #     asin_html = response.xpath(
        #         "//div[starts-with(@class, 'content')]//b[contains(text(),'ASIN: ')]/../..").extract_first()
        #     if asin_html is not None:
        #         asin_html = clean_html(asin_html)
        #         asin_html = asin_html.split('ASIN')
        #         for asin_html in asin_html[1:]:
        #             asin_html, w3 = re.split(r'Item', asin_html, 1)
        #             asin_html = '' if asin_html is None else asin_html.strip()
        #     else:
        #         print("as3")
        #         asin_html = response.xpath("//div[starts-with(@class,'pdTab')]//td[contains(text(),'ASIN')]/../..").extract_first()
        #         asin_html = clean_html(asin_html)
        #         asin_html = asin_html.split('ASIN')
        #         for asin_html in asin_html[1:]:
        #             asin_html, w3 = re.split(r'Customer ', asin_html, 1)
        #             asin_html = '' if asin_html is None else asin_html.strip()
        #
        # print("ASIN")
        # print(asin_html)
        # ---------------------------------------------------------------------------------------------------
        # asin  方法二
        asin_html = response.xpath("//div[@id='cerberus-data-metrics']/@data-asin").extract_first()

        if asin_html is not None:
            asin_html = asin_html
        else:
            asin_html = response.xpath("//div[@id='fast-track']/input//@value").extract_first()
            if asin_html is not None:
                asin_html = asin_html
            else:
                asin_html = response.xpath("//div[@class='a-hidden']/@data-asin").extract_first()
                if asin_html is not None:
                    asin_html = asin_html
                else:
                    asin_html = response.xpath(
                        '//div[@class="a-box-inner a-padding-base"]/form/input[@name="ASIN.0"]/@value').extract_first()

        if asin_html is not None:
            asin_html = asin_html
        else:
            asin_html = response.xpath(
                '//div[@class="a-box-inner a-padding-base"]/form/input[@name="ASIN.0"]/@value').extract_first()
            if asin_html is not None:
                asin_html = asin_html
            else:
                asin_html = response.xpath(
                    "//div[starts-with(@class, 'content')]//b[contains(text(),'ASIN:')]/..").extract_first()
                asin_html = clean_html(asin_html)
                try:
                    asin_html = asin_html.split('ASIN:')[1].strip()
                except:
                    asin_html = asin_html.split('ASIN')[1].strip()

        print("ASIN")
        print(asin_html)

        # 上架时间
        # 大体上是两种页面结构，每种页面结构上架时间也不一样
        first_time_html = response.xpath(
            "//table[@id='productDetails_detailBullets_sections1']//th[contains(text(),'Date')]/../td/text()").extract_first()
        if first_time_html is not None:
            first_time_html = first_time_html
            first_time_html = '' if first_time_html is None else first_time_html.strip()
        else:
            first_time_html = response.xpath(
                "//div[starts-with(@class, 'content')]//b[contains(text(),'Date')]/..").extract_first()
            if first_time_html is not None:
                first_time_html = clean_html(first_time_html)
                try:
                    first_time_html = first_time_html.split('Date:')[1]
                except:
                    first_time_html = first_time_html.split(':')[1]
            else:
                first_time_html = response.xpath(
                    "//table[@id='tech-specs-table-right']//p[contains(text(),'Generation')]/../..").extract_first()
                if first_time_html is not None:

                    first_time_html = clean_html(first_time_html)
                    first_time_html = first_time_html.split('Generation')[1]
                else:  # 书的上架时间没解决
                    print("书店的上架时间")
                    p = ""
                    first_time_html = response.xpath(
                        "//div[starts-with(@class, 'content')]//b[contains(text(),'Publisher')]/..").extract_first()
                    print(first_time_html)
                    # first_time_html = clean_html(first_time_html)
                    print(first_time_html)
                    first_time_html = re.findall(r'<li><b>.*?</b>(.*?)</li>', first_time_html, re.S)
                    first_time_html = p.join(first_time_html)
                    first_time_html = first_time_html.split('(')[1]
                    first_time_html = first_time_html.split(')')[0]
                    first_time_html = first_time_html.strip()
                    print(first_time_html)

        first_time_html = '' if first_time_html is None else first_time_html
        print("上架时间")
        print(first_time_html)

        #   Q&A的数量（评价回答数量）
        answer_num = response.xpath("//a[@id='askATFLink']/span/text()").extract_first()
        if answer_num is not None:
            answer_num = answer_num.strip()
            answer_num = re.search("\d+(\.\d+)?", answer_num).group()
        else:
            answer_num = []
        # answer_num = '' if answer_num is None else answer_num.strip()
        # answer_num = re.search("\d+(\.\d+)?", answer_num).group()
        print("回答数量")
        print(answer_num)
