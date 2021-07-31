#!/usr/bin/env python
# coding: utf-8
# In[1]:
FINNISH_NUM2WORDS = {
    1: 'yksi',
    2: 'kaksi',
    3: 'kolme',
    4: 'neljä',
    5: 'viisi',
    6: 'kuusi',
    7: 'seitsemän',
    8: 'kahdeksan',
    9: 'yhdeksän',
    10: 'kymmenen'
}
# In[2]:
PLACE_WORDS = {
    0: {'plural': '', 'singular': ''},
    1: {'plural': 'tuhatta', 'singular': 'tuhat'},
    2: {'plural': 'miljoonaa', 'singular': 'miljoona'},
    3: {'plural': 'miljardia', 'singular': 'miljardi'},
    4: {'plural': 'biljoonaa', 'singular': 'biljoona'},
    5: {'plural': 'biljardia', 'singular': 'biljardi'},
    6: {'plural': 'triljoonaa', 'singular': 'triljoona'},
    7: {'plural': 'triljardia', 'singular': 'triljardi'},
    8: {'plural': 'kvadriljoonaa', 'singular': 'kvadriljoona'},
    9: {'plural': 'kvadriljardia', 'singular': 'kvadriljardi'},
    10: {'plural': 'kvintiljoonaa', 'singular': 'kvintiljoona'},
    11: {'plural': 'kvintiljardia', 'singular': 'kvintiljardi'},
    12: {'plural': 'sekstiljoonaa', 'singular': 'sekstiljoona'},
    13: {'plural': 'sekstiljardia', 'singular': 'sekstiljardi'},
    14: {'plural': 'septiljoonaa', 'singular': 'septiljoona'},
    15: {'plural': 'septiljardia', 'singular': 'septiljardi'},
    16: {'plural': 'oktiljoonaa', 'singular': 'oktiljoona'},
    17: {'plural': 'oktiljardia', 'singular': 'oktiljardi'},
    18: {'plural': 'noviljoonaa', 'singular': 'noviljoona'},
    19: {'plural': 'noviljardia', 'singular': 'noviljardi'},
    20: {'plural': 'dekiljoonaa', 'singular': 'dekiljoona'},
    21: {'plural': 'dekiljardia', 'singular': 'dekiljardi'},
    22: {'plural': 'undekiljoonaa', 'singular': 'undekiljoona'},
    23: {'plural': 'undekiljardia', 'singular': 'undekiljardi'},
    24: {'plural': 'duodekiljoonaa', 'singular': 'duodekiljoona'},
    25: {'plural': 'duodekiljardia', 'singular': 'duodekiljardi'},
    26: {'plural': 'tredekiljoonaa', 'singular': 'tredekiljoona'},
    27: {'plural': 'tredekiljardia', 'singular': 'tredekiljardi'},
    28: {'plural': 'kvattuordekiljoonaa', 'singular': 'kvattuordekiljoona'},
    29: {'plural': 'kvattuordekiljardia', 'singular': 'kvattuordekiljardi'},
    30: {'plural': 'kvindekiljoonaa', 'singular': 'kvindekiljoona'},
    31: {'plural': 'kvindekiljardia', 'singular': 'kvindekiljardi'},
    32: {'plural': 'sedekiljoonaa', 'singular': 'sedekiljoona'},
    33: {'plural': 'sedekiljardia', 'singular': 'sedekiljardi'},
    34: {'plural': 'septendekiljoonaa', 'singular': 'septendekiljoona'},
    35: {'plural': 'septendekiljardia', 'singular': 'septendekiljardi'},
    36: {'plural': 'duodevigintiljoonaa', 'singular': 'duodevigintiljoona'},
    37: {'plural': 'duodevigintiljardia', 'singular': 'duodevigintiljardi'}
}
# In[3]:
def tens(number):
    if number > 19:
        return f'{FINNISH_NUM2WORDS[number//10]}kymmentä'
    elif number > 10:
        return f'{FINNISH_NUM2WORDS[number-10]}toista'
    else:
        return f'{FINNISH_NUM2WORDS[number]}'
# In[4]:
def singles(number):
    if number != 0:
        return f'{FINNISH_NUM2WORDS[number]}'
    return ''
# In[5]:
def hundreds(number):
    if number > 1:
        return f'{FINNISH_NUM2WORDS[number]}sataa'
    else:
        return 'sata'
# In[6]:
def thousands(number):
    if number > 1:
        return f'{FINNISH_NUM2WORDS[number]}tuhatta'
    else:
        return 'tuhat'
# In[7]:
def build_string(digits, place):
    len_num = len(digits)
    num_string = ''
    is_between_10_and_19 = int(digits[-2:]) > 9 and int(digits[-2:]) < 20
    is_divisible_by_10 = int(digits) % 10 == 0
    is_place_gt_0_and_number_1 = int(digits) == 1 and place > 0
    if not is_between_10_and_19 and not is_divisible_by_10 and not is_place_gt_0_and_number_1:
        num_string = f'{singles(int(digits[-1]))}'
    
    if len_num >= 2 and int(digits[-2:]) > 9 and int(digits) % 100 != 0:
        num_string = f'{tens(int(digits[-2:]))}{num_string}'
        
    if len_num >= 3 and int(digits) > 99:
        num_string = f'{hundreds(int(digits[-3]))}{num_string}'
    
    if len_num >= 1 and int(digits) >= 1:
        type = 'singular' if int(digits) == 1 else 'plural' 
        num_string = f'{num_string}{PLACE_WORDS[place][type]}'
    return num_string
# In[8]:
def spell_number(num):
    str_num = str(num)
    len_num = len(str_num)
    
    offset = 1
    splits = (len_num // 3) + 1
    num_part = str_num[-3:len(str_num)]
    
    num_str = f''
    while num_part:
        num_str = f'{build_string(num_part, offset - 1)}{num_str}'
        splits -= 1
        offset += 1
        num_part = str_num[-3*offset:-3*(offset-1)]
    return num_str