from logging import exception
from selenium import webdriver as wd
from selenium import webdriver
from time import sleep
import os
import json

path_ = os.path.dirname(str(os.path.realpath(__file__)))
options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')


target_url = 'https://community.rememberapp.co.kr/community/61'
driver = wd.Chrome(executable_path=f"{path_}/driver/chromedriver",options=options)
driver.get(target_url)
#main_url_list = driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div/div[1]/div')
#main_url_list.find_element_by_tag_name('a').get_attribute('href')
#best_W = driver.find_element_by_class_name("sc-1geooqf-0.jhmgoF").find_element_by_tag_name('a')
best_W = driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div/div[2]/div[3]').find_elements_by_tag_name('a')
best_W_url = []

for i in best_W:
    best_W_url.append(i.get_attribute('href'))
    
A = {}

for j,t in  enumerate(best_W_url):    
    comment_list = []
    driver.get(t)
    title_name = driver.find_element_by_class_name("sc-14ghfp4-3.cBzLtS").text
    main_like = driver.find_element_by_class_name("w0px7c-4.beOEEB").text
    text_data = driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div/main/div[1]/article/div[1]').text
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    sleep(3)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight-3000);")
    sleep(2)
    nbr=2
    while True:
   
        comment = driver.find_element_by_xpath(f'//*[@id="__next"]/div[3]/div/main/div[1]/div/div[{nbr}]')
        print(nbr)
        print(len(driver.find_elements_by_xpath(f'//*[@id="__next"]/div[3]/div/main/div[1]/div')))
        print("----------------------------------")
        maincomment =  comment.find_element_by_class_name('sc-1k9y380-1')
        comment_text = maincomment.find_element_by_class_name("sc-1k9y380-9.hyNvVF").text
        comment_name = maincomment.find_element_by_class_name("sc-1k9y380-7.dzjIfr").text
        comment_job = maincomment.find_element_by_class_name("sc-1k9y380-8.jyiHSA").text
        like = maincomment.find_element_by_class_name('sc-1k9y380-14.iyjckW').text
        nested_reply = comment.find_elements_by_class_name("sc-1k9y380-1.jRlCJe")
        print(nested_reply)
        print(len(nested_reply))
        if nested_reply:
            nested_reply_ = []
            print("=================================================")
            for i in nested_reply:
                #nested = i.find_element_by_class_name('sc-1k9y380-1.jRlCJe')
                nested_reply_name = i.find_element_by_class_name("sc-1k9y380-7.dzjIfr").text
                nested_reply_job = i.find_element_by_class_name("sc-1k9y380-8.jyiHSA").text
                nested_reply_text = i.find_element_by_class_name('sc-1k9y380-9.hyNvVF').text
                nested_reply_.append({"nsd_re_name":nested_reply_name,"nsd_re_job":nested_reply_job,"nsd_re_text":nested_reply_text })

            comment_list.append({"name":comment_name,"job":comment_job,"like":like,"text":comment_text,"nested_reply":nested_reply_})
            nbr+=1
        else:
            nested_reply_ = [None]
            comment_list.append({"name":comment_name,"job":comment_job,"like":like,"text":comment_text,"nested_reply":nested_reply_})
            nbr+=1
        if nbr is 15:
            break
    A[f'{j}'] = [{"title":title_name,"text_data":text_data,"like":main_like,"comment":comment_list}]
print(A)
with open(f'{path_}/test.json', 'w',encoding='utf-8') as f:
    f.write(json.dumps(A,ensure_ascii = False,indent=4))

driver.close()