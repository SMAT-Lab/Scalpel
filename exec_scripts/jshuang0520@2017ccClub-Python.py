#!/usr/bin/env python
# coding: utf-8
# In[1]:
def star_array(input_value) :
    a = "*"    
    ai = -1  # ai for number of stars 
    i = 0    # i for number of blanks
    for i in range(0, (input_value) ) : 
        i = i + 1
        ai = ai + 2
        #print("ai = %i , i = %i " % (ai, i) )  # ai for number of stars , i for number of blanks
    
    
    print("\n")
    aj = -1
    j = i
    #print(i)
    for i in range(0, (input_value) ) :     
        aj = aj + 2
        j = j - 1
        #print("aj = %i" % (aj) ) 
        #print("\n")
        print(" "*(j), a * (aj))       
    return("")
print(star_array(7))
# In[30]:
def month_difference(x, y) :
    '''
    輸入兩個字串，分別是 "年月" 的形式， 保證第二個字串發生的時間較晚，且字串長度皆為6，輸出相差幾個月份
    '''
    try :
        year_x = int(x[0 : 4]) # python 取到 end - 1 ， 且因為輸入是文字，欲計算須轉成數字，使用 int()
        year_y = int(y[0 : 4])
        
        month_x = int(x[4: ])
        month_y = int(y[4: ])
        
        return("您所輸入的 %s 和 %s 月分差為 : %i 個月" % (x, y, ((year_y - year_x)*12 + (month_y) - (month_x)) ) )
        
    except :
        return('輸入格式錯誤 : 輸入兩個格式為 "oooooo"(分別代表年、月)的字串，且保證第二個字串發生的時間較晚、字串長度皆為6 \n  ->  例 : month_difference("201601", "201710") \n')
print(month_difference(201601, 201710))    
print(month_difference("201601", "201710"))
# In[3]:
def count_vowel(input_string) :
    
    '''    
    輸入一個字串，輸出有幾種母音(大小寫是為同一種，最大值為5)
    '''
    # 先全部轉換成小寫，以避免大小寫的困擾
    tolower_input_string = str.lower(input_string)
    
        
    # 把字串分開
    str.split(input_string)
 
    
    # 收集出現過的母音
    vowel_list_of_your_input = []
    for i in range(0,len(input_string)) :
        if (tolower_input_string[i] == "a" or tolower_input_string[i] == "e" or tolower_input_string[i] == "i" or tolower_input_string[i] == "o" or tolower_input_string[i] == "u") :
            # 成員
            vowel_list_of_your_input.append(tolower_input_string[i])            
        else :
            None
    summation = 0
    vowel_list = ["a", "e", "i", "o", "u"]
    for i in range(0, len(vowel_list)) :
        if vowel_list[i] in tolower_input_string :
            summation = summation + 1 
        
    return ("您的輸入 %s 所出現過的母音 : %s ， 共有 %i 種不同的母音" % (input_string, vowel_list_of_your_input, summation))
    
print(count_vowel("HI, Apple Pen"))
# In[4]:
def count_alphabet(input_string) :
    
    '''    
    輸入一個字串，輸出一共出現過幾種英文字母(大小寫是為同一種，最大值為26)
    '''
    # 先全部轉換成小寫
    tolower_input_string = str.lower(input_string)
    # 計算共有幾個不同的英文字母
    summation = 0
    alphabet_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    for i in range(0, len(alphabet_list)) :
        if alphabet_list[i] in tolower_input_string :
            summation = summation + 1 
        
    return ("您的輸入是 : %s ， 共有 %i 種不同的英文字母" % (input_string, summation))
    
print(count_alphabet("Hello world !"))
print(count_alphabet("Hello, my name is Johnson Huang !"))
print(count_alphabet("Curry drives, Curry fakes, Curry steps back...... Oh! He puts it in!!!"))
# In[5]:
def your_input_palindrome(input_string) :
    
    '''    
    輸入一個字串，回傳是不是回文
    '''
    for i in range(0, len(input_string)) :
        
        # 回文的頭尾元素要對稱、要一樣
        if input_string[i] == input_string[-i-1] :
            return ("您所輸入的 %s : Yes ! 這是回文" % input_string)
        else :
            return ("您所輸入的 %s : Nooo! 這不是回文" % input_string)
    
print(your_input_palindrome("a"))
print(your_input_palindrome("aabbaa"))
print(your_input_palindrome("app"))
print(your_input_palindrome("早安安早"))
# In[24]:
def sum_your_input(input_string) :
    
    '''    
    輸入一個字串，輸出裡面含有數字部分的總和
    '''
    # 正規表達式
    # 看來可以趁機找了解一下python正規表達式子的使用方法
    
    summation = 0
    number_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    
    for i in range(0, len(input_string)) :
        if input_string[i] in number_list :
            # 因為 number_list 裡面元素都是文字，我要轉換成數字接下來才能運算相加 : 使用 int()
            summation = summation + int(input_string[i])
        
    return ("您所輸入的數字部分，總合是 : %i ，您的輸入為 \"%s\"" % (summation, input_string) )
    
print(sum_your_input("Here's my email : s9140911@yahoo.com.tw"))
print(sum_your_input("This is ccClub2017!"))
print(sum_your_input("我並沒有輸入數字"))