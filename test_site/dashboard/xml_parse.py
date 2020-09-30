from lxml import etree
import math
import pandas as pd

# with open('../../Documents/9037-8601A.xml', 'r', encoding='utf-8') as f:
#     setting = f.read()

# test = etree.fromstring(setting)




def find_element_value(tree, name):
    temp = tree.findall('Group[@Name=\'Group 1\']')[0].xpath(f'Setting/Setting[text()="{name}"   ]')
    if not temp:
        return None
    temp2 = temp[0].getparent().find('Value').text 
    return temp2
def safe_float(number):
    try:
        temp = float(number)
    except ValueError:
        return None
    return temp

def setting_check(file):
    

    tree = etree.fromstring(file)
    y = tree.findall('Group[@Name=\'Group 1\']')[0].getchildren()
    list_setting = [[i.find('Setting').text , i.find('Description').text ,i.find('Value').text, ''] for i in y ]

    setting= {}
    setting['CTRW'] = safe_float( find_element_value(tree,'CTRW'))
    setting['PTRZ'] = safe_float( find_element_value(tree,'PTRZ'))
    setting['XP1'] = safe_float( find_element_value(tree,'XP1'))
    setting['XP2'] = safe_float( find_element_value(tree,'XP2'))
    setting['XP3'] = safe_float( find_element_value(tree,'XP3'))
    setting['RP1'] = safe_float( find_element_value(tree,'RP1'))
    setting['RP2'] = safe_float( find_element_value(tree,'RP2'))
    setting['RP3'] = safe_float( find_element_value(tree,'RP3'))
    setting['Z1MAG'] = safe_float( find_element_value(tree,'Z1MAG'))
    setting['Z1ANG'] = safe_float(find_element_value(tree,'Z1ANG'))
    setting['factor'] = safe_float(setting['PTRZ']) / safe_float(setting['CTRW'])
    zline = safe_float(setting['Z1MAG'])* setting['factor']
    x1l = zline * math.sin( setting['Z1ANG'] * (math.pi / 180)) * setting['factor']
    r1l = zline * math.cos( setting['Z1ANG'] * (math.pi / 180)) * setting['factor']
    z1 = math.sqrt((setting['XP1'] ** 2 + ((setting['XP1'] / x1l) *  r1l) ** 2)) * setting['factor']
    z2 = math.sqrt((setting['XP2'] ** 2 + ((setting['XP2'] / x1l) *  r1l) ** 2)) * setting['factor']
    z3 = math.sqrt((setting['XP3'] ** 2 + ((setting['XP3'] / x1l) *  r1l) ** 2)) * setting['factor']

    setting_frame = pd.DataFrame(list_setting, columns=['Name','Description','Value','Flags'])
    checked_field = [i for i in setting]
    setting_frame.loc[setting_frame['Name'].isin(checked_field), 'Flags'] = 'OK'
    if z1 > 0.9 * zline or z1 < 0.4 * zline:
                setting_frame.loc[setting_frame['Name'].isin(['XP1','RP1']), 'Flags'] = 'Require Review'

    setting_frame.sort_values(by=['Flags'], ascending=False, inplace=True)
    respone = setting_frame.to_json(index=False, orient='table')
    return respone