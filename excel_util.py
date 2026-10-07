import traceback

from openpyxl import load_workbook
from chrome import Chrome
from re_util import get_size, get_position, get_cm
from config_util import read_column_index

class ExcelUtil:
    def __init__(self):
        print('init excel util')
        self.chrome = Chrome()

    def read_excel(self):
        # 加载工作簿
        wb = load_workbook('input.xlsx')

        # 获取工作表
        sheet = wb.worksheets[0]  # 通过索引

        # 遍历所有行
        print('从第4行开始处理')
        for row in sheet.iter_rows(min_row=4):  # 从第2行开始，只获取值
            try:
                row_number = str(row[0].row)
                print('行号', row_number)

                number = row[0].value
                print('产品编号', number)
                result = self.chrome.handle(number)
                print(result)

                if not result:
                    continue

                # 操作的索引
                column_index = read_column_index()
                print('column_index', column_index)

                sheet[column_index['title'] + row_number] = result['title']

                overview = result['overview']
                overview_size = result['overview_size']
                print('overview_size', overview_size)
                index = overview.find('.')
                overview_first_sentence = overview[0:index + 1]

                if overview_size is not None:
                    overview = overview.replace(overview_size, '')

                sheet[column_index['overview'] + row_number] = overview
                sheet[column_index['overview_first_sentence'] + row_number] = overview_first_sentence

                sheet[column_index['img'] + row_number] = result['img']

                sheet[column_index['color'] + row_number] = result['color']
                sheet[column_index['overview_size'] + row_number] = result['overview_size']
                sheet[column_index['themes'] + row_number] = result['themes']

                imprint = result['imprint']
                imprint_items = imprint.split('.')
                imprint_first = imprint_items[0]

                start_index = imprint_first.find(',')
                end_index = imprint_first.find('.')
                imprint_type = imprint_first[0:start_index]
                imprint_type = imprint_first.split(',')[0]
                print('imprint_type', imprint_type)

                imprint_color = imprint_first[start_index + 1:end_index]
                print('imprint_color', imprint_color)

                sheet[column_index['imprint_type'] + row_number] = imprint_type
                # sheet['AE' + row_number] = imprint_color

                imprint_second = imprint_items[1]
                on_index = imprint_second.find('on')
                # imprint_size = imprint_second[0:on_index]
                imprint_size = get_size(imprint)
                imprint_position = get_position(imprint)
                print('imprint_size', imprint_size)
                print('imprint_position', imprint_position)
                sheet[column_index['imprint_size'] + row_number] = imprint_size
                sheet[column_index['imprint_position'] + row_number] = imprint_position

                # imprint_third = imprint_items[2]
                cm = get_cm(imprint)
                print('cm', cm)
                sheet[column_index['cm'] + row_number] = cm

                delivery = result['delivery']
                print('delivery', delivery)

                delivery_items = delivery.split('\n')
                delivery_first = delivery_items[0]
                delivery_first = delivery_first.split(':')[1]
                delivery_index = delivery_first.find('working days')
                delivery_working_days = delivery_first[0:delivery_index]
                print('delivery_working_days', delivery_working_days)
                sheet[column_index['delivery_working_days'] + row_number] = delivery_working_days

                delivery_second = delivery_items[1]
                delivery_second_items = delivery_second.split(';')

                packaging_material = delivery_second_items[0].split(':')[1]
                print('packaging_material', packaging_material)
                sheet[column_index['packaging_material'] + row_number] = packaging_material

                if len(delivery_second_items) >= 2:
                    packaging_way = delivery_second_items[1]
                    print('packaging_way', packaging_way)
                    sheet[column_index['packaging_way'] + row_number] = packaging_way

                if len(delivery_second_items) >= 3:
                    packaging_weight = delivery_second_items[2]
                    print('packaging_weight', packaging_weight)
                    sheet[column_index['packaging_weight'] + row_number] = packaging_weight

                if len(delivery_second_items) >= 4:
                    packaging_size = delivery_second_items[3].split(':')[1]
                    print('packaging_size', packaging_size)
                    sheet[column_index['packaging_size'] + row_number] = packaging_size

                sheet[column_index['title2'] + row_number] = result['title']

                quantity_start_column_index = column_index['quantity_start']
                if len(quantity_start_column_index) == 1:
                    start = ''
                    quantity_index = quantity_start_column_index
                else:
                    quantity_index = quantity_start_column_index[0]
                    start = quantity_start_column_index[1]
                print(quantity_index, start) # 是不是BH

                quantity = result['quantity']
                # start = 'H'
                print('quantity', quantity)
                for quantity_item in quantity:
                    # print('quantity_item', quantity_item)
                    sheet[quantity_index + start +  row_number] = quantity_item.replace(',', '')
                    if start != '':
                        start = chr(ord(start) + 1)
                    # print('start', start)

                price_start_column_index = column_index['price_start']
                if len(price_start_column_index) == 1:
                    start = ''
                    price_index = price_start_column_index
                else:
                    price_index = price_start_column_index[0]
                    start = price_start_column_index[1]
                print(price_index, start)  # 是不是BH

                price = result['price']
                print('price', price)
                # start = 'R'
                for price_item in price:
                    price_item = price_item.replace('$', '')
                    # print('price_item', price_item)
                    sheet[price_index + start + row_number] = price_item

                    if start != '':
                        start = chr(ord(start) + 1)
                    # print('start', start)

                # 保存到excel
                wb.save('output.xlsx')
                print('保存到数据表')
            except Exception as e:
                print(e)
                traceback.print_exc()
                continue

        print('处理完成，保存到当前目录output.xlsx')










