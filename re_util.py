import re

def get_overview_size(overview):
    overview = overview[-30:]
    start_index = None
    for index, char in enumerate(overview):
        if char.isdigit():
            start_index = index
            break
    if start_index is None:
        return None
    return overview[start_index:]

def get_size(overview):
    print('overview', overview)

    #  4.72" L x 0.79" W
    pattern = r'\d{1}\.\d{2}.+d{1}\.\d{2}.+'
    pattern = r'\d+\.?\d*?"\s[a-zA-Z]\sx\s\d+\.?\d*?""?\s[a-zA-Z]'
    # pattern ='.+?x.+?'

    # 测试字符串
    # test_str = '这里有1.23，12.34和一些不符合规则的1.234     4.72" L x 0.79" W'

    # 查找所有匹配项
    matches = re.findall(pattern, overview)

    # print(matches)  # 输出匹配的浮点数字符串

    if len(matches) >= 1:
        print(matches)
        print('overview_size', matches[0])
        return matches[0]
    else:
        # pattern = r'\d?\s?\d+/?\d+?"\s[a-zA-Z]\sx\s\d?\s?\d+/?\d+?"\s[a-zA-Z]'
        pattern = r'\d*?\s?\d+/?\d*?"\s[a-zA-Z]\sx\s\d*?\s?\d+/?\d*?"\s[a-zA-Z]'
        matches = re.findall(pattern, overview)

        if len(matches) >= 1:
            print(matches)
            print('overview_size', matches[0])
            return matches[0]

# overview = "Laser engraved. 1\" W x 5/16\" H. Price includes 1 color, 1 side, 1 location"
# get_size(overview)

def get_position(imprint):
    print('imprint', imprint)
    pattern = r'on\s[a-zA-Z]+.'
    matches = re.findall(pattern, imprint)
    print(matches)

    if len(matches) >= 1:
        match = matches[0]
        position = match.replace('on ', '').replace('.', '')
        print('position', position)
        return position

def get_cm(imprint):
    print('imprint', imprint)
    pattern = r'includes\s.+'
    matches = re.findall(pattern, imprint)
    print(matches)

    if len(matches) >= 1:
        match = matches[0]
        position = match.replace('includes ', '')
        print('position', position)
        return position


imprint = 'Full color heat transfer. 4.72" L x 0.79" W on front. Price includes Full color, 1 side, 1 location'
get_cm(imprint)
