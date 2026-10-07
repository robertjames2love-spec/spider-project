import time
import traceback
from config_util import read_domian

from DrissionPage import ChromiumOptions, Chromium
from re_util import get_size, get_overview_size


class Chrome:
    def __init__(self):
        print('init chrome')
        chromium_options = ChromiumOptions()
        # chromiumOptions.auto_port()
        chromium_options.set_local_port(9600)
        chromium_options.headless()
        self.chromium = Chromium(chromium_options)
        self.tab = self.chromium.latest_tab

    def get_setup(self):
        smalls = self.tab.eles('@tag()=small')
        for small in smalls:
            if small.text.startswith('Setup: '):
                text = small.text
                start_index = text.find('$')
                end_index = text.find(';')
                return text[start_index+1:end_index]
        return None

    def handle(self, number):
        try:
            domain = read_domian()
            time.sleep(1)
            self.tab.get(f'https://{domain}/:quicksearch.htm?quicksearchbox={number}')

            # 判断跳转到列表还是直接跳转
            thumbnail_list = self.tab.ele('@class=thumbnail-list')
            if thumbnail_list:
                lis = thumbnail_list.eles('@tag()=li')
                print('搜索结果个数', len(lis))
                if len(lis) > 1:
                    print('搜索结果有多个，手动跳转')
                    li = lis[0]
                    # print(li.html)

                    a = li.ele('@tag()=a')
                    # print(a.html)
                    href = a.attr('href')
                    print('跳转地址', href)
                    self.tab.get(href)
            else:
                print('直接地址', self.tab.url)

            result = {}

            # 导航
            ol = self.tab.ele('@class=breadcrumb')
            # print(ol.html)
            nav = ol.eles('@tag()=li')[1].text
            # print('nav', nav)
            result['nav'] = nav

            # 标题
            title = self.tab.ele('@class=product-name').text
            # print('title', title)
            result['title'] = title

            overview = self.tab.ele('@class=item-desc').text
            # print('overview', overview)
            result['overview'] = overview

            index = overview.rfind('.')
            overview_size = overview[index + 1:]
            # print('overview_size', overview_size)
            result['overview_size'] = get_overview_size(overview)

            setup = self.get_setup()
            # print('setup', setup)
            result['setup'] = setup

            price_grid = self.tab.ele('@id=price-grid')
            trs = price_grid.eles('@tag()=tr')

            ths = trs[0].eles('@tag()=th')
            quantity = []
            for index, th in enumerate(ths):
                if index == 0:
                    continue
                # print(th.text)
                quantity.append(th.text)

            # print(trs[1].html)
            tds = trs[1].eles('@tag()=td')
            price = []
            for index, td in enumerate(tds):
                if index == 0:
                    continue
                # print(td.text)
                price.append(td.text)
            result['quantity'] = quantity
            result['price'] = price

            color = self.tab.ele('@id=colors-tab1').text
            # print('color', color)
            result['color'] = color

            themes = self.tab.ele('@id=themes').text
            # print('themes', themes)
            result['themes'] = themes

            imprint = self.tab.ele('@id=imprint').text
            # print('imprint', imprint)
            result['imprint'] = imprint

            delivery = self.tab.ele('@id=delivery').text
            # print('delivery', delivery)
            result['delivery'] = delivery

            time.sleep(1)
            thumbCarousel = self.tab.ele('@id=thumbCarousel')
            # print(thumbCarousel.html)
            img = thumbCarousel.ele('@tag()=img')
            data_lazy = img.attr('data-lazy')
            if data_lazy is None:
                data_lazy = img.attr('src')

            if data_lazy.startswith('http'):
                img = data_lazy
            else:
                img = f'https://{domain}' + data_lazy
            result['img'] = img
            return result
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False











