from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import emoji
import string
import pandas as pd
import csv

browser = webdriver.Chrome()
url = "https://www.instagram.com"
username = 'roxxstarrr99'
password = 'lupabanget1234'



def login_instagram(url,username,password):
    #Masuk ke url
    browser.get(url)

    time.sleep(3)
    #Klik untuk login
    browser.find_element_by_xpath('/html/body/span/section/main/article/div[2]/div[2]/p/a').click()

    time.sleep(3)
    #Isi form dan login
    browser.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(username)
    browser.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(password)
    browser.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[4]/button').click()

    time.sleep(3)
    #Close pop-up
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()


def get_follower(username):
    time.sleep(3)
    #mendapatkan jumlah follower
    a = browser.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title').replace(',','')
    #klik follower
    followersLink = browser.find_element_by_css_selector('ul li a')
    followersLink.click()

    time.sleep(2)
    #klick follower list
    followersList = browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul')
    #mendapatkan panjang dari list yang di 
    numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
    followersList.click()

    time.sleep(2)
    browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul').click()#klik bar kosong akun pertama

    actionChain = webdriver.ActionChains(browser)

    itung = 0
    simpan = 0
    #scroll follower
    while (numberOfFollowersInList < int(a) and numberOfFollowersInList <= 2000): #mengatasi loading lama 
        time.sleep(1)
        if simpan == numberOfFollowersInList:
            itung += 1
            if itung > 4:
                break
        else:
            browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li[' + str(numberOfFollowersInList-2) + ']').click()
            itung = 0
        actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform() #scroll menggunakan space
        simpan = numberOfFollowersInList
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
        print(numberOfFollowersInList)
    # batas scraping follower = 500
    if numberOfFollowersInList > 500:
       numberOfFollowersInList = 501


    follow1 = []
    for i in range(1, numberOfFollowersInList):
        if int(a) > 12:
            follow1.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li['+str(i)+']/div/div[1]/div[2]/div[1]/a').get_attribute('title'))
        else:
            follow1.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li['+str(i)+']/div/div[2]/div[1]/div/div/a').get_attribute('title'))
    return follow1


translator = str.maketrans('', '', string.punctuation)
def give_emoji_free_text(text):
    allchars = [str for str in text.encode('ascii', 'ignore').decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.encode('ascii', 'ignore').decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text

def hashtag(text):
    char = text.encode('ascii', 'ignore').decode('utf-8').replace('\n',' ')
    tag = []
    teks = ''
    tulis = 0
    for i in range(len(char)):
        if tulis == 1:
            teks = teks + char[i]
        if char[i] == '#':
            tulis = 1
        elif (char[i] == ' ' or i == len(char)-1) and teks != '':
            teks = '#' + teks            
            tag.append(teks)
            tulis = 0
            teks = ''
    return tag

def get_post(index,username):
    
    try:
        browser.find_element_by_xpath('/html/body/span/section/main/div/div/article/div[1]/div/h2') #Nyari private
        return index
        
    except:
        time.sleep(2)
        #jumlah post orang tersebut
        jml_posts = browser.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[1]/span/span').text
        jml_posts.replace(',','')
        if int(jml_posts) == 0:
            return index
        #mengatasi html post pertama yang berbeda tiap akun
        tes = 0
        eror = 0
        benar = 1
        
        while benar == 1 and int(jml_posts) != 0:
            try:
                browser.find_element_by_xpath('/html/body/span/section/main/div/div['+str(tes)+']/article/div[1]/div/div[1]/div[1]').click()
                benar = 0
            except:
                tes += 1
                eror += 1
                if eror == 8:
                    break
                continue


        time.sleep(1)
        #mengambil post
        limit = 0
        while limit <= 100 and limit < int(jml_posts)-1 and int(jml_posts) != 0 and eror != 8:
            loop = False
            kiri = False
            kanan = False
            try:
                time.sleep(3)
                browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div/svg')
                if limit > 0:
                    browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a').click()
                    loop = True
                    kanan = True
                else:
                    browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a').click()
                    loop = True
                    kiri = True
        
            except:
                #mengambil teks
                try:
                    
                    if loop:
                        
                        if kanan:
                            browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a').click()
                            loop = False
                            kanan = False
                            time.sleep(2)
                            continue
                        
                        elif kiri:
                            browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a[2]').click()
                            loop = False
                            kiri = False
                            time.sleep(2)
                            continue
                        
                    teks = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span').text
                    tag = hashtag(teks) #ambil tag
                    if len(tag) == 0:
                        tag = ''
                    teks = give_emoji_free_text(teks) #hilangkan emoji
                    teks = teks.translate(translator).lower() #menjadikan teks huruf kecil
                except:
                    teks = ''
                    tag = ''
                #mengambil like
                try:
                    #like photo
                    try:
                        likes = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div/button/span').text
                    except:
                        likes = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div/button').text
                        likes = likes.replace('like','').replace('this','0')
                except:
                    #like video
                    likes = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/span/span').text
                ####print(teks, likes, tag)


                #mengambil komen
                try:
                    commentlist = len(browser.find_elements_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/div[1]/ul/ul')) #panjang dari banyak komen
                    comment = []
                    ####print(commentlist)
                    #mengambil komen 1/1
                    for i in range(1,commentlist+1):
                        isi_c = []
                        commentter = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/div[1]/ul/ul['+str(i)+']/div/li/div/div[1]/div[2]/h3/a').text #akun yang komen
                        teks_c = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/div[1]/ul/ul['+str(i)+']/div/li/div/div[1]/div[2]/span').text #isi komen
                        teks_c = give_emoji_free_text(teks_c)
                        teks_c = teks_c.translate(translator).lower()
                        isi_c.append(commentter)
                        isi_c.append(teks_c)
                        comment.append(isi_c)
                        ####print(commentter,teks)
                    if len(comment) == 0:
                        comment = ''
                except:
                    comment = ''        
                if index == 0:
                    with open('tes1.csv','a',newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['username','post','tag','likes','comment'])
                        writer.writerow([username, teks, tag, likes, comment])
                    index += 1
                else:
                    with open('tes1.csv', 'a', newline = '') as csvfile:
                        writer = csv.writer(csvfile)
                        ###print(username, teks, tag, likes, comment)
                        writer.writerow([username, teks, tag, likes, comment])
                    index += 1
                if limit == 0:
                    browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a').click()
                else:
                    browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a[2]').click()
                
                ###print()
                time.sleep(2)
                limit += 1
                continue
    return index
                
def jalankan():
    login_instagram(url,username,password)
    browser.find_element_by_xpath('/html/body/span/section/nav/div[2]/div/div/div[3]/div/div[3]/a/span').click()
    lis_follower = get_follower(username)
    print(lis_follower)
    index = 0
    for i in range (len(lis_follower)):
        #masuk akun orang
        try:
            browser.get(url+'/'+lis_follower[i])
            index = get_post(index, lis_follower[i])
        except:
            print("O")
            continue
    

jalankan()
browser.quit()
