#!/usr/bin/python
# -*- coding: utf-8

if 1==1: # ОГЛАВЛЕНИЕ ПРОГРАММЫ
    ver = '2.3'
    import colorama
    colorama.init(autoreset=True)
    print(colorama.Fore.GREEN  + '[+] Работаем c API VK (Все программы)',colorama.Fore.YELLOW + '[+] Версия:',ver)
    #// цвет текста
    #Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    #// цвет фона
    #Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    #// яркость текста и общий сброс
    #Style: DIM, NORMAL, BRIGHT, RESET_ALL
    #from colorama import init
    pass

if 1==1: # ИСТОРИЯ 
    ### --------------------------------------------------------------------------
    # 1. Читаю новости у группы и проставляю нравится
    grup_like = -90064209  ## Моя группа телеграмм бота
    grup_like = 24709387   ## Моя группа в контаете
    grup_like = -209085681 ## 1С Предприятие API VK
    # 2. Проставляем данные пользователя. У наших аккаунтов
    # 3. Обновляем названия группам
    # 4. Читаю группы у клиента
    # 5. Собираю пользователей из группы
    # 6. Собираю группы у пользователей
    # 7. Собираю друзей у пользователей
    # 8. Программа поздравления с днем рождения
    #dt_b = '13.12.%'
    step = ['','    ','        ','            ',]
    ### --------------------------------------------------------------------------
    pass
  
if 1==1: # НАСТРОЙКИ
    ### --------------------------------------------------------------------------
    import iz_vk
    import configparser
    config          = configparser.ConfigParser()
    config.read('settings.ini') 
    grup_like     = config.get('Settings', "grup_like")
    bithday       = config.get('Settings', "bithday")

def connect ():
    import pymysql
    db = pymysql.connect(host='localhost',
                            user='izofen',
                            password='Podkjf3141!',
                            database='site_rus',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor() 
    return db,cursor

def change (word):
    word = word.replace("'","<1>")
    word = word.replace('"',"<2>")
    word = word.replace('/',"<3>")
    word = word.replace('\\',"<4>")
    word = word.replace(')',"<5>")
    word = word.replace('(',"<6>")
    return (word)

def get_token_list ():
    import iz_func
    db1,cursor1 = iz_func.connect ()
    sql = "select id,token from vk_accound where 1=1".format()    
    cursor1.execute(sql)
    data = cursor1.fetchall()
    list = []
    for rec in data:     
       id,token = rec.values()
       list.append([id,token])  
    return list       

def iz_pause (wait):
    import time
    for number in range(wait):
        st_print = '[+] Ожидаем '+str(wait-number)+' сек.'
        dl_str = len (st_print)
        add_st = 30 - dl_str 
        for number in range(add_st):
            st_print = st_print + ' '
        print (st_print, end='')    
        ls = ''
        for k in range(30):
            ls = ls + '\b'
        print (ls, end='')
        time.sleep (1)

def get_data_user (user_id,token):
    import requests
    url = 'https://api.vk.com/method/users.get?access_token='+str(token)+'&user_ids='+str(user_id)+'&fields=about,bdate,can_post,can_send_friend_request,can_see_all_posts,online,last_seen,relation&v=5.131'
    response        = requests.get(url)
    parsed_string   = response.json()
    response        = parsed_string['response']       
    for line in response:
        last_seen = ''
        try:
            last_seen       = line['last_seen']
        except Exception as e:
            pass    
        platform = ''
        try:   
            platform        = last_seen['platform']
        except Exception as e:
            pass   
        time_w = 0
        try:
            time_w          = last_seen['time']
        except Exception as e:
            pass
        if platform == 1:
            platform = 'мобильная версия'
        if platform == 2: 
            platform = 'приложение для iPhone'
        if platform == 3:
            platform = 'приложение для iPad'
        if platform == 4:
            platform = 'приложение для Android'
        if platform == 5:
            platform = 'приложение для Windows Phone'
        if platform == 6:
            platform = 'приложение для Windows 10'
        if platform == 7:
            platform = 'полная версия сайта'

    return last_seen,platform,time_w,platform
   
def get_fearend (user_id,token,unixtime,time_w):
    ps = (int((unixtime - time_w)/60))/60
    url = get_command ('friends.areFriends',{'token':token,'user_id':user_id})
    parsed_string   = request_vk (url)
    #response        = requests.get(url)
    #parsed_string   = response.json()
    response        = parsed_string['response']
    friend_status = ''
    for line in response:
        friend_status = line['friend_status']
    return friend_status,ps

def save_capcha (namebot,user_id,url,captcha_img):
    import requests   
    captcha_img = captcha_img.replace ('/','**1**')
    captcha_img = captcha_img.replace ('&','**2**')
    captcha_img = captcha_img.replace ('?','**3**')
    url = 'http://3dot14.ru:5000/save_capcha/1111/'+str(captcha_img)+'/'
    response        = requests.get(url)
    lastid          = str(response.text)
    import iz_telegram
    iz_telegram.save_variable (user_id,namebot,"id capcha",str(lastid))
    #id_save   = iz_telegram.load_variable (user_id,namebot,'id capcha')
    #import iz_func
    #db,cursor = iz_func.connect ()
    #sql = "INSERT INTO vk_capcha (namebot,unixtime,url,capcha,status) VALUES ('{}',{},'{}','','')".format (namebot,0,url)
    #cursor.execute(sql)
    #db.commit()
    #lastid = cursor.lastrowid
    #message_out,menu = iz_telegram.get_message (user_id,'Проверка капчи',namebot)
    #message_out = message_out.replace('%%captcha_img%%',str(captcha_img))   
    #markup = ''
    #print ('[+] Отправка капчи:',message_out)
    #answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
    #iz_telegram.save_variable (user_id,namebot,"status",'Ввод капчи')
    return lastid
      
def error_code_test (parsed_string,url,token,text):
    import iz_func
    import iz_telegram
    import requests
    import time   
    answer      = parsed_string 
    captcha_sid = ''    
    error_code  = 0
    error_msg   = ''
    try:
        error       = parsed_string['error']
        error_code  = error['error_code']
        error_msg   = error['error_msg']
        captcha_sid = error['captcha_sid']
        captcha_img = error['captcha_img']
        print ('[captcha_img]',captcha_img)
        print ('[captcha_sid]',captcha_sid)
    except Exception as e:
        pass
        
        
    if error_msg.find ("User is deactivated") != -1:
        answer = ''
        iz_pause (10)
        return answer    
    
        
    if error_msg == 'User authorization failed: user is blocked.': 
        print ('[token]',token)
        answer = ''
        iz_pause (600)
        return answer    
        
    if error_msg == 'User authorization failed: invalid session.':
        answer = ''
        return answer   


    if error_msg == 'Access denied: no access to this group':
        answer = ''
        return answer   
    


    
            
    while captcha_sid != '':
        namebot = '@ask_314_bot'
        user_id = '399838806'
        lastid = save_capcha (namebot,user_id,url,captcha_img)                          
        response = ''
        time.sleep (30)
        while response == "":
            db2,cursor2 = iz_func.connect ()                        
            sql = "select id,capcha from vk_capcha where id = "+str(lastid)+";"   ### 
            cursor2.execute(sql)
            data2 = cursor2.fetchall()
            k = 0
            for row2 in data2:
                k = k + 1
                id,capcha = row2.values()
                print ('[+] id,capcha',id,capcha)
                response = capcha
                if response == '':
                    if k > 5:
                        k = 0
                        lastid = save_capcha (namebot,user_id,url,captcha_img) 
                    iz_pause (300)                    
                else:  
                    url = 'https://api.vk.com/method/friends.add?access_token='+str(token)+'&user_id='+str(id)+'&text='+str(text)+'&follow=0&v=5.131&captcha_sid='+str(captcha_sid)+'&captcha_key='+str(response)
                    response        = requests.get(url)
                    parsed_string   = response.json()
                    #print ('[+] parsed_string:',parsed_string)
                    captcha_sid = ''
                    try:
                        error       = parsed_string['error']
                        error_code  = error['error_code']
                        error_msg   = error['error_msg']
                        captcha_sid = error['captcha_sid']
                        captcha_img = error['captcha_img']
                        print ('[captcha_img]',captcha_img)
                        print ('[captcha_sid]',captcha_sid)
                    except Exception as e:
                        captcha_sid = ''
    return answer

def request_vk (url):
    import requests
    response        = requests.get(url)
    parsed_string   = response.json()
    return parsed_string

def get_command (command,data):
    try: 
        token   = data ['token']
    except Exception as e:
        token = ''
    try:    
        user_id = data ['user_id']
    except Exception as e:        
        user_id = ''     
    try:    
        text = data ['text']
    except Exception as e:        
        text = ''
   
    v = '&v=5.131'
    
    if command == 'utils.get':
        url = 'https://api.vk.com/'    
        url = url + 'method/utils.getServerTime'
        url = url + '?access_token=%%token%%'
        url = url + '&v=%%v%%'
        
    if command == 'friends.areFriends':    
        url = 'https://api.vk.com/'        
        url = url + 'method/friends.areFriends'
        url = url + '?access_token=%%token%%'
        url = url + '&user_ids=%%user_id%%'
        url = url + '&need_sign=0'
        url = url + '&extended=0'
        url = url + '&v=%%v%%'
       
    if command == 'friends.add':   
        url = 'https://api.vk.com/'
        url = url + 'method/friends.add'
        url = url + '?access_token=%%token%%'
        url = url + '&user_id=%%user_id%%'
        url = url + '&text=%%text%%'
        url = url + '&follow=0'
        url = url + '&v=%%v%%'
                                 
    url = url.replace ("%%token%%",str(token))   
    url = url.replace ("%%text%%",str(text))
    url = url.replace ("%%user_id%%",str(user_id))
    url = url.replace ("%%v%%",str(v))
    
    return url 

def start_bithday (dt_b,token):
    import colorama
    import requests
    import random
    import pymysql
    import time
    import iz_func
    import iz_telegram
    from grab import Grab
    colorama.init(autoreset=True)
    print(step[1],colorama.Fore.GREEN  + '[+] Программа поздравления с днем рождения')    
    print(step[2],colorama.Fore.YELLOW + '[+] Выбранная дата:',dt_b)  
    db = pymysql.connect(host='localhost',
                        user='izofen',
                        password='Podkjf3141!',
                        database='site_rus',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor() 
    
    namebot     = '@ask_314_bot'
    user_id_bot = '399838806'
    
    print(step[2],colorama.Fore.MAGENTA + '[+] Поиск необходимых данных.')
    ## Сайты которые нам не нужны.
    list_key = []
    sql = "select id,name from vk_key where 1=1;"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,name = rec.values() 
        list_key.append(name)
        
    url = get_command ('utils.get',{'token':token})
    
    #response        = requests.get(url)
    #parsed_string   = response.json()
    parsed_string    = request_vk (url)
    
    unixtime        = parsed_string['response']
    list_site = []
    
    sql = "select id,first_name,last_name,site,bdate from vk_user where site  <> '' and bdate like '"+str(dt_b)+"' ;"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,first_name,last_name,site,bdate = rec.values() 
        list_site.append([id,first_name,last_name,site,bdate]) 
    random.shuffle(list_site)
    for site_line in list_site:
        label = False
        id,first_name,last_name,site,bdate = site_line      
        if site.find ('.ru') != -1:
            label = False
        else:    
            label = True
        if label == False:
            for key in list_key:
                if site.find (key) != -1:
                    label = True                
        if label == False:
            last_seen,platform,time_w,platform = get_data_user (id,token)
            if 1==1:
                friend_status,ps = get_fearend (id,token,unixtime,time_w)
                code  = 0
                body  = ''
                title = ''
                g = Grab()
                try:
                    g.go(site)
                    title = g.doc.select('//title').text()
                    code = g.doc.code
                    body = g.doc.body
                    title = title.strip()
                    if title == '':
                        title = "нет титле"            
                except Exception as e:
                    pass

                print ('[+] Пользователь: {:5} {:10} {:10}'.format (id,first_name,last_name))
                print ('[+] ДР:',bdate)
                print ('    [+] Сайт : ',site)
                print ('    [+] Title: ',title)
                print ('    [+] Code : ',code)
                print ('        [+] Время на сайте: ',str(ps),'час.')
                print ('        [+] Инструмент:     ',platform)
                print ('        [+] friend_status    :     ',friend_status)
                text = 'Поздравляю тебя с Днем рождения! Желаю удачи и счастья.'
                if ps <= 48 and friend_status == 0 and code != 0:
                    captcha_sid = ''
                    if 1==1:                     
                        #url = 'https://api.vk.com/method/friends.add?access_token='+str(token)+'&user_id='+str(id)+'&text='+str(text)+'&follow=0&v=5.131'
                        url = get_command ('friends.add',{'token':token,'user_id':id,'text':text})
                        #response        = requests.get(url)
                        #parsed_string   = response.json()
                        parsed_string   = request_vk (url)
                        print ('[+] Приглашение дружбы:',parsed_string)     
                        answer = error_code_test (parsed_string,url,token,text)                 
                    message_out,menu = iz_telegram.get_message (user_id_bot,'Отправлено сообщение пользователю',namebot)
                    message_out = message_out.replace('%%Сайт%%',str(site))   
                    message_out = message_out.replace('%%Title%%',str(title))
                    markup = ''
                    answer = iz_telegram.bot_send (user_id_bot,namebot,message_out,markup,0)                
                    iz_pause (10*60) 
                else:  
                    if ps > 48:
                        print (colorama.Fore.YELLOW  + '    [+] Пропускаем из за неактивности пользователя') 
                    if friend_status != 0: 
                        print (colorama.Fore.YELLOW  + '    [+] Пропускаем так как заявка уже отправлена')
                    if code == 0:
                        print (colorama.Fore.YELLOW  + '    [+] Сайт пользователя не активный')
                    iz_pause (10)
    print ('[+] Внимание !!! Высылаем остальных клиентов')
    sql = "select id,first_name,last_name,site,bdate from vk_user where bdate like '"+str(dt_b)+"' ;"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,first_name,last_name,site,bdate = rec.values() 
        list_site.append([id,first_name,last_name,site,bdate]) 
    random.shuffle(list_site)
    for site_line in list_site:
        label = False
        id,first_name,last_name,site,bdate = site_line      
        print ('[+]',id,first_name,last_name,site,bdate)

def parser_user (line):
    first_name          = line['first_name']
    id_user             = line['id']
    last_name           = line['last_name']
    can_access_closed = ''
    if 1==1:
        if 1==1:
            if 1==1:
                try:
                    can_access_closed   = line['can_access_closed']
                except Exception as e:
                    can_access_closed = ''                 
                is_closed = ''
                try:    
                    is_closed           = line['is_closed']
                except Exception as e:
                    is_closed = ''              
                sex                 = line['sex']               
                bdate = ''
                try: 
                    bdate               = line['bdate']
                except Exception as e:
                    bdate = ''                   
                city = ''
                city_id = 0
                city_title = ''
                try:
                    city                = line['city']
                    city_id             = city['id']
                    city_title          = city['title']
                except Exception as e:
                    city = ''       
                country = ''
                country_id = 0
                country_title = ""
                try:
                    country             = line['country']
                    country_id          = country['id']
                    country_title       = country['title']
                except Exception as e:
                    country = ''    
                try: 
                    status              = line['status'] 
                except Exception as e:
                    status = ''  
                site = ''
                try:
                    site                = line['site'] 
                except Exception as e:
                    site = ''                
                if site != '':      
                    #print ('        [+]',id,first_name,last_name,site)
                    pass        
    return id_user,first_name,last_name,can_access_closed,is_closed,bdate,country_id,country_title,city_id,city_title,status,site,sex

def get_token (status):
    import iz_func
    import random
    db,cursor = iz_func.connect ()
    sql = "select id,name,token,user_id from vk_accound where status = '"+str(status[0])+"';"
    #print ('[+] sql:',sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    list = []    
    for rec in data: 
        id,name,token,user_id = rec.values()
        list.append ([id,name,token,user_id])        
    random.shuffle(list)    
    token = list[0]
    return token 

if 1==1:
    import optparse
    parser =  optparse.OptionParser(version='1.0',description='Шаблон')
    parser.add_option('-m','--menu', type='string', dest='menu', help='Меню')
    parser.add_option('-c','--city', type='string', dest='city', help='Меню')
    (options, args) = parser.parse_args()
    ### --------------------------------------------------------------------------
    if options.menu == None:
        from consolemenu import *
        from consolemenu.items import *
        menu = ConsoleMenu("API ВКонтакте", "Список программ для работы с сервером ВКонтакте")   
        menu_item01    	= MenuItem("Запуск программы приглашения в друзья")
        function_item = FunctionItem("Call a Python function", start_bithday, [dt_b])
        #function_item01 = FunctionItem("Call a Python function",start_bithday (dt_b))
        #menu.append_item(function_item01)
        menu.append_item(menu_item01)
        menu.append_item(function_item)
        menu.show()

##################################################################### ПОЛУЧАЕМ СПИСОК ID ПО НАЗВАНИЮ ##############################################################
def parser_get_list_user (users,list_info):  #### Получение списка пользователей по никам
    list = []
    list_user = users.split(',')
    token = get_token (["like"])
    url = ''    
    url = url + 'https://api.vk.com/method/users.get'
    url = url + '?access_token='+str(token[2])
    url = url + '&user_ids='+str(data['user_id'])
    answer = ''
    print ('[+] list_info',list_info)  
    if list_info != '':    
        url = url + '&fields='+list_info
    url = url + '&v=5.131'
    print ('[url]',url)
    answer          = requests.get(url)
    parsed_string   = answer.json()    
    print (parsed_string)    
    response  = parsed_string['response']
    for line in response:
        list.append(line) 
    return list   
       
def parser_get_list_group (list_group):  #### Получение списка групп по никам
    list = []
    token = get_token (["like"])
    url = ''    
    url = url + 'https://api.vk.com/method/groups.getById'    ###api.vk.com/method/groups.getById
    url = url + '?access_token='+str(token[2])
    url = url + '&group_ids='+str(list_group)
    url = url + '&v=5.131'
    answer          = requests.get(url)
    parsed_string   = answer.json() 
    error =  parser_test_error (parsed_string) 
    if error == '':    
        response  = parsed_string['response']
        for line in response:
            list.append(line)        
    return list   

def parser_get_list_post (list_post):  #### Получение списка групп по постам
    list_post = list_post.split(',')
    return list_post

##################################################################################################################################################################  
          
##################################################################### ПОЛУЧАЕМ ДАННЫЕ ИЗ ОБЩЕГО ##############################################################
def parser_get_group_in_user (user,detail):  ###  Получение списка групп у пользователя
    count  = 100
    offset = 0
    max_count = 1000000000
    list = []
    while offset < max_count:
        token = get_token (["like"])
        url = ''    
        url = url + 'https://api.vk.com/method/groups.get'
        url = url + '?access_token='+str(token[2])
        if detail == 'yes':
            url = url + '&extended=1'
        url = url + '&user_id='+str(user)
        if detail == 'yes':
            url = url + '&fields=nickname'
        url = url + '&v=5.131'
        time.sleep (5)        
        answer          = requests.get(url)
        list = []
        parsed_string   = answer.json() 
        error =  parser_test_error (parsed_string) 
        if error == '':
            response = parsed_string['response']
            items = response['items']
            count_F = response['count']
            max_count = count_F
            print ('         [+] count:',count_F)            
            for line in items:
                offset = offset + 1
                list.append(line) 
        print ('[-----------------------------------------------------------------------------------------------------------------------------------------------]')   
        print ('offset',offset)  
        print ('max_count',max_count)   
        time.sleep (1)                
        return list
    
def parser_get_user_in_group (group):  ###  Получение списка пользователей из групп
    count  = 100
    offset = 0
    max_count = 1000000000
    list = []    
    while offset < max_count:
        token = get_token (["like"])
        url = ''    
        url = url + 'https://api.vk.com/method/groups.getMembers'
        url = url + '?access_token='+str(token[2])
        url = url + '&group_id='+str(group)
        url = url + '&fields=nickname'    
        url = url + '&offset='+str(offset)    
        url = url + '&fields=nickname'    
        url = url + '&v=5.131'
        answer          = requests.get(url)
        parsed_string   = answer.json() 
        print (parsed_string)
        error =  parser_test_error (parsed_string) 
        if error == '':
            response = parsed_string['response']
            items   = response['items'] 
            print (items)
            if  items == []:
                offset = max_count + 10
            count_F = response['count']
            max_count = count_F
            print ('         [+] count:',count_F)
            for line in items:
                offset = offset + 1
                print ('            [+] line:',offset,str(line)[0:400])
                list.append(line) 
        #print ('[-----------------------------------------------------------------------------------------------------------------------------------------------]')   
        #print ('offset',offset)  
        #print ('max_count',max_count)   
        time.sleep (1)
    return list    
         
def parser_get_friend_in_user (user,detail): ###  Получение списка друзей у пользователя
    count  = 100
    offset = 0
    max_count = 1000000000
    labal = 'Yes'
    list = []  
    items = ''
    while labal == 'Yes':
        token = get_token (["like"])
        url = ''    
        url = url + 'https://api.vk.com/method/friends.get'
        url = url + '?access_token='+str(token[2])
        if detail == 'yes':
            url =  url + '&fields=activities,about,blacklisted,blacklisted_by_me,books,bdate,can_be_invited_group,can_post,can_see_all_posts,can_see_audio,can_send_friend_request,can_write_private_message,career,common_count,connections,contacts,city,country,crop_photo,domain,education,exports,followers_count,friend_status,has_photo,has_mobile,home_town,photo_100,photo_200,photo_200_orig,photo_400_orig,photo_50,sex,site,schools,screen_name,status,verified,games,interests,is_favorite,is_friend,is_hidden_from_feed,last_seen,maiden_name,military,movies,music,nickname,occupation,online,personal,photo_id,photo_max,photo_max_orig,quotes,relation,relatives,timezone,tv,universities'
        else:
            url = url + '&fields=nickname'
        url = url + '&user_id='+str(user)
        url = url + '&offset='+str(offset)
        url = url + '&v=5.131'
        answer          = requests.get(url)
        parsed_string   = answer.json() 
        error =  parser_test_error (parsed_string) 
        if error == '':
            try:
                response = parsed_string['response']
            except:       
                print ('[+]',parsed_string)
                exit (0)
            items   = response['items'] 
            count_F = response['count']
            max_count = count_F
            print ('        [+] count:',count_F)
            labal = 'No'
            for line in items:
                offset = offset + 1
                labal = 'Yes'
                list.append(line) 
        else:
            print ('[error]') 
            print ('[+] parsed_string:',parsed_string)
            labal = 'No'
                    
        #print ('[-----------------------------------------------------------------------------------------------------------------------------------------------]')   
        #print ('offset',offset)  
        #print ('max_count',max_count)   
        #print ('labal',labal)   
        #print ('[-----------------------------------------------------------------------------------------------------------------------------------------------]')   
        time.sleep (1)    
    return list
    
def parser_get_followers_in_user (user,detail): ###  Получение списка подписчиков у пользователя
    count  = 1000
    offset = 0
    max_count = 1000000000
    labal = 'Yes'
    list = []  
    items = ''
    while labal == 'Yes':
        token = get_token (["like"])
        url = ''    
        url = url + 'https://api.vk.com/method/users.getFollowers'
        url = url + '?access_token='+str(token[2])
        if detail == 'yes':            
            url = url + '&fields=activities,about,blacklisted,blacklisted_by_me,books,bdate,can_be_invited_group,can_post,can_see_all_posts,can_see_audio,can_send_friend_request,can_write_private_message,career,common_count,connections,contacts,city,country,crop_photo,domain,education,exports,followers_count,friend_status,has_photo,has_mobile,home_town,photo_100,photo_200,photo_200_orig,photo_400_orig,photo_50,sex,site,schools,screen_name,status,verified,games,interests,is_favorite,is_friend,is_hidden_from_feed,last_seen,maiden_name,military,movies,music,nickname,occupation,online,personal,photo_id,photo_max,photo_max_orig,quotes,relation,relatives,timezone,tv,universities'
        else:
            url = url + '&fields=nickname'            
        url = url + '&user_id='+str(user)
        url = url + '&offset='+str(offset)
        url = url + '&count=1000'
        url = url + '&v=5.131'
        time.sleep (2)
        answer          = requests.get(url)
        parsed_string   = answer.json() 
        #print (parsed_string)
        time.sleep (2)
        error =  parser_test_error (parsed_string) 
        if error == '':
            response = parsed_string['response']
            items   = response['items'] 
            count_F = response['count']
            max_count = count_F
            print ('        [+] count:',count_F)
            labal = 'No'
            for line in items:
                offset = offset + 1
                labal = 'Yes'
                print ('            [+] line:',offset,str(line)[0:100])
                list.append(line) 
        time.sleep (1)            
    return list    
    
def parser_get_news_in_group222 (group,news_limit): ###  Получение списка новостей у группы
    url = ''  
    token = get_token (["like"])    
    url = url + 'https://api.vk.com/method/friends.get'
    url = url + '?access_token='+str(token[2])
    url = url + '&fields=nickname'
    url = url + '&user_id='+str(user)
    url = url + '&v=5.131'
    answer          = requests.get(url)
    list = []
    parsed_string   = answer.json() 
    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:
            list.append(line)    
    return list
      
def parser_get_news_in_user (user,list_info): ###  Получение списка новостей у пользователя
    url = ''    
    token = get_token (["like"])       
    url = url + 'https://api.vk.com/method/wall.get'
    url = url + '?access_token='+str(token[2])
    url = url  + '&owner_id='+str(user)
    url = url  + '&fields='+str(list_info)
    url = url + '&v=5.131'
    answer          = requests.get(url)
    list = []
    parsed_string   = answer.json() 
    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:
            list.append(line)    
    return list    

def parser_get_news_in_group (group,list_news): ###  Получение списка новостей у пользователя
    url = ''      
    token = get_token (["like"])  
    url = url + 'https://api.vk.com/method/wall.get'
    url = url + '?access_token='+str(token[2])
    url = url + '&count='+str(list_news)
    url = url  + '&owner_id=-'+str(group)
    #url = url + '&fields=nickname'
    #url = url + '&user_id='+str(user)
    url = url + '&v=5.131'
    answer          = requests.get(url)
    list = []
    parsed_string   = answer.json() 
    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:
            list.append(line)    
    return list        

def parser_get_сomments_in_user (avtor_owner_id,avtor_post_id): ###  Получение списка коментариев у пользователя
    import time
    print ('    [+] avtor_post_id:',avtor_post_id)
    print ('    [+] avtor_owner_id:',avtor_owner_id) 
    token = get_token (["like"])  
    url = ''    
    url = url + 'https://api.vk.com/method/wall.getComments'
    url = url + '?access_token='+str(token[2])
    url = url + '&owner_id='+str(avtor_owner_id)
    url = url + '&post_id='+str(avtor_post_id)
    url = url + '&v=5.131'
    answer          = requests.get(url)
    time.sleep (1)
    list = []
    parsed_string   = answer.json() 
    #print ('parsed_string',parsed_string)
    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:
            list.append(line)  
            print ('        [+] id:',line['id'])
            print ('        [+] from_id:',line['from_id'])
            #print ('        [+] post_id:',line['post_id'])
            print ('        [+] text:',line['text'])

    return list    

def parser_get_сomments_in_group (avtor_owner_id,avtor_post_id): ###  Получение списка коментариев у пользователя
    import time
    print ('    [+] avtor_post_id:',avtor_post_id)
    print ('    [+] avtor_owner_id:',avtor_owner_id) 
    token = get_token (["like"])  
    url = ''    
    url = url + 'https://api.vk.com/method/wall.getComments'
    url = url + '?access_token='+str(token[2])
    url = url + '&owner_id=-'+str(avtor_owner_id)
    url = url + '&post_id='+str(avtor_post_id)
    url = url + '&v=5.131'
    answer          = requests.get(url)
    time.sleep (1)
    list = []
    parsed_string   = answer.json() 
    #print ('parsed_string',parsed_string)
    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:
            list.append(line)  
            print ('        [+] id:',line['id'])
            print ('        [+] from_id:',line['from_id'])
            #print ('        [+] post_id:',line['post_id'])
            #print ('        [+] text:',line['text'])

    return list    

def parser_get_likes_in_group (avtor_owner_id,avtor_post_id): ###  Получение списка коментариев у пользователя
    import time
    print ('    [+] avtor_post_id:',avtor_post_id)
    print ('    [+] avtor_owner_id:',avtor_owner_id) 
    token = get_token (["like"]) 
    url = ''    
    url = url + 'https://api.vk.com/method/likes.getList'
    url = url + '?access_token='+str(token[2])
    url = url + '&type=post'
    url = url + '&owner_id=-'+str(avtor_owner_id)
    url = url + '&item_id='+str(avtor_post_id)
    url = url + '&extended=1'
    url = url + '&v=5.131'
    answer          = requests.get(url)
    time.sleep (1)
    list = []
    parsed_string   = answer.json() 
    print ('parsed_string',parsed_string)
    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:
            list.append(line)  
            print ('        [+] id:',line['id'])
            #print ('        [+] from_id:',line['from_id'])
            #print ('        [+] post_id:',line['post_id'])
            #print ('        [+] text:',line['text'])
           
    #exit (0) 
    return list    

def parser_get_likes_in_user (avtor_owner_id,avtor_post_id): ###  Получение списка коментариев у пользователя
    import time
    print ('    [+] avtor_post_id:',avtor_post_id)
    print ('    [+] avtor_owner_id:',avtor_owner_id) 
    token = get_token (["like"]) 
    url = ''    
    url = url + 'https://api.vk.com/method/likes.getList'
    url = url + '?access_token='+str(token[2])
    url = url + '&type=post'
    url = url + '&owner_id='+str(avtor_owner_id)
    url = url + '&item_id='+str(avtor_post_id)
    url = url + '&extended=1'
    url = url + '&v=5.131'
    answer          = requests.get(url)
    time.sleep (1)
    list = []
    parsed_string   = answer.json() 
    print ('parsed_string',parsed_string)
    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:
            list.append(line)  
            print ('        [+] id:',line['id'])
            #print ('        [+] from_id:',line['from_id'])
            #print ('        [+] post_id:',line['post_id'])
            #print ('        [+] text:',line['text'])
          
    return list    

def parser_get_info_news (post,limit,list_info): ### Получене информации о новости 
    post      = str(post.replace('https://vk.com/feed?w=wall',''))
    token = get_token (["like"])  
    url = ''
    url = url + 'https://api.vk.com/method/wall.getById'
    url = url + '?access_token='+str(token[2])
    url = url + '&posts='+str(post)
    url = url + '&count='+str(limit)
    url = url  + '&extended=1'
    if list_info != '':
        url = url  + '&fields='+list_info
    url = url + '&v=5.131'    
    print ('url',url)
    answer          = requests.get(url)
    list = []
    parsed_string   = answer.json() 
    error =  parser_test_error (parsed_string) 
    post_id  = 0
    owner_id = 0
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:   
            post_id  = line['id']
            owner_id = line['owner_id']
            list.append(line)
    return list,post_id,owner_id

def parser_get_commers_news (info_news,post_id,owner_id):
    print ('    [+] Список коментариев')  
    url = ''      
    token = get_token (["like"])  
    url = "https://api.vk.com/method/wall.getComments"
    url = url + '?access_token='+str(token[2])
    url = url + '&owner_id='+str(owner_id)
    url = url + '&post_id=' +str(post_id)
    url = url + '&extended=0'
    url = url + '&v=5.131"'
    answer          = requests.get(url)
    list = []
    parsed_string   = answer.json()
    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:
            list.append(line) 
    return list

def parser_get_likes_news (info_news,post_id,owner_id):
    url = ''      
    token = get_token (["like"])  
    url = "https://api.vk.com/method/likes.getList"
    url = url + '?access_token='+str(token[2])
    url = url + '&type=post'
    url = url + '&owner_id='+str(owner_id)
    url = url + '&item_id=' +str(post_id)
    url = url + '&extended=0'
    url = url + '&v=5.131"'
    #print ('url',url) 
    answer          = requests.get(url)
    list = []
    parsed_string   = answer.json()
    #print ('[3]',parsed_string)
    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:
            list.append(line) 
    #print (list)
    #parser_save_likes_in_base  (list,1000)
    #parser_save_сomments_in_base (list,1000)
    return  list

def parser_get_info_user (user_id):
    url = ''      
    token = get_token (["like"])  
    url = "https://api.vk.com/method/users.get"
    url = url + '?access_token='+str(token[2])
    url = url + '&user_ids='+str(user_id)
    url = url + '&fields=sex,city,bdate'
    url = url + '&v=5.131"'
    #print ('[url]',url)    
    answer          = requests.get(url)
    list = []
    parsed_string   = answer.json()
    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        #items = response['items'] 
        for line in response:
            list.append(line) 
    return  list

def get_data_in_json (line,list_info):  ### Готовим выходной параметр для вывода в строку 
    #print ('list_info',list_info)
    list_info = list_info.split (',')    
    answer = ''
    n = 0
    simvol_epson = iz_telegram.load_setting ('@parser3141_bot','Отсутствие')      ## Заполнение ответа 
    for param in list_info:
        n = n + 1
        if n == 1:
            raz = ''
        else:    
            raz = iz_telegram.load_setting ('@parser3141_bot','Разделитель')      ## Зпполнение ответа            
        try:
            plus = str(line[param])
        except:        
            pass
            plus = 'no'            
            
        try:    
            if param == 'occupation':
                plus = line['occupation']['name']
        except:        
            pass        

        try:  
            if param == 'universities':
                nm1 = line['universities']
                for nm2 in nm1:
                    plus = nm2['name']+','+nm2['chair_name']
        except:
            pass                
            
            
            
        try: 
            if param == 'relation':
                plus = line['relation']            
                if plus == 1:
                   plus = 'не женат/не замужем'
                if plus == 2:
                   plus = 'есть друг/есть подруга'
                if plus == 3:
                   plus = 'помолвлен/помолвлена'
                if plus == 4:
                   plus = 'женат/замужем'
                if plus == 5:
                   plus = 'всё сложно'
                if plus == 6:
                   plus = 'в активном поиске'
                if plus == 7:
                   plus = 'влюблён/влюблена'
                if plus == 8:
                   plus = 'в гражданском браке'
                if plus == 0:
                   plus = 'не указано'
        except:        
            pass


            
        try:
            if param == 'contacts':
                plus = line['mobile_phone']  
        except:   
            pass                 

        try: 
            if param == 'career':  
                nm1 = line['career']
                for nm2 in nm1: 
                    plus = nm2['position']                       
        except:   
            pass


        try:  
            if param == 'country':  
                plus = line['country']['title']        
        except: 
            pass        
      
        try:
            if param == 'city':  
                plus = line['city']['title']        
        except:   
            pass         
            
        if param == 'well_url':
            plus = str("https://vk.com/?w=wall"+str(line['owner_id'])+"_"+str(line['id'])+"")           ### id"+str(line['owner_id'])+"     
        
        if param == 'date':
            from datetime import datetime
            ts = int(plus)
            plus = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            plus = str(plus)            
        answer = answer + raz + plus
    
    return answer        

def get_god (bdate):   
    gt = ''
    if 1==1:    
        if len(str(bdate)) == 8:                                                   
            god = int(str(bdate)[4:10])
            yang = 2020 - god                            
            if yang <= 18:
                gt = '0-18'
            if yang >= 18 and yang <= 24:
                gt = '18-24'
            if yang >= 25 and yang <= 34:
                gt = '25-34'
            if yang >= 35 and yang <= 44:
                gt = '35-44'
            if yang >= 45 and yang <= 54:
                gt = '45-54'
            if yang >= 55 and yang <= 64:
                gt = '55-64'
            if yang >= 65 and yang <= 100:
                gt = '65-100'
    return gt            

def clear_task (task_id):
    sql = "DELETE FROM vk_answer where task_id = "+str(task_id)+""
    cursor.execute(sql) 
    db.commit()

##################################################################################################################################################################
    
def parser_active_user_in_base (users,task_id,detail,main,list_info):
    n = 0
    for line in users:
        n = n + 1
        id  = 0  
        try:
            id_user = line['id']   
        except:   
            id_user = line
        try: 
            data_name = line['first_name'] +" "+ line['last_name'] 
        except:   
            data_name = line          
        data_big = get_data_in_json (line,list_info)             
        data_big = iz_func.change (str(data_big))  
        name     = iz_func.change (str(line['id']))
               
        additional = iz_telegram.load_setting ('@parser3141_bot','get_info_user_Additional')    

        if additional.find ("%video%") != -1:
            list,count = parser_get_video (id_user)        
            additional = additional.replace("%video%",str(count))
            
        if additional.find ("%grup%") != -1:
            list,count = parser_get_grup (id_user)        
            additional = additional.replace("%grup%",str(count))
            
        if additional.find ("%photo%") != -1:
            list,count = parser_get_photos (id_user)        
            additional = additional.replace("%photo%",str(count))
            
        if additional.find ("%friends%") != -1:
            list,count = parser_get_friends (id_user)        
            additional = additional.replace("%friends%",str(count))
        
        if additional.find ("%followers%") != -1:
            list,count = parser_get_followers (id_user)        
            additional = additional.replace("%followers%",str(count))
        
        
        
        
        
        sql = "INSERT INTO vk_answer (`comment`,`data_big`,`data_id`,`data_name`,`name`,`status`,`task_id`,`additional`) VALUES ('','"+str(data_big)+"','"+str(id_user)+"','"+str(data_name)+"','"+str(name)+"','',"+str(task_id)+",'"+str(additional)+"')" 
        cursor.execute(sql)              
        print ('         [+] Записан :',n,name,'('+str(id_user)+')')
        db.commit()    

def get_data_in_list (name,data_big):
    data = ''
    try: 
        data = data_big[name]
    except Exception as e:
        print ('[+]',e)    
        data = ''
    return data    

def parser_save_user_in_base (users,task_id,detail,status,user_id,list_info):
    import time
    print ('[+] Записываем в базу данный пользователей',status,detail)
    n = 0
    #if status == 'new':
    #    sql = "DELETE FROM vk_answer where task_id = "+str(task_id)+""
    #    cursor.execute(sql) 
    #    db.commit()     
    #else:
    #    pass    
    for line in users:
        n = n + 1
        id  = 0  
        try:
            id_user = line['id']   
        except:   
            id_user = line            
        try: 
            name = line['nickname'] +" "+ line['first_name'] +" "+ line['last_name'] 
        except:   
            name = ''                
        answer = ""      
        #list = ['activities','about','blacklisted','blacklisted_by_me','books','bdate','can_be_invited_group','can_post','can_see_all_posts','can_see_audio','can_send_friend_request','can_write_private_message','career','common_count','connections','contacts','city','country','crop_photo','domain','education','exports','followers_count','friend_status','has_photo','has_mobile','home_town','photo_100','photo_200','photo_200_orig','photo_400_orig','photo_50','sex','site','schools','screen_name','status','verified','games','interests','is_favorite','is_friend','is_hidden_from_feed','last_seen','maiden_name','military','movies','music','nickname','occupation','online','personal','photo_id','photo_max','photo_max_orig','quotes','relation','relatives','timezone','tv','universities']                   
        if list_info == '':
            list_info = 'activities,about,blacklisted,blacklisted_by_me,books,bdate,can_be_invited_group,can_post,can_see_all_posts,can_see_audio,can_send_friend_request,can_write_private_message,career,common_count,connections,contacts,city,country,crop_photo,domain,education,exports,followers_count,friend_status,has_photo,has_mobile,home_town,photo_100,photo_200,photo_200_orig,photo_400_orig,photo_50,sex,site,schools,screen_name,status,verified,games,interests,is_favorite,is_friend,is_hidden_from_feed,last_seen,maiden_name,military,movies,music,nickname,occupation,online,personal,photo_id,photo_max,photo_max_orig,quotes,relation,relatives,timezone,tv,universities'
        
        data_big = get_data_in_json (line,list_info)
        
        data_big     = iz_func.change (str(data_big)) 
        name     = iz_func.change (str(name)) 
        
        if detail == 'yes':        
            sql = "INSERT INTO vk_answer (`comment`,`data_big`,`data_id`,`data_name`,`name`,`status`,`task_id`,`additional`) VALUES ('','"+str(data_big)+"','"+str(id_user)+"','"+str(name)+"','"+str(user_id)+"','',"+str(task_id)+",'')"
        else:    
            sql = "INSERT INTO vk_answer (`comment`,`data_big`,`data_id`,`data_name`,`name`,`status`,`task_id`,`additional`) VALUES ('','"+str(data_big)+"','"+str(id_user)+"','"+str(name)+"','"+str(user_id)+"','',"+str(task_id)+",'')"
            
        #print ('[sql]',sql)    
        cursor.execute(sql)              
              
        print ('         [+] Записан :',n,name,'('+str(id_user)+')')
        db.commit()    
                         
def parser_save_group_in_base (groups,task_id,detail,master):
    n = 0
    sql = "DELETE FROM vk_answer where task_id = "+str(task_id)+""
    cursor.execute(sql) 
    db.commit() 
       
    for line in groups:
        id  = 0  
        if detail == 'yes':
            id_group = line['id']
        else:    
            id_group = line

        try: 
            name = line['name']  
        except:   
            name = ''                

        name = iz_func.change (name)        
        data_big = iz_func.change (str(line))

        if 1==1:    
            sql = "INSERT INTO vk_answer (`comment`,`data_big`,`data_id`,`data_name`,`name`,`status`,`task_id`,`additional`) VALUES ('','"+str(data_big)+"','"+str(id_group)+"','"+str(name)+"','"+str(master)+"','',"+str(task_id)+",'')"
            cursor.execute(sql)
            db.commit()  
            print ('         [+] Записан :',name,'('+str(id_group)+')')            
        db.commit()

def parser_save_news_in_base (news,task_id,list_info):   
    for new in news:
        print ('----------------------------------------------')
        print ('[new]',new)
        print ('----------------------------------------------')
        id  = 0  
        news_id   = new['id']
        news_date = new['date']        
        data_name = str(news_id)+";"+str(news_date)                
        name = new['text']  
        name = iz_func.change (name)                
        data_big = get_data_in_json (new,list_info)         
        if 1==1:
            data_big = iz_func.change (str(data_big))             
            sql = "INSERT INTO vk_answer (`comment`,`data_big`,`data_id`,`data_name`,`name`,`status`,`task_id`,`additional`) VALUES ('news','"+str(data_big)+"','"+str(data_name)+"','"+str(name[0:254])+"','news','',"+str(task_id)+",'')" 
            cursor.execute(sql)
            db.commit()  
            print ('         [+] Записан :',name,'('+str(news_id)+')')
        else:
            print ('         [+] Обновлен:',name,'('+str(news_id)+')')           

def parser_save_сomments_in_base (сomments,task_id,avtor):
    for сomment in сomments:
        #print ('[+] сomment',сomment)
        id  = 0 
        сomment_id = сomment['id']
        from_id    = сomment['from_id'] 
        name = avtor
        data_id = str(from_id)
        data_big = сomment['text']
        #data_big = #z_func.change (str(сomment)) 
        user_id = from_id
        user  =  parser_get_info_user (user_id)
        for ln in user:
            try:
                sex    = ln['sex']
            except:  
                sex = ''
            if sex == 1:
                sex = 'женский'
            if sex == 2:
                sex = 'мужской'       
            try:    
                bdate = ln['bdate']
            except:     
                bdate = ''
            bdate = get_god (bdate)
            try:    
                city   = ln['city']['title']
            except: 
                city   = ''                
            try:    
                education   = ln['education']
            except: 
                education   = ''
        data_name = str(sex)+';'+str(bdate)+";"+str(city)+';'+str(education)+';'+''        
        sql = "INSERT INTO vk_answer (`comment`,`data_big`,`data_id`,`data_name`,`name`,`status`,`task_id`,`additional`) VALUES ('Комментарий','"+str(data_big)+"','"+str(from_id)+"','"+str(data_name)+"','"+str(name)+"','',"+str(task_id)+",'')"            
        cursor.execute(sql)
        db.commit()  

def parser_save_likes_in_base (likes,task_id,avtor):
    for like in likes:
        #print ('[+] like',like)
        id  = 0 
        data_id = str(like)
        name = avtor
        user_id = like
        user  =  parser_get_info_user (user_id)
        for ln in user:
            try:
                sex    = ln['sex']
            except:  
                sex = ''
            if sex == 1:
                sex = 'женский'
            if sex == 2:
                sex = 'мужской'
            try:    
                bdate = ln['bdate']
            except:     
                bdate = ''
            bdate = get_god (bdate)
            try:    
                city   = ln['city']['title']
            except: 
                city   = ''
            try:    
                education   = ln['education']
            except: 
                education   = ''                    
        data_name = str(sex)+';'+str(bdate)+";"+str(city)+';'+str(education)+';'+''

        data_big = ''
        sql = "INSERT INTO vk_answer (`comment`,`data_big`,`data_id`,`data_name`,`name`,`status`,`task_id`,`additional`) VALUES ('Лайк','"+str(data_big)+"','"+str(data_id)+"','"+str(data_name)+"','"+str(name)+"','',"+str(task_id)+",'')"            
        cursor.execute(sql)
        db.commit()  

def parser_test_error (parsed_string):  ### Проверка на наличие в ответе ошибки
    error = ''
    try:                    
        error = parsed_string['error']
    except Exception as e:
        error = ''      
    return error    

def parser_save_answer (sql,task_id):
    sql = iz_func.change (sql)
    sql = "UPDATE vk_task SET answer = '"+sql+"' WHERE id = "+str(task_id)+" "
    cursor.execute(sql)  
    db.commit()  
    sql = "UPDATE vk_task SET status_task = 'Выполнен' WHERE id = "+str(task_id)+" "
    cursor.execute(sql)
    db.commit()
    sql = "SELECT COUNT(*) FROM vk_answer where task_id = "+str(task_id)
    cursor.execute(sql)
    results = cursor.fetchall()
    summ = results[0]['COUNT(*)']
    sql = "UPDATE vk_task SET namebot = 'найдено:"+str(summ)+"' WHERE id = "+str(task_id)+" "
    cursor.execute(sql)
    db.commit()
    if summ == 0:
        sql = "UPDATE vk_task SET status_task = 'Ошибка' WHERE id = "+str(task_id)
        cursor.execute(sql)
        db.commit()
   
def save_comment_to_base (avtor_owner_id,avtor_post_id,comment_from_id,comment_id,comment_post_id,comment_text):  # Обработка для пополнения данных
    import iz_func
    comment_text = iz_func.change (comment_text)
    id = 0                     
    sql = "select id,`comment_text` from vk_comment where avtor_owner_id = "+str(avtor_owner_id)+" and avtor_post_id = "+str(avtor_post_id)+" and comment_from_id = "+str(comment_from_id)+" and comment_id = "+str(comment_id)+" and comment_post_id = "+str(comment_post_id)+""
    cursor_save.execute(sql)
    data = cursor_save.fetchall()
    for rec in data:
        id,text = rec.values()

    if comment_text != '':                    
        if id == 0:
            sql = "INSERT INTO vk_comment (avtor_owner_id,avtor_post_id,comment_from_id,comment_id,comment_post_id,comment_text) VALUES ("+str(avtor_owner_id)+","+str(avtor_post_id)+","+str(comment_from_id)+","+str(comment_id)+","+str(comment_post_id)+",'"+str(comment_text)+"')".format ()
            cursor_save.execute(sql)
            db_save.commit()
            lastid = cursor_save.lastrowid
            print ('[+] Запись,Запись,Запись,Запись,Запись,Запись,Запись,Запись,Запись,Запись,Запись,Запись,Запись,Запись',sql)
        else:
            print ('[+] Пропуск,Пропуск,Пропуск,Пропуск,Пропуск,Пропуск,Пропуск,Пропуск,Пропуск,Пропуск,Пропуск,Пропуск')
    else:
        print ('[+] Нет текста',comment_text)        

def get_task (namebot):
    db,cursor = connect ()
    sql = "select `id`,name,offset,data from vk_task where status = '' and namebot = '"+str(namebot)+"'"
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

def master_json (user_id,name,line,task_id,cursor,namebot):
    answer = ''
    try: 
        answer = line[name[0]]
    except: 
        pass    
    if name[1] == "str":
        save_data = change (str(answer))
        sql = "UPDATE vk_get_full_user SET `"+str(name[0])+"` = '"+str(save_data)+"' WHERE `name` = '"+str(user_id)+"' and task_id = "+str(task_id)+""
        cursor.execute(sql)
        return answer         
    if name[1] == "int":
        if answer == '':
            answer = 0
        save_data = answer
        sql = "UPDATE vk_get_full_user SET `"+str(name[0])+"` = "+str(save_data)+" WHERE `name` = '"+str(user_id)+"' and task_id = "+str(task_id)+""
        cursor.execute(sql)
        return answer 

def master_inser (user_id,base_name,list,task_id,namebot):
    sql = "INSERT INTO "+str(base_name)+" (name,task_id,namebot,sources,answer"
    for name in list:  
        sql = sql + ",`"+str(name[0])+"`"
    sql = sql + ") VALUES ('"+str(user_id)+"','"+str(task_id)+"','"+str(namebot)+"','',''"
    for name in list:
        if name[1] == 'str':
            sql = sql + ",''"
        if name[1] == 'int':  
            sql = sql + ",0"  
    sql = sql + ")"    
    return sql    

def master_test_save (base_name,pl,user_id,list,task_id,cursor,namebot):
    answer = False 
    sql = "select `id` from "+str(base_name)+" where "+str(pl)+" = '"+str(user_id)+"' and task_id = "+str(task_id)+" and namebot = '"+str(namebot)+"' limit 1"   ### 
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        answer  = True
    if answer == False:
        print ('        [+] Новый пользователь',user_id)
        sql = master_inser (user_id,'vk_get_full_user',list,task_id,namebot)
        cursor.execute(sql)         
    else:
        pass
        #print ('        [+] Обновление')      
    return answer      

def save_full_user (items,task_id,namebot):    
    db,cursor = connect ()
    for line in items:
        list = [['first_name','str'],['last_name','str'],['city','str'],['country','str'],['site','str'],['sex','int'],['nickname','str'],['bdate','str'],['about','str'],['status','str'],['followers_count','int']]                                           
        user_id = line['id']  
        answer = master_test_save ('vk_get_full_user','name',user_id,list,task_id,cursor,namebot)
        for pl in list: 
            if answer == False:
                name = master_json (user_id,pl,line,task_id,cursor,namebot)
        if answer == False:        
            pass
        db.commit()

def complite_line_fl (rec):
    id,name,city,sex,bdate = rec.values() 
    answer = ''
    answer = answer + '1,'
    if sex == 2:
        answer = answer + 'male,'
    if sex == 1:   
        answer = answer + 'female,'
    gt = ''   
    if len(str(bdate)) == 8:                                                   
        god = int(str(bdate)[4:10])
        yang = 2020 - god                            
        if yang <= 18:
            gt = '0-18'
            if yang >= 18 and yang <= 24:
                gt = '18-24'
            if yang >= 25 and yang <= 34:
                gt = '25-34'
            if yang >= 35 and yang <= 44:
                gt = '35-44'
            if yang >= 45 and yang <= 54:
                gt = '45-54'
            if yang >= 55 and yang <= 64:
                gt = '55-64'
            if yang >= 65 and yang <= 100:
                gt = '65-100'
    answer = answer + gt+','
    answer = answer + ','    ###  Образование
    answer = answer + ','    ###  Доход
    answer = answer + city_title + ','                              
    answer = answer + rec_task['namebot'] + ','  
    answer = answer + rec_task['namebot'] + ','                           
    url = 'https://vk.com/id'+name
    answer = answer + url + ''
    return answer 

def send_admin_message (namebot,name):     
    list_admin = iz_telegram.list_admin (namebot)
    for user_id in list_admin:
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,name,'S',0)
        print ('[user_id]',user_id)
        time.sleep (2)

def list_line_and_count (parsed_string):
    list  = []
    count = 0
    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        count = response['count']
        for line in items:
           list.append(line)  
           #print ('        [+] id:',line['id'])
    return list,count

def parser_get_video (avtor_owner_id):
    import time
    import requests
    token = get_token (["like"]) 
    url = ''    
    url = url + 'https://api.vk.com/method/video.get'           #?access_token=73c5444fbf26ceed3cf1325500d9afc1e0b42bd4d43dd086d89c90bf3319a31762b66bddf8546590650c2&owner_id=24709387&extended=0&v=5.131   
    url = url + '?access_token='+str(token[2])
    url = url + '&owner_id='+str(avtor_owner_id)
    url = url + '&extended=0'
    url = url + '&v=5.131'
    
    print ('[url]',url)
    
    answer          = requests.get(url)
    time.sleep (1)    
    parsed_string   = answer.json() 
    list,count = list_line_and_count (parsed_string)      
    return list,count    
    
def parser_get_grup (avtor_owner_id):
    import time
    import requests
    token = get_token (["like"]) 
    url = ''    
    url = url + 'https://api.vk.com/method/groups.get'           #?access_token=73c5444fbf26ceed3cf1325500d9afc1e0b42bd4d43dd086d89c90bf3319a31762b66bddf8546590650c2&owner_id=24709387&extended=0&v=5.131   
    url = url + '?access_token='+str(token[2])
    url = url + '&user_id='+str(avtor_owner_id)
    url = url + '&extended=0'
    url = url + '&v=5.131'
    answer          = requests.get(url)
    time.sleep (1)    
    parsed_string   = answer.json() 
    #print ('parsed_string',parsed_string)
    list,count = list_line_and_count (parsed_string)      
    return list,count     

def parser_get_photos (avtor_owner_id):
    import time
    import requests
    token = get_token (["like"]) 
    url = ''    
    url = url + 'https://api.vk.com/method/photos.getAll'           #?access_token=73c5444fbf26ceed3cf1325500d9afc1e0b42bd4d43dd086d89c90bf3319a31762b66bddf8546590650c2&owner_id=24709387&extended=0&v=5.131   
    url = url + '?access_token='+str(token[2])
    url = url + '&owner_id='+str(avtor_owner_id)
    #url = url + '&album_id=saved' 
    #url = url + '&extended=0'
    url = url + '&v=5.131'
    answer          = requests.get(url)
    time.sleep (1)    
    parsed_string   = answer.json() 
    #print ('parsed_string',parsed_string)
    list,count = list_line_and_count (parsed_string)      
    return list,count      
    
    
def parser_get_friends (avtor_owner_id):
    import time
    import requests
    token = get_token (["like"]) 
    url = ''    
    url = url + 'https://api.vk.com/method/friends.get'           #?access_token=73c5444fbf26ceed3cf1325500d9afc1e0b42bd4d43dd086d89c90bf3319a31762b66bddf8546590650c2&owner_id=24709387&extended=0&v=5.131   
    url = url + '?access_token='+str(token[2])
    url = url + '&user_id='+str(avtor_owner_id)
    #url = url + '&album_id=saved' 
    #url = url + '&extended=0'
    url = url + '&v=5.131'
    answer          = requests.get(url)
    time.sleep (1)    
    parsed_string   = answer.json() 
    #print ('parsed_string',parsed_string)
    list,count = list_line_and_count (parsed_string)      
    return list,count      


def parser_get_followers (avtor_owner_id):
    import time
    import requests
    token = get_token (["like"]) 
    url = ''    
    url = url + 'https://api.vk.com/method/users.getFollowers'           #?access_token=73c5444fbf26ceed3cf1325500d9afc1e0b42bd4d43dd086d89c90bf3319a31762b66bddf8546590650c2&owner_id=24709387&extended=0&v=5.131   
    url = url + '?access_token='+str(token[2])
    url = url + '&user_id='+str(avtor_owner_id)
    #url = url + '&album_id=saved' 
    #url = url + '&extended=0'
    url = url + '&v=5.131'
    #print ('url',url)
    answer          = requests.get(url)
    time.sleep (1)    
    parsed_string   = answer.json() 
    #print ('parsed_string',parsed_string)
    list,count = list_line_and_count (parsed_string)      
    return list,count      



if options.menu == '24':
    print ('[+] Тестируем данные')
    avtor_owner_id = '24709387'
    list,count = parser_get_video (avtor_owner_id)
    print (count)

if options.menu == '23':
    import json
    import time
    import iz_func
    import requests
    print ('[+] Скачиваем друзей у пользователя ')    
    namebot = 'Оренбург'
    namebot = options.city
    print ('[+] Обрабатываем город ',namebot)    
    time.sleep (20) 
    db,cursor = connect ()    
    sql = "select id,name from vk_get_full_user where city  like '%"+str(namebot)+"%' and answer = '' limit 1000"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id_task,name = rec.values() 
        print ('    [+] Обрабатываем пользователя:',id_task,name)
        list = parser_get_followers_in_user (name,'yes')
        save_full_user (list,id_task,namebot)
        db.commit()
        sql = "SELECT COUNT(*) FROM vk_get_full_user where task_id = "+str(id_task)+" and namebot = '"+str(namebot)+"'"
        cursor.execute(sql) 
        results = cursor.fetchall()[0]
        summ = results['COUNT(*)']
        report = '{"base":'+str(summ)+'}'
        sql = "UPDATE vk_get_full_user SET `answer` = '"+str(report)+"' WHERE `id` = "+str(id_task)+""
        cursor.execute(sql)           
        db.commit()      

if options.menu == '21':
    import json
    import iz_func
    print ("[+] Выгружаем данные в файл - Друзей")
    import iz_func    
    my_Friend = open("Friend_7000000.csv", "w+")
    db,cursor = connect ()    
    sql = "select id,name,city,sex,bdate,first_name,last_name from vk_get_full_user where  task_id > 104  limit 1000000 OFFSET 6000000" ### На одну меньше
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,name,city,sex,bdate,first_name,last_name = rec.values() 
        print ('[+] id,name,city,sex,bdate,first_name,last_name',id,name,city,sex,bdate,first_name,last_name)
        answer = ''
        answer = answer + '1,'  
        city = iz_func.change_back (city)
        city = city.replace("'",'"')  
        answer = answer + name + ','       
        try:            
            city_title = json.loads(city)['title']        
        except Exception as e:  
            #print ('error [city]',city)
            city_title = ''  
        if sex == 2:
            answer = answer + 'male,'
        if sex == 1:   
            answer = answer + 'female,'                          
        gt = ''   
        if len(str(bdate)) == 8:                                                   
            god = int(str(bdate)[4:10])
            yang = 2020 - god                            
            if yang <= 18:
                gt = '0-18'
            if yang >= 18 and yang <= 24:
                gt = '18-24'
            if yang >= 25 and yang <= 34:
                gt = '25-34'
            if yang >= 35 and yang <= 44:
                gt = '35-44'
            if yang >= 45 and yang <= 54:
                gt = '45-54'
            if yang >= 55 and yang <= 64:
                gt = '55-64'
            if yang >= 65 and yang <= 100:
                gt = '65-100'
        answer = answer + gt+','
        answer = answer + ','    ###  Образование
        answer = answer + ','    ###  Доход
        answer = answer + city_title + ','                                                      
        name_full = first_name + ' ' + last_name                        
        answer = answer + name_full + ','
        answer = answer + '' + ','
        answer = answer + '' + ','                        
        url = 'https://vk.com/id'+name
        answer = answer + url + ''                                                     
        my_Friend.write(answer+'\n') 
    my_Friend.close()        

if options.menu == '20':
    import json
    import time
    import iz_func
    import requests
    print ('[+] Скачиваем друзей у пользователя ')    
    namebot = 'Оренбург'
    namebot = options.city
    print ('[+] Обрабатываем город ',namebot)    
    time.sleep (20) 
    db,cursor = connect ()    
    sql = "select id,name from vk_get_full_user where city  like '%"+str(namebot)+"%' and sources = '' limit 1000"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id_task,name = rec.values() 
        print ('    [+] Обрабатываем пользователя:',id_task,name)
        list = parser_get_friend_in_user (name,'yes')
        save_full_user (list,id_task,namebot)
        db.commit()
        sql = "SELECT COUNT(*) FROM vk_get_full_user where task_id = "+str(id_task)+" and namebot = '"+str(namebot)+"'"
        cursor.execute(sql) 
        results = cursor.fetchall()[0]
        summ = results['COUNT(*)']
        report = '{"base":'+str(summ)+'}'
        sql = "UPDATE vk_get_full_user SET `sources` = '"+str(report)+"' WHERE `id` = "+str(id_task)+""
        cursor.execute(sql)           
        db.commit()      

if options.menu == '19':   # Выводим инфрмацию по новости пользователя или группы
    import iz_func
    import json
    import time
    import requests    
    db,cursor = iz_func.connect ()
    name_grup = "https://vk.com/3dot14?w=wall24709387_10216"
    name_grup = "https://vk.com/feed?w=wall-15722194_6454550"
    name_grup = "https://vk.com/feed?w=wall-15722194_6437318" 
    group     = str(name_grup.replace('https://vk.com/feed?w=wall',''))
    url = ''      
    token = get_token (["like"])  
    url = url + 'https://api.vk.com/method/wall.getById'
    url = url + '?access_token='+str(token[2])
    url = url  + '&posts='+str(group)
    url = url  + '&extended=1'
    url = url + '&v=5.131'    
    print ('    [+] Информация о новости')    
    answer          = requests.get(url)
    list = []
    parsed_string   = answer.json() 
    #print ('[1]',parsed_string)
    error =  parser_test_error (parsed_string) 
    post_id  = 0
    owner_id = 0
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:
            list.append(line)    
            post_id  = line['id']
            owner_id = line['owner_id']

    parser_save_news_in_base (list,1000)

    print ('[+] Список коментариев')
    url = ''      
    token = get_token (["like"])  
    url = "https://api.vk.com/method/wall.getComments"
    url = url + '?access_token='+str(token[2])
    url = url + '&owner_id='+str(owner_id)
    url = url + '&post_id=' +str(post_id)
    url = url + '&extended=0'
    url = url + '&v=5.131"'

    #print ('url',url) 

    answer          = requests.get(url)
    list = []
    parsed_string   = answer.json()
    #print ('[2]',parsed_string)
    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:
            list.append(line) 

    #print (list)
    parser_save_сomments_in_base (list,1000)
    

    #exit (0)

    
    print ('[+] Лайки')
    #url = "https://api.vk.com/method/likes.getList
    #?access_token=a59492d8acaac8b17bc18441d113092cc02e250d14daf11d8f8e554d96f23e2bf1ecac676032c55e4c494&type=post
    #&owner_id=-15722194&item_id=6454550&extended=0&v=5.131"
    #answer          = requests.get(url)
    #print (answer.json() )
    #print ('-----------------------')


    url = ''      
    token = get_token (["like"])  
    url = "https://api.vk.com/method/likes.getList"
    url = url + '?access_token='+str(token[2])
    url = url + '&type=post'
    url = url + '&owner_id='+str(owner_id)
    url = url + '&item_id=' +str(post_id)
    url = url + '&extended=0'
    url = url + '&v=5.131"'

    print ('url',url) 

    answer          = requests.get(url)
    list = []
    parsed_string   = answer.json()
    print ('[3]',parsed_string)



    error =  parser_test_error (parsed_string) 
    if error == '':
        response = parsed_string['response']
        items = response['items'] 
        for line in items:
            list.append(line) 

    print (list)
    parser_save_likes_in_base  (list,1000)
    #parser_save_сomments_in_base (list,1000)


    exit (0)


    
    print ('[+] Информация о комантарии')
    url = "https://api.vk.com/method/wall.getComment?access_token=a59492d8acaac8b17bc18441d113092cc02e250d14daf11d8f8e554d96f23e2bf1ecac676032c55e4c494&owner_id=-15722194&comment_id=6454620&extended=0&v=5.131"
    answer          = requests.get(url)
    print (answer.json() )
    #print ('-----------------------')
    







    print ('[+] Получение комантария к коментариям')
    url = "https://api.vk.com/method/wall.getComments?access_token=a59492d8acaac8b17bc18441d113092cc02e250d14daf11d8f8e554d96f23e2bf1ecac676032c55e4c494&owner_id=-15722194&post_id=6454550&need_likes=1&extended=0&comment_id=6454620&v=5.131"
    answer          = requests.get(url)
    print (answer.json() )
    
if options.menu == '18':
    import json
    import iz_func
    print ("[+] Выгружаем данные в файл")
    import iz_func    
    my_DNR = open("DNR_VK.csv", "w+")
    my_LNR = open("LNR_VK.csv", "w+")
    db,cursor = connect ()    
    sql = "select id,name,data,namebot from vk_task where 1=1"
    cursor.execute(sql)
    data_task = cursor.fetchall()
    for rec_task in data_task:
        print ('[+] task',rec_task)
    sql = "select id,name,city,sex,bdate,first_name,last_name from vk_get_full_user where  task_id < 105 and task_id <> 1 "
    cursor.execute(sql)
    data = cursor.fetchall()
    print ('[+] data:',data)
    for rec in data:
        id,name,city,sex,bdate,first_name,last_name = rec.values() 
        print ('[+] :',name)
        if city != '': 
            city = iz_func.change_back (city)
            city = city.replace("'",'"')
            try:            
                city_title = json.loads(city)['title']        
            except Exception as e:  
                print ('error [city]',city)
                city_title = ''              
            for rec_task in data_task:
                if rec_task['data'] == city_title:
                    print ('    [+] task',rec_task['data'],rec_task['namebot'])
                    if rec_task['namebot'] == 'ДНР':
                        answer = ''
                        answer = answer + '1,'
                        if sex == 2:
                           answer = answer + 'male,'
                        if sex == 1:   
                           answer = answer + 'female,'
                           
                        gt = ''   
                        if len(str(bdate)) == 8:                                                   
                            god = int(str(bdate)[4:10])
                            yang = 2020 - god                            
                            if yang <= 18:
                                gt = '0-18'
                            if yang >= 18 and yang <= 24:
                                gt = '18-24'
                            if yang >= 25 and yang <= 34:
                                gt = '25-34'
                            if yang >= 35 and yang <= 44:
                                gt = '35-44'
                            if yang >= 45 and yang <= 54:
                                gt = '45-54'
                            if yang >= 55 and yang <= 64:
                                gt = '55-64'
                            if yang >= 65 and yang <= 100:
                                gt = '65-100'
                        answer = answer + gt+','
                        answer = answer + ','    ###  Образование
                        answer = answer + ','    ###  Доход
                        answer = answer + city_title + ','                                                      
                        name_full = first_name + ' ' + last_name                         
                        answer = answer + name_full + ','                          
                        answer = answer + rec_task['namebot'] + ','
                        answer = answer + rec_task['namebot'] + ','                        
                        url = 'https://vk.com/id'+name
                        answer = answer + url + ''                            
                           
                        my_DNR.write(answer+'\n')
                        
                    if rec_task['namebot'] == 'ЛНР':
                        answer = ''
                        answer = answer + '1,'
                        if sex == 2:
                           answer = answer + 'male,'
                        if sex == 1:   
                           answer = answer + 'female,'
                           
                        gt = ''   
                        if len(str(bdate)) == 8:                                                   
                            god = int(str(bdate)[4:10])
                            yang = 2020 - god                            
                            if yang <= 18:
                                gt = '0-18'
                            if yang >= 18 and yang <= 24:
                                gt = '18-24'
                            if yang >= 25 and yang <= 34:
                                gt = '25-34'
                            if yang >= 35 and yang <= 44:
                                gt = '35-44'
                            if yang >= 45 and yang <= 54:
                                gt = '45-54'
                            if yang >= 55 and yang <= 64:
                                gt = '55-64'
                            if yang >= 65 and yang <= 100:
                                gt = '65-100'
                        answer = answer + gt+','
                        answer = answer + ','    ###  Образование
                        answer = answer + ','    ###  Доход
                        answer = answer + city_title + ',' 
                        name_full = first_name + ' ' + last_name                         
                        answer = answer + name_full + ','                        
                        answer = answer + rec_task['namebot'] + ','  
                        answer = answer + rec_task['namebot'] + ','                           
                        url = 'https://vk.com/id'+name
                        answer = answer + url + ''                                         
                        
                        my_LNR.write(answer+'\n')

    my_DNR.close()
    my_LNR.close()

if options.menu == '17':   # Ютубе
    import iz_func
    import json
    import time
    import json
    import requests
    print ('[+] Выполнение задачи по проекту Ютубе')
    db,cursor = iz_func.connect ()
    sql = "select id,name,dataT,status from vk_task where (status_task = '' or status_task = 'Ожидание') and user_id = 'YT' "
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        task_id,name,dataT,status = rec.values()   
        dataT = iz_func.change_back (dataT)
        dataT = dataT.replace("'",'"')
        dataT = dataT.replace('"{','{')
        dataT = dataT.replace('}"','}')
        b = json.loads(dataT)
        data = b['data']
        print ('    [+] data:',data) 
        try:
            list_data = data['user_id']
        except Exception as e:    
            list_data = ''
            #print ('[+] Ощибка в строке ',task_id)
            #print ('[+] ',dataT)
            #exit (0)
        try:    
            detail = data['detail']    
        except Exception as e:    
            detail = 'no' 
        main = data['main']    
        
        if main == 'get_info_user':             
            if status == '':
                #sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
                param =  {"task_type_id": 3,"data": {"loms": ["TbA9Bd1vxF4", "SfYaAQ9-RnE"]},"priority": 4,"fields": ["."]}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer)
                print ("[+] answer",answer.json() )
                data  = answer.json()
                #data = json.loads(answer.json()) # string to json
                answer_id = data["task_id"]            
                sql = "UPDATE vk_task set status = 'Ожидание: "+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                cursor.execute(sql)
                db.commit()  
                sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                cursor.execute(sql)
                db.commit()
            else:
                id_status = status.replace('Ожидание: ','')
                print ('[+] id_status',id_status)
                param = {"command":"status","id":int(id_status)}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer.json() )                
                #answer_id = answer.json()['task']['id']            
                #sql = "UPDATE vk_task set status = '"+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                #cursor.execute(sql)
                #db.commit()  
                #sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                #cursor.execute(sql)
                #db.commit()      

        if main == 'get_user':             
            if status == '':
                #sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
                param =  {"task_type_id": 3,"data": {"loms": ["TbA9Bd1vxF4", "SfYaAQ9-RnE"]},"priority": 4,"fields": ["."]}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer)
                print ("[+] answer",answer.json() )
                data  = answer.json()
                #data = json.loads(answer.json()) # string to json
                answer_id = data["task_id"]            
                sql = "UPDATE vk_task set status = 'Ожидание: "+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                cursor.execute(sql)
                db.commit()  
                sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                cursor.execute(sql)
                db.commit()
            else:
                id_status = status.replace('Ожидание: ','')
                print ('[+] id_status',id_status)
                param = {"command":"status","id":int(id_status)}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer.json() )                
                #answer_id = answer.json()['task']['id']            
                #sql = "UPDATE vk_task set status = '"+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                #cursor.execute(sql)
                #db.commit()  
                #sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                #cursor.execute(sql)
                #db.commit()        

        if main == 'get_bvcs_user':             
            if status == '':
                #sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
                param =  {"task_type_id": 3,"data": {"loms": ["TbA9Bd1vxF4", "SfYaAQ9-RnE"]},"priority": 4,"fields": ["."]}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer)
                print ("[+] answer",answer.json() )
                data  = answer.json()
                #data = json.loads(answer.json()) # string to json
                answer_id = data["task_id"]            
                sql = "UPDATE vk_task set status = 'Ожидание: "+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                cursor.execute(sql)
                db.commit()  
                sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                cursor.execute(sql)
                db.commit()
            else:
                id_status = status.replace('Ожидание: ','')
                print ('[+] id_status',id_status)
                param = {"command":"status","id":int(id_status)}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer.json() )                
                #answer_id = answer.json()['task']['id']            
                #sql = "UPDATE vk_task set status = '"+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                #cursor.execute(sql)
                #db.commit()  
                #sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                #cursor.execute(sql)
                #db.commit()        

        if main == 'get_bvcs_user':             
            if status == '':
                #sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
                param =  {"task_type_id": 3,"data": {"loms": ["TbA9Bd1vxF4", "SfYaAQ9-RnE"]},"priority": 4,"fields": ["."]}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer)
                print ("[+] answer",answer.json() )
                data  = answer.json()
                #data = json.loads(answer.json()) # string to json
                answer_id = data["task_id"]            
                sql = "UPDATE vk_task set status = 'Ожидание: "+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                cursor.execute(sql)
                db.commit()  
                sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                cursor.execute(sql)
                db.commit()
            else:
                id_status = status.replace('Ожидание: ','')
                print ('[+] id_status',id_status)
                param = {"command":"status","id":int(id_status)}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer.json() )                
                #answer_id = answer.json()['task']['id']            
                #sql = "UPDATE vk_task set status = '"+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                #cursor.execute(sql)
                #db.commit()  
                #sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                #cursor.execute(sql)
                #db.commit()        

        if main == 'get_vcs_video':             
            if status == '':
                #sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
                param =  {"task_type_id": 3,"data": {"loms": ["TbA9Bd1vxF4", "SfYaAQ9-RnE"]},"priority": 4,"fields": ["."]}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer)
                print ("[+] answer",answer.json() )
                data  = answer.json()
                #data = json.loads(answer.json()) # string to json
                answer_id = data["task_id"]            
                sql = "UPDATE vk_task set status = 'Ожидание: "+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                cursor.execute(sql)
                db.commit()  
                sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                cursor.execute(sql)
                db.commit()
            else:
                id_status = status.replace('Ожидание: ','')
                print ('[+] id_status',id_status)
                param = {"command":"status","id":int(id_status)}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer.json() )                
                #answer_id = answer.json()['task']['id']            
                #sql = "UPDATE vk_task set status = '"+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                #cursor.execute(sql)
                #db.commit()  
                #sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                #cursor.execute(sql)
                #db.commit()        

        if main == 'get_vcs_playlist':             
            if status == '':
                #sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
                param =  {"task_type_id": 3,"data": {"loms": ["TbA9Bd1vxF4", "SfYaAQ9-RnE"]},"priority": 4,"fields": ["."]}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer)
                print ("[+] answer",answer.json() )
                data  = answer.json()
                #data = json.loads(answer.json()) # string to json
                answer_id = data["task_id"]            
                sql = "UPDATE vk_task set status = 'Ожидание: "+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                cursor.execute(sql)
                db.commit()  
                sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                cursor.execute(sql)
                db.commit()
            else:
                id_status = status.replace('Ожидание: ','')
                print ('[+] id_status',id_status)
                param = {"command":"status","id":int(id_status)}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer.json() )                
                #answer_id = answer.json()['task']['id']            
                #sql = "UPDATE vk_task set status = '"+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                #cursor.execute(sql)
                #db.commit()  
                #sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                #cursor.execute(sql)
                #db.commit()        

        if main == 'get_comment_user':             
            if status == '':
                #sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
                param =  {"task_type_id": 3,"data": {"loms": ["TbA9Bd1vxF4", "SfYaAQ9-RnE"]},"priority": 4,"fields": ["."]}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer)
                print ("[+] answer",answer.json() )
                data  = answer.json()
                #data = json.loads(answer.json()) # string to json
                answer_id = data["task_id"]            
                sql = "UPDATE vk_task set status = 'Ожидание: "+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                cursor.execute(sql)
                db.commit()  
                sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                cursor.execute(sql)
                db.commit()
            else:
                id_status = status.replace('Ожидание: ','')
                print ('[+] id_status',id_status)
                param = {"command":"status","id":int(id_status)}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer.json() )                
                #answer_id = answer.json()['task']['id']            
                #sql = "UPDATE vk_task set status = '"+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                #cursor.execute(sql)
                #db.commit()  
                #sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                #cursor.execute(sql)
                #db.commit()        

        if main == 'get_video_user':             
            if status == '':
                #sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
                param =  {"task_type_id": 3,"data": {"loms": ["TbA9Bd1vxF4", "SfYaAQ9-RnE"]},"priority": 4,"fields": ["."]}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer)
                print ("[+] answer",answer.json() )
                data  = answer.json()
                #data = json.loads(answer.json()) # string to json
                answer_id = data["task_id"]            
                sql = "UPDATE vk_task set status = 'Ожидание: "+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                cursor.execute(sql)
                db.commit()  
                sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                cursor.execute(sql)
                db.commit()
            else:
                id_status = status.replace('Ожидание: ','')
                print ('[+] id_status',id_status)
                param = {"command":"status","id":int(id_status)}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://85.193.84.122:5000/api/task/', data=data,headers=headers)
                print ("[+] answer",answer.json() )                              

if options.menu == '16':
    import colorama
    import random
    import iz_func
    import json
    import requests
    import time
    colorama.init(autoreset=True)
    print(colorama.Fore.MAGENTA  + '    [+] Собираю пользователей из города') 
    print (colorama.Fore.MAGENTA + '    [+] Время старта программы:',int(time.time()))
    namebot = 'master'
    #namebot = 'ДНР'
    #namebot = 'ЛНР'
    task = get_task (namebot)
    for row in task:
        id_task,name_task,offset_task,data_task = row.values() 
        token = get_token (["random"])
        print ('    [+] Пользователь: ',token[1])    
        print ('    [+] offset_task:  ',offset_task)
        birth_day     = json.loads(offset_task)['birth_day']
        birth_month   = json.loads(offset_task)['birth_month']
        limit  = 1000
        birth_day = birth_day + 1
        if birth_day > 31:
            birth_month = birth_month + 1
            birth_day = 1
        if birth_month < 13:
            url = 'https://api.vk.com/method/users.search?access_token='+str(token[2])+'&count='+str(limit)+'&hometown='+str(data_task)+'&v=5.131&offset='+str(0)+''
            url = url + '&fields=about,activities,bdate,blacklisted,blacklisted_by_me,books,can_post,can_see_all_posts,can_see_audio,can_send_friend_request,can_write_private_message,career,city,common_count,conections,contacts,country,crop_photo,domain,education,exports,followers_count,friend_status,games,has_mobile,has_photo,home_town,interests,is_favorite,is_friend,•is_hidden_from_feed,last_seen,lists,maiden_name,military,movies,music,nickname,occupation,online,personal,photo_100,photo_200,photo_200_orig,photo_400_orig,photo_50,photo_id,photo_max.photo_max_orig,quotes,relation,relatives,schools,screen_name,sex,site,status,timezone,tv,universities,verified,wall_comments'
            url = url + '&birth_day='+str(birth_day)+'&birth_month='+str(birth_month)+''
            response = requests.get(url)
            parsed_string = response.json()
            response = parsed_string['response']        
            count = response ['count']
            items = response ['items']
            save_full_user (items,id_task)                    
            offset = '{"birth_day":'+str(birth_day)+',"birth_month":'+str(birth_month)+'}'
            db,cursor = connect ()
            sql = "UPDATE vk_task SET `offset` = '"+str(offset)+"' WHERE `id` = "+str(id_task)+""
            cursor.execute(sql) 
            sql = "SELECT COUNT(*) FROM vk_get_full_user where task_id = "+str(id_task)+""
            cursor.execute(sql) 
            results = cursor.fetchall()[0]
            summ = results['COUNT(*)']
            report = '{"all":'+str(count)+',"base":'+str(summ)+'}'
            sql = "UPDATE vk_task SET `report` = '"+str(report)+"' WHERE `id` = "+str(id_task)+""
            cursor.execute(sql) 
            print ('[count]',count)            
            db.commit()            
        else:
            print ('[-]')        
        
if options.menu == '15':
    import iz_func
    import json
    import time
    import json
    import requests
    print ('[+] Выполнение задачи по проекту Инста')
    db,cursor = iz_func.connect ()
    sql = "select id,name,dataT,status from vk_task where (status_task = '' or status_task = 'Ожидание' or status_task = 'В работе') and user_id = 'Insta' "
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        task_id,name,dataT,status = rec.values()   
        dataT = iz_func.change_back (dataT)
        dataT = dataT.replace("'",'"')
        dataT = dataT.replace('"{','{')
        dataT = dataT.replace('}"','}')
        b = json.loads(dataT)
        data = b['data']
        print ('    [+] data:',data) 
        try:
            list_data = data['user_id']
        except Exception as e:    
            list_data = ''
            #print ('[+] Ощибка в строке ',task_id)
            #print ('[+] ',dataT)
            #exit (0)
        main = data['main']    
        sql = "UPDATE vk_task SET status_task = 'Стартанул' WHERE id = "+str(task_id)+" "
        cursor.execute(sql)
        db.commit()
        
        if main == 'follower':
            print ('    [+] Начинаем парсить пользователей из группы')
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
            #parser_save_answer (sql,task_id)  
            
            
        if main == 'get_info_user':
            import requests
            import json
            print ('    [+] Начинаем парсить друзей')
            if status == '':
                #sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
                param =  {"command":"register","items":["navalny"],"task_id":3}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('https://api-hype.uzavr.ru/api/interaction', data=data,headers=headers)
                print ("[+] answer",answer.json() )
                print (type (answer.json()))
                data = json.loads(answer.json()) # string to json
                answer_id = data["navalny"]            
                sql = "UPDATE vk_task set status = 'Ожидание: "+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                cursor.execute(sql)
                db.commit()  
                sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                cursor.execute(sql)
                db.commit()
            else:
                id_status = status.replace('Ожидание: ','')
                print ('[+] id_status',id_status)
                param = {"command":"status","id":int(id_status)}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('https://api-hype.uzavr.ru/api/interaction', data=data,headers=headers)
                print ("[+] answer",answer.json() )                
                #answer_id = answer.json()['task']['id']            
                #sql = "UPDATE vk_task set status = '"+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                #cursor.execute(sql)
                #db.commit()  
                sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                cursor.execute(sql)
                db.commit()
            
            
            
            #exit (0)
            
            #https://g.uzavr.ru/parsers/facebook-subscribers-anton
            #http://94.26.227.250:8018/QWERTY/task/14
            #http://94.26.227.250:8018/QWERTY/task/14


        if main == 'comment_like':
            print ('    [+] Начинаем парсить пользователей из группы')
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
            #parser_save_answer (sql,task_id)  
            


        if main == 'user_details':
            print ('    [+] Начинаем парсить пользователей из группы')   
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
            #parser_save_answer (sql,task_id)  
            

        if main == 'post':
            print ('    [+] Начинаем парсить пользователей из группы')             
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""

if options.menu == '14':  ### FB
    import iz_func
    import json
    import time
    import json
    import requests
    print ('[+] Выполнение задачи по проекту FB')
    db,cursor = iz_func.connect ()
    sql = "select id,name,dataT,status from vk_task where (status_task = '' or status_task = 'Ожидание' or status_task = 'В работе') and user_id = 'FB' "
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        task_id,name,dataT,status = rec.values()   
        dataT = iz_func.change_back (dataT)
        dataT = dataT.replace("'",'"')
        dataT = dataT.replace('"{','{')
        dataT = dataT.replace('}"','}')
        b = json.loads(dataT)
        data = b['data']
        print ('    [+] data:',data) 
        try:
            list_data = data['user_id']
        except Exception as e:    
            list_data = ''
            #print ('[+] Ощибка в строке ',task_id)
            #print ('[+] ',dataT)
            #exit (0)
        main = data['main']    
        sql = "UPDATE vk_task SET status_task = 'Стартанул' WHERE id = "+str(task_id)+" "
        cursor.execute(sql)
        db.commit()
        
        if main == 'follower':
            print ('    [+] Начинаем парсить пользователей из группы')
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
            #parser_save_answer (sql,task_id)  
            
            
        if main == 'friend':
            import requests
            import json
            print ('    [+] Начинаем парсить друзей')
            if status == '':
                #sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
                param = {"data": {"items": ["www.adme.ru"]},"priority": 1,"fields": [],"parsing_type": "comment_like"}
                data = json.dumps(param)
                headers = {"Content-Type": "application/json"}
                answer = requests.post('http://94.26.227.250:8018/QWERTY/task', data=data,headers=headers)
                print ("[+] answer",answer.json() )
                answer_id = answer.json()['task']['id']            
                sql = "UPDATE vk_task set status = 'Ожидание: "+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                cursor.execute(sql)
                db.commit()  
                sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                cursor.execute(sql)
                db.commit()
            else:
                #param = {"data": {"items": ["www.adme.ru"]},"priority": 1,"fields": [],"parsing_type": "comment_like"}
                #data = json.dumps(param)
                #headers = {"Content-Type": "application/json"}
                url = 'http://94.26.227.250:8018/QWERTY/task/'+str(status).replace('Ожидание: ','')
                answer = requests.get(url)
                print ("[+] answer",answer.json() )                
                #answer_id = answer.json()['task']['id']            
                #sql = "UPDATE vk_task set status = '"+str(answer_id)+"' where id = '"+str(task_id)+"'" 
                #cursor.execute(sql)
                #db.commit()  
                sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
                cursor.execute(sql)
                db.commit()
            
            
            
            #exit (0)
            
            #https://g.uzavr.ru/parsers/facebook-subscribers-anton
            #http://94.26.227.250:8018/QWERTY/task/14
            #http://94.26.227.250:8018/QWERTY/task/14


        if main == 'comment_like':
            print ('    [+] Начинаем парсить пользователей из группы')
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
            #parser_save_answer (sql,task_id)  
            


        if main == 'user_details':
            print ('    [+] Начинаем парсить пользователей из группы')   
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
            #parser_save_answer (sql,task_id)  
            

        if main == 'post':
            print ('    [+] Начинаем парсить пользователей из группы')             
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""            
            
if options.menu == '13':
    import iz_func
    import json
    import time
    import json
    import requests
    print ('[+] Получение списка новостей группы и комментарий')
    import pymysql
    
    #db,cursor = iz_func.connect () 
    
    db_save = pymysql.connect(host='localhost',
                        user='izofen',
                        password='Podkjf3141!',
                        database='site_rus',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
    cursor_save = db_save.cursor() 
     
    sql = "select id,name from vk_grup where 1=1 ORDER BY id DESC limit 100000"
    cursor_save.execute(sql)
    data = cursor_save.fetchall()
    for rec in data:
        group_id,name = rec.values() 
        print ('[+] id,name:',group_id,name)
        list_news = parser_get_news_in_group (group_id,news_limit)
        for new in list_news:
            list_сomments = parser_get_сomments_in_group (group_id,new['id'])
            #print ("[+] list_сomments:",list_сomments)  
            for сomment in list_сomments:
                #print ('[+]---------------------------------[+]',сomment)
                avtor_owner_id      = group_id
                avtor_post_id       = new['id']
                comment_from_id     = сomment ['from_id']
                comment_id          = сomment ['id']
                try:
                    comment_post_id     = сomment ['post_id']
                except Exception as e:
                    comment_post_id     = 0
                comment_text        = сomment ['text']
                save_comment_to_base (avtor_owner_id,avtor_post_id,comment_from_id,comment_id,comment_post_id,comment_text)    

if options.menu == '12':   # VK
    import iz_func
    import json
    import time
    import json
    import requests
    import iz_telegram
    print ('[+] Выполнение задачи по проекту')
    send_admin_message ('@parser3141_bot','Проверка задания')
    db,cursor = iz_func.connect ()
    sql = "select id,name,dataT from vk_task where (status_task = '' or status_task = 'Ожидание') and user_id = 'VK' "
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        task_id,name,dataT = rec.values()  
        print ('    [+] Задание  :',task_id)
        print ('    [+] Данные   :',dataT)
        dataT = iz_func.change_back (dataT)
        dataT = dataT.replace("'",'"')
        dataT = dataT.replace('"{','{')
        dataT = dataT.replace('}"','}')
        
        if 1==1:
                    
            try:
                b = json.loads(dataT)
                data = b['data']
            except Exception as e:    
                data = []
                print ('dataT',dataT)
        
            try:
                list_data = data['user_id']
            except Exception as e:    
                list_data = ''

            try:    
                detail = data['detail']    
            except Exception as e:    
                detail = 'no'
                        
            try:    
                main = data['main']  
            except Exception as e:           
                main = ''
                
            try:    
                news_limit = data['news']  
            except Exception as e:           
                news_limit = 10    
                

            print ('    [+] Детализация:',detail)
            print ('    [+] limit:',news_limit)

            sql = "UPDATE vk_task SET status_task = 'В работе' WHERE id = "+str(task_id)+" "
            cursor.execute(sql)
            db.commit()
              
        if main == 'full_info_post' or main == 'full_info_post_e':
            send_admin_message ('@parser3141_bot','Старт задания full_info_post')
            print ('    [+] Получаем полную информацию о новости')
            list_posts = parser_get_list_post (list_data)
            
            print ('    [+] Список id групп переданные по списку',list_posts)
            clear_task (task_id)
            for post in list_posts:
                print ('        [+] Обрабатываемая post:',post)                 
                list_info = iz_telegram.load_setting ('@parser3141_bot','full_info_post_Data_big')                 
                info_news,post_id,owner_id  = parser_get_info_news (post,100,list_info)                          ####  Выбираем пользователей из группы                
                #parser_save_news_in_base (info_news,task_id,list_info)                                
                list_commens  = parser_get_commers_news (info_news,post_id,owner_id)
                #print ('[list_commens]',list_commens)
                parser_save_сomments_in_base (list_commens,task_id,post)                                             
                list_likes  = parser_get_likes_news (info_news,post_id,owner_id)                              
                parser_save_likes_in_base  (list_likes,task_id,post)                              
            sql  = ''
            parser_save_answer (sql,task_id)
            send_admin_message ('@parser3141_bot','Стоп задания full_info_post')
            
        if main == 'get_info_user':
            print ('    [+] Информация о пользователе')
            clear_task (task_id) 
            send_admin_message ('@parser3141_bot','Старт задания get_info_user')                   ## Начало операции
            list_info = iz_telegram.load_setting ('@parser3141_bot','get_info_user_Data_big')      ## Зпполнение ответа
            print ('    [+] Начинаем парсить информацию о пользователе')            
            list_user = parser_get_list_user (list_data,list_info)
            print ('    [+] Результат ответа :',list_user)
            parser_active_user_in_base (list_user,task_id,detail,list_user,list_info)
            sql  = ""
            parser_save_answer (sql,task_id)
            send_admin_message ('@parser3141_bot','Стоп задания get_info_user')
         
        if main == 'get_user_in_group':
            print ('    [+] Начинаем парсить пользователей из группы')
            list_group = parser_get_list_group (list_data)
            #print ('    [+] Список id групп переданные по списку',list_group)
            for group in list_group:
                print ('        [+] Обрабатываемая группа:',group['name'])                                                             
                list_user = parser_get_user_in_group (group['id'])                          ####  Выбираем пользователей из группы
                #print ('        [+] Список спарсенных пользователей:',list_user) 
                parser_save_user_in_base (list_user,task_id,detail,'new',group['id'],list_info)
            sql  = ""
            parser_save_answer (sql,task_id)
          
        if main == 'get_subscribers_in_user':
            print ('    [+] Начинаем парсить подписчиков у пользователя')
            clear_task (task_id) 
            send_admin_message ('@parser3141_bot','Старт задания get_subscribers_in_user') 
            list_user = parser_get_list_user (list_data,'')  
            list_info = iz_telegram.load_setting ('@parser3141_bot','get_subscribers_in_user_Data_big')            
            for user in list_user:
                print ('        [+] Обрабатываемая пользователь:',user)                                                          
                list_users = parser_get_followers_in_user (user['id'],detail)
                print ('        [+] Список спарсенных пользователей:',list_user)
                parser_save_user_in_base (list_users,task_id,detail,'new',user['id'],list_info)                
            #sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
            parser_save_answer ('',task_id)
        
        if main == 'get_only_friend_in_user':        
            print ('    [+] Начинаем парсить друзей у пользователя')
            list_user = parser_get_list_user (list_data,'')            
            #print ('    [+] Список id пользователей переданные по списку',list_user)
            k = 0
            for user in list_user:
                k = k + 1
                print ('        [+] Обрабатываемая пользователь:',user)                                                          
                list_users = parser_get_friend_in_user (user['id'],detail)
                if k == 1:
                    parser_save_user_in_base (list_users,task_id,detail,'new',user['id'])
                else:    
                    parser_save_user_in_base (list_users,task_id,detail,'old',user['id'])
                print ('        [+] Список спарсенных пользователей:',list_user)
            sql  = ""
            parser_save_answer (sql,task_id)
            
        if main == 'get_friend_in_user':        
            print ('    [+] Начинаем парсить друзей у пользователя')
            clear_task (task_id)            
            send_admin_message ('@parser3141_bot','Старт задания get_friend_in_user')             
            list_user = parser_get_list_user (list_data,'')
            list_info = iz_telegram.load_setting ('@parser3141_bot','get_friend_in_user_Data_big')            
            #k = 0
            for user in list_user:
                print ('        [+] Обрабатываемая пользователь:',user)                                                          
                list_users = parser_get_followers_in_user (user['id'],detail)
                parser_save_user_in_base (list_users,task_id,detail,'new',user['id'],list_info)
                list_users = parser_get_friend_in_user (user['id'],detail)
                #print ('        [+] Список спарсенных пользователей:',list_user)
                parser_save_user_in_base (list_users,task_id,detail,'old',user['id'],list_info)
            sql  = ""
            parser_save_answer (sql,task_id)
            
        if main == 'get_followers_in_user':        
            print ('    [+] Начинаем парсить подписчиков у пользователя')
            list_user = parser_get_list_user (list_data,'')            
            #print ('    [+] Список id пользователей переданные по списку',list_user)
            k = 0
            for user in list_user:
                k = k + 1
                print ('        [+] Обрабатываемая пользователь:',user)                                                          
                list_users = parser_get_followers_in_user (user['id'],detail)
                
                if k == 1:
                    list_info = ''
                    parser_save_user_in_base (list_users,task_id,detail,'new',user['id'],list_info)
                else:    
                    list_info = ''
                    parser_save_user_in_base (list_users,task_id,detail,'old',user['id'],list_info)
                    
                    
                    
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
            parser_save_answer (sql,task_id)            
                     
        if main == 'get_group_in_user': 
            print ('    [+] Начинаем парсить группы у пользователя')  
            list_user = parser_get_list_user (list_data,'')  
            #print ('    [+] Список id пользователей переданные по списку',list_user)
            for user in list_user:
                print ('        [+] Обрабатываемая пользователь:',user)
                list_group = parser_get_group_in_user (user['id'],detail)
                #print ('        [+] Список спарсенных групп:',list_group)  
                parser_save_group_in_base (list_group,task_id,detail,user['id']) 
            sql  = ""
            parser_save_answer (sql,task_id)                
            
        if main == 'get_news_in_group':
            print ('    [+] Начинаем парсить новости у группы')
            clear_task (task_id) 
            list_info = iz_telegram.load_setting ('@parser3141_bot','get_news_in_group_Data_big')
            list_group = parser_get_list_group (list_data)
            for group in list_group:
                print ('        [+] Обрабатываемая группа:',group) 
                list_news = parser_get_news_in_group (group['id'],news_limit)   
                print ('        [+] Список спарсенных новостей:',list_news)   
                #list_info = 'data,id'
                parser_save_news_in_base (list_news,task_id,list_info)
            sql  = ""    #### select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+"
            parser_save_answer (sql,task_id) 
            
        if main == 'get_news_in_post' or main == 'get_posts_by_group':
            print ('    [+] Начинаем парсить новости по посту')
            list_grup = parser_get_list_post  (data['user_id'])
            print ('    [+] Список id пользователей переданные по списку',list_grup)
            for grup in list_grup:
                print ('        [+] Обрабатываемая пользователь:',grup)
                grup_id = parser_get_list_group (grup)[0]
                print ('[+] grup_id',grup_id)
                list_news = parser_get_news_in_group (grup_id['id'],list_news)
                print ('        [+] Список спарсенных новостей:',list_news) 
                parser_save_news_in_base (list_news,task_id,'')   
            sql  = ""
            parser_save_answer (sql,task_id)     
               
        if main == 'get_news_in_user' or main == 'get_posts_by_user' :
            print ('    [+] Начинаем парсить новости пользователя')
            clear_task (task_id)
            list_info = iz_telegram.load_setting ('@parser3141_bot','get_news_in_user_Data_big')
            list_user = parser_get_list_user (data['user_id'],'')
            print ('    [+] Список id пользователей переданные по списку',list_user)
            
            
            
            for user in list_user:
                print ('        [+] Обрабатываемая пользователь:',user)
                #list_info = ''
                list_news = parser_get_news_in_user (user['id'],list_info)
                print ('        [+] Список спарсенных новостей:',list_news) 
                #list_info = ''
                parser_save_news_in_base (list_news,task_id,list_info)   
            sql  = ""
            parser_save_answer (sql,task_id)     
   
        if main == 'get_сomments_in_user':
            print ('    [+] Начинаем парсить коментария у пользователя')
            list_user = parser_get_list_user (data['user_id'],'')
            print ('    [+] Список id пользователей переданные по списку',list_user)
            for user in list_user:
                print ('        [+] Обрабатываемая пользователь:',user)
                list_news = parser_get_news_in_user (user['id'])
                print ('        [+] Список спарсенных новостей:',list_news) 
                for new in list_news:
                    list_сomments = parser_get_сomments_in_user (user['id'],new['id'])
                    parser_save_сomments_in_base (list_сomments,task_id)   

            #sql = "select id,name from vk_answer where task_id =  "+str(task_id)+";"                
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
            parser_save_answer (sql,task_id)                             

        if main == 'get_сomments_in_group':
            print ('    [+] Начинаем парсить коментария у группы')
            list_group = parser_get_list_group (list_data)
            #print ('    [+] Список id групп переданные по списку',list_group)
            for group in list_group:
                print ('        [+] Обрабатываемая группа:',group)   
                list_news = parser_get_news_in_group (group['id'],list_news)
                for new in list_news:
                    print ('    [+] Обрабатываем группу:',new) 
                    list_сomments = parser_get_сomments_in_group (group['id'],new['id'])
                    parser_save_сomments_in_base (list_сomments,task_id)   

            #sql = "select id,name from vk_answer where task_id =  "+str(task_id)+";"                
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
            parser_save_answer (sql,task_id)                             
                
        if main == 'get_like_in_group':
            print ('    [+] Начинаем парсить нравится у группы')
            list_group = parser_get_list_group (list_data)
            #print ('    [+] Список id групп переданные по списку',list_group)
            for group in list_group:
                print ('        [+] Обрабатываемая группа:',group['name'])   
                list_news = parser_get_news_in_group (group['id'],news_limit)
                for new in list_news:
                    #print ('            [+] Обрабатываем новость:',new['text'][0:140]) 
                    list_like = parser_get_likes_in_group (group['id'],new['id'])
                    list_info = ''
                    parser_save_user_in_base (list_like,task_id,detail,'new',list_info)
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
            print ('[sql]',sql)
            parser_save_answer (sql,task_id)                
                
        if main == 'get_like_in_user':
            print ('    [+] Начинаем парсить нравится у пользователя')
            list_user = parser_get_list_user (data['user_id'],'')
            print ('    [+] Список id пользователей переданные по списку',list_user)
            for user in list_user:
                print ('        [+] Обрабатываемая пользователь:',user)
                list_news = parser_get_news_in_user (user['id'])
                print ('        [+] Список спарсенных новостей:',list_news) 
                for new in list_news:
                    print ('            [+] Обрабатываем новость:',new['text'][0:140])
                    #print ('[+]---------------------------------------------[+]')                     
                    #list_сomments = parser_get_сomments_in_user (user['id'],new['id'])
                    list_like = parser_get_likes_in_user (user['id'],new['id'])
                    list_info = ''
                    parser_save_user_in_base (list_like,task_id,detail,'new',list_info)
                    #parser_save_сomments_in_base (list_сomments,task_id)   

            #sql = "select id,name from vk_answer where task_id =  "+str(task_id)+";"                
            sql  = "select id,data_name,data_id,data_big from vk_answer where task_id = "+str(task_id)+""
            parser_save_answer (sql,task_id)              
              
        if main == '':        
            pass
            #sql = "select * from vk_user where 1=1 limit 10;"
            #sql = iz_func.change (sql)
            #sql = "UPDATE vk_task SET answer = '"+sql+"' WHERE id = "+str(task_id)+" "
            #cursor.execute(sql)
            
    send_admin_message ('@parser3141_bot','Задания выполнены')  
    iz_pause (300)    
    
if options.menu == '11':
    import iz_func
    print ('[+] Загрузка ключей в базу данных')
    db,cursor = iz_func.connect ( )
    f = open('list_token.txt','r')
    for line in f:  
        n  = line.find(' ')
        line = line[n:]
        line = line.strip()
        n  = line.find(' ')
        line = line[:n]
        print ('[-]'+line)
        id = 0;
        sql = "select id,name from vk_accound where token = '"+str(line)+"' limit 1"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data:
            id,name = rec.values() 
        if id == 0:
            sql = "INSERT INTO vk_accound (`first_name`,`from`,`last_name`,`name`,`status`,`token`,`user_id`) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format ('','inet','','','',line,'')
            cursor.execute(sql)
            db.commit()

if options.menu == '10':
    print ("[+] Всупляем в группу аккаунтё")
    import random
    import iz_func
    import json
    import requests
    import time
    print ('unixtime:',int(time.time()))
    
    token = 'a78057dff8e61dfe41aa76b375c284506737f675a5ac7a211326cd9b3a498dbac445bbbe7e69dc95a419c'
    token = '6f324045278e6d668bc8a01c5557e6a1046c6a4f7b0809083bc03caca33c21bc60903867189223b3eb5c0'
    url = ""  
    url = url + "https://api.vk.com/method/groups.get?access_token="+str(token)+"&extended=0&v=5.131"
    response = requests.get(url)
    parsed_string = response.json()
        
        
    import pymysql
    db = pymysql.connect(host='localhost',
                            user='izofen',
                            password='Podkjf3141!',
                            database='site_rus',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()     
    sql = "select id,name from vk_grup where description like '% python %' ORDER BY id limit 100;"   ### "   ### ORDER BY id DESC
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name = rec.values()
        print ('[+]id,name',id,name)      
        url = ""  
        url = url + "https://api.vk.com/method/groups.join"
        url = url + "?access_token="+str(token)+""
        url = url + "&group_id="+str(id)
        url = url + "&v=5.131"
        response = requests.get(url)
        parsed_string = response.json()
        print ('Пауза')
        time.sleep (10*60)
     
if options.menu == '9':
    import requests
    print ("[+] Публикую фотографию на стене")
    token = '6f324045278e6d668bc8a01c5557e6a1046c6a4f7b0809083bc03caca33c21bc60903867189223b3eb5c0'
    v     = '5.131'
    url = "https://api.vk.com/method/account.getProfileInfo";
    data={'access_token':token,'v':v}
    response = requests.post(url,data=data)
    parsed_string = response.json()
    print ('[+] parsed_string',parsed_string)
   
    #exit (0)
    
    url = "https://api.vk.com/method/photos.getWallUploadServer?access_token=6f324045278e6d668bc8a01c5557e6a1046c6a4f7b0809083bc03caca33c21bc60903867189223b3eb5c0&v=5.131";
    response = requests.get(url)
    parsed_string = response.json()
    print ('[+] parsed_string',parsed_string)

    url = parsed_string['response']['upload_url']
    
    files = {'photo': open('3dot14_000000415.jpg', 'rb')}
    response = requests.post(url, files=files)
    parsed_string = response.json()
    print ('[+] parsed_string',parsed_string)
    
    hash    = parsed_string['hash']
    server  = parsed_string['server']
    photo   = parsed_string['photo']
    
    print ('[+] hash:',hash)
    print ('[+] server:',server)
    print ('[+] photo:',photo)    

    url = "https://api.vk.com/method/photos.saveWallPhoto";
    #url = url + "&server="+str(server)
    #url = url + "&hash="+str(hash)
    #url = url + "&photo="+str(photo)
    
    token = '6f324045278e6d668bc8a01c5557e6a1046c6a4f7b0809083bc03caca33c21bc60903867189223b3eb5c0'
    v     = '5.131'
    data={'access_token':token,'v':v,'hash':hash,'server':server,'photo':photo}
    #response = requests.post(url,data=data)
    #parsed_string = response.json()
    #print ('[+] parsed_string',parsed_string)  
    response = requests.post(url,data=data)
    parsed_string = response.json()
    print ('[+] parsed_string',parsed_string)
    
    print ('')
    print ('')
    print ('')
    print ('[+]',url)
    
    "photo24709387_457269528"
          
if options.menu == '8': 
    import datetime
    token = iz_vk.get_token (3)[0][2]
    now = datetime.datetime.now()
    sl = str(now.day) + '.' + str(now.month)+'%'
    print ("[+] Текущий месяц:",now.month)
    print ("[+] Текущий день: ",now.day)   
    print ('[+] Получаем данные ДР:',sl)
    bithday = str(sl)
    start_bithday (bithday,token)       

if options.menu == '7':
    import colorama
    colorama.init(autoreset=True)
    print(colorama.Fore.MAGENTA  + '    [+] Собираю друзей у пользователей. В 2.11')  
    #print ("[+] Собираю друзей у пользователей. В 2.11")
    token = get_token (['random'])
    import random
    import iz_func
    import json
    import requests
    import time
    print ('unixtime:',int(time.time()))
    import pymysql
    db = pymysql.connect(host='localhost',
                            user='izofen',
                            password='Podkjf3141!',
                            database='site_rus',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()     
    sql = "select id,first_name,last_name from vk_user where friend = 0  limit 1000;"   ### "   ### ORDER BY id DESC
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        user_id,first_name,last_name = rec.values()      
        unixtime = int(time.time ())
        sql = "UPDATE vk_user SET friend = "+str(unixtime) + " where id = "+str(user_id)+""
        cursor.execute(sql) 
        db.commit()        
        print ("[+] Читаем данные клиента:",user_id,first_name,last_name)  
        count  = 0
        offset = 0   
        nm     = 0
        count_list = 1000
        while offset <= count:
            token = get_token (['random'])
            url = 'https://api.vk.com/method/friends.get?access_token='+str(token[2])+'&user_id='+str(user_id)+'&fields=nickname,site,bdate,sex&v=5.131&offset='+str(offset)+'&count=1000'
            response = requests.get(url)
            parsed_string = response.json()
            try:
                response = parsed_string['response']
                #print (response)
            except Exception as e:
                print (colorama.Fore.YELLOW+'parsed_string: '+str(parsed_string))
                unixtime = int(time.time ())
                sql = "UPDATE vk_user SET friend = "+str(unixtime) + " where id = "+str(user_id)+""
                cursor.execute(sql) 
                db.commit()   
                break   
            count = response ['count']
            items = response ['items']
            #print ('    [+] Всего записей:',count,'смещение:',offset)
            offset = offset + count_list        
            #for line in items:
            for line in items:
                id_user,first_name,last_name,can_access_closed,is_closed,bdate,country_id,country_title,city_id,city_title,status,site,sex = parser_user (line)      
                #print (first_name,last_name,'('+str()+')')
                id_code = 0
                sql = "select id,first_name,last_name,site from vk_user where id = "+str(id_user)+" limit 1;"   ### 
                cursor.execute(sql)
                data = cursor.fetchall()
                first_name2 = ''
                last_name2  = '' 
                site2       = ''              
                for row in data: 
                    id_code,first_name2,last_name2,site2 = row.values()      
                print ('    [+]',id_code,first_name,last_name,'    -    ',first_name2,last_name2,'-------',bdate,site)  
                if id_code == 0:   
                    unixtime = int(time.time ())
                    try:
                        #sql = "INSERT INTO vk_user (id,`bdate`,`can_access_closed`,`city_id`,`city_title`,`country`,`deactivated`,`first_name`,`is_closed`,`last_name`,`sex`,`site`,`unixtime`) VALUES ("+str(id_user)+",'"+str(bdate)+"',"+str(0)+","+str(city_id)+",'"+str(city_title)+"',"+str(country_id)+",'','"+str(first_name)+"',"+str(0)+",'"+str(last_name)+"',"+str(sex)+",'"+str(site)+"',"+str(unixtime)+")".format ()
                        print ('        [+] Данные по пользователю записаны') 
                        #cursor.execute(sql)
                        #db.commit()


                        sql = "INSERT INTO vk_user (id,`bdate`,`can_access_closed`,`city_id`,`city_title`,`country`,`deactivated`,`first_name`,`is_closed`,`last_name`,`sex`,`site`,`unixtime`,unixtime_update) VALUES ("+str(id_user)+",'"+str(bdate)+"',"+str(0)+","+str(city_id)+",'"+str(city_title)+"',"+str(country_id)+",'','"+str(first_name)+"',"+str(0)+",'"+str(last_name)+"',"+str(sex)+",'"+str(site)+"',"+str(unixtime)+",0)".format ()
                        cursor.execute(sql)
                        db.commit()



                        info_grup = 'Записан'
                    except Exception as e:
                        print ('[+] Ошибка записи 2:',e)
                        info_grup = 'Ошибка'                
            print ('[+] Пауза между запросами',count,offset) 
            iz_pause (10)
        print ('[+] Пауза между клиентами')
        iz_pause (30)        
        
if options.menu == '6':
    import colorama
    colorama.init(autoreset=True)
    print(colorama.Fore.MAGENTA  + '    [+] Собираю группы у пользователей')  
    token = get_token (["random"])
    print ('    [+] Пользователь: ',token[1])    
    import random
    import iz_func
    import json
    import requests
    import time
    print (colorama.Fore.MAGENTA  + '    [+] Время старта программы:',int(time.time()))
    import pymysql
    db = pymysql.connect(host='localhost',
                            user='izofen',
                            password='Podkjf3141!',
                            database='site_rus',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()  
    print (colorama.Fore.MAGENTA  + '    [+] Выбираем данные для работы (Пользователи 1000 шт.)')    
    sql = "select id,first_name,last_name from vk_user where grup = 0  limit 1000;"   ### "   ### and unixtime < 1639050802 
    cursor.execute(sql)
    data = cursor.fetchall()
    count_list = 1000
    for rec in data: 
        user_id,first_name,last_name = rec.values()
        print ("        [+] Клиент:",user_id,first_name,last_name)   
        unixtime = int(time.time ())
        sql = "UPDATE vk_user SET grup = "+str(unixtime) + " where id = "+str(user_id)+""
        cursor.execute(sql)
        db.commit()  
        count  = 0
        offset = 0   
        nm     = 0
        while offset <= count:
            ##  members_count
            token = get_token (['random'])
            url = 'https://api.vk.com/method/groups.get?access_token='+str(token[2])+'&user_id='+str(user_id)+'&extended=1&count='+str(count_list)+'&fields=description,members_coun&v=5.131&offset='+str(offset)+''
            response = requests.get(url)
            parsed_string = response.json()
            #print ('[parsed_string]',parsed_string)
            try:
                response = parsed_string['response']
            except Exception as e:
                print (colorama.Fore.YELLOW+'parsed_string: '+str(parsed_string))
                unixtime = int(time.time ())
                #sql = "UPDATE vk_user SET unixtime = "+str(unixtime) + " where id = "+str(user_id)+""
                #cursor.execute(sql)
                #db.commit() 
                break   
            count = response ['count']
            items = response ['items']
            #print ('    [+] Всего записей:',count,'смещение:',offset)
            offset = offset + count_list        
            for line in items:
                nm = nm + 1
                id_grup         = line['id']
                name            = line['name']
                screen_name     = line['screen_name'] 
                try:
                     description     = line['description']
                except Exception as e:
                     description     = ''
                try:
                    members_count   = line['members_count'] 
                except Exception as e:
                    members_count   = 0       
                unixtime = int(time.time ())       
                sql = "select id,name,description from vk_grup where id = "+str(id_grup)+" limit 1;"   ### 
                cursor.execute(sql)
                data = cursor.fetchall()
                id_find = 0
                for row in data: 
                    id_find,name,description = row.values()
                description = iz_func.change (description)
                name = iz_func.change (name)
                info_grup = ''
                if id_find == 0:             
                    try:
                        sql = "INSERT INTO vk_grup (id,`description`,`members_count`,`name`,`screen_name`,`unixtime`) VALUES ("+str(id_grup)+",'"+str('')+"',"+str(0)+",'"+str(name)+"','"+str(screen_name)+"',"+str(unixtime)+")".format ()       
                        cursor.execute(sql)
                        db.commit()
                        lastid = cursor.lastrowid     
                        try:                         
                            sql = "UPDATE vk_grup SET description = '"+str(description)+"' WHERE `id` = '"+str(lastid)+"'"    
                            cursor.execute(sql)
                            db.commit()    
                        except Exception as e:
                            pass
                            print ('[+] sql:',sql)
                            print ('[+] e:',e)
                        info_grup = 'Записан'
                    except Exception as e:
                        print ('[+] sql:',sql)
                        info_grup = 'Ошибка'
                else:
                    info_grup = 'Записана ранее'

                if info_grup == 'Записана ранее':
                    print (colorama.Fore.MAGENTA  + '            [+] '+str(nm)+' группа: '+name+' ('+str(id_grup)+') '+info_grup)
                else:
                    print (colorama.Fore.YELLOW   + '            [+] '+str(nm)+' группа: '+name+' ('+str(id_grup)+') '+info_grup)    
    


        unixtime = int(time.time ())
                   
        iz_pause (30)
    iz_pause (600)
           
if options.menu == '5':
    print ("    [+] Собираю пользователей из группы. ")
    import random
    import iz_func
    import json
    import requests
    import time
    print ('    [+] Текущее время:',int(time.time()))
    token = get_token (["random"])
    print ('    [+] Пользователь: ',token[1])
    import pymysql
    db = pymysql.connect(host='localhost',
                            user='izofen',
                            password='Podkjf3141!',
                            database='site_rus',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()     
    print (colorama.Fore.MAGENTA  + '    [+] Выбираем данные для работы (Группы 100 шт.)')
    sql = "select id,name,description from vk_grup where 1=1 ORDER BY unixtime limit 100;"   ### Берем группы познее даты начало остальным ставим текушее знаение unixtime < 1638344623
    cursor.execute(sql)
    data = cursor.fetchall()
    nm = ''
    count_list = 1000  
    list = []    
    for rec in data: 
        id_grup,name,description = rec.values()
        print ('[+]',id_grup,name)
        unixtime = int(time.time ())            
        sql = "UPDATE vk_grup SET unixtime = '"+str(unixtime)+"'  WHERE `id` = "+str(id_grup)+" "
        cursor.execute(sql)
        db.commit() 
        count  = 0
        offset = 0   
        while offset <= count:
            token = get_token (["random"])
            url = ""
            url = url + "https://api.vk.com/method/groups.getMembers"
            url = url + "?access_token="+token[2]
            url = url + "&group_id="+str(id_grup)
            url = url + "&sort=id_desc"
            url = url + "&count="+str(count_list)
            url = url + "&fields=sex,bdate,city,country,site,status"
            url = url + "&v=5.131"
            url = url + "&offset="+str(offset)
            response = requests.get(url)
            parsed_string = response.json()    
            parsed_string = error_code_test (parsed_string,url,token,"") 
            if parsed_string != '':
                print ('[parsed_string]',parsed_string)
                response = parsed_string['response']
                count = response ['count']
                items = response ['items']
                offset = offset + count_list
                print ('    [+] Всего записей:',count,'смещение:',offset)
                for line in items:
                    first_name          = line['first_name']
                    id_user             = line['id']
                    last_name           = line['last_name']
                    can_access_closed = ''
                    try:
                        can_access_closed   = line['can_access_closed']
                    except Exception as e:
                        can_access_closed = ''                 
                    is_closed = ''
                    try:    
                        is_closed           = line['is_closed']
                    except Exception as e:
                        is_closed = ''              
                    sex                 = line['sex']               
                    bdate = ''
                    try: 
                        bdate               = line['bdate']
                    except Exception as e:
                        bdate = ''                   
                    city = ''
                    city_id = 0
                    city_title = ''
                    try:
                        city                = line['city']
                        city_id             = city['id']
                        city_title          = city['title']
                    except Exception as e:
                        city = ''       
                    country = ''
                    country_id = 0
                    country_title = ""
                    try:
                        country             = line['country']
                        country_id          = country['id']
                        country_title       = country['title']
                    except Exception as e:
                        country = ''    
                    try: 
                        status              = line['status'] 
                    except Exception as e:
                        status = ''  
                    site = ''
                    try:
                        site                = line['site'] 
                    except Exception as e:
                        site = ''                
                    if site != '':      
                        #print ('        [+]',id,first_name,last_name,site)
                        pass
                    id_code = 0

                    #print (colorama.Fore.MAGENTA  + '        [+] Пользователь: '+str(id_user)+' '+str(first_name)+' '+str(last_name)+' '+str(site))

                    sql = "select id,first_name,last_name,site from vk_user where id = "+str(id_user)+" limit 1;"   ### 
                    cursor.execute(sql)
                    data = cursor.fetchall()    
                    for row in data: 
                        id_code,first_name,last_name,site = row.values()      
                    info_grup = ''
                    if id_code == 0:
                        unixtime = int(time.time ())
                        try:
                            sql = "INSERT INTO vk_user (id,`bdate`,`can_access_closed`,`city_id`,`city_title`,`country`,`deactivated`,`first_name`,`is_closed`,`last_name`,`sex`,`site`,`unixtime`,unixtime_update) VALUES ("+str(id_user)+",'"+str(bdate)+"',"+str(0)+","+str(city_id)+",'"+str(city_title)+"',"+str(country_id)+",'','"+str(first_name)+"',"+str(0)+",'"+str(last_name)+"',"+str(sex)+",'"+str(site)+"',"+str(unixtime)+",0)".format ()
                            cursor.execute(sql)
                            db.commit()
                            info_grup = 'Записан'
                        except Exception as e:
                            #print ('[+] Ошибка записи 1:',e)
                            info_grup = 'Ошибка'
                    else:
                        info_grup = 'Записана ранее'
                        #print ('    [+] Данные по пользователю записаны ранее')
                    if info_grup == 'Записана ранее':
                        #print (colorama.Fore.MAGENTA  + '            [+] '+str(nm)+' группа: '+name+' ('+str(id_grup)+') '+info_grup)
                        print (colorama.Fore.MAGENTA  + '        [+] Пользователь: '+str(id_user)+' '+str(first_name)+' '+str(last_name)+' '+str(site)+' '+info_grup)
                        pass
                    else:
                        #print (colorama.Fore.YELLOW   + '            [+] '+str(nm)+' группа: '+name+' ('+str(id_grup)+') '+info_grup)    
                        print (colorama.Fore.YELLOW  +  '        [+] Пользователь: '+str(id_user)+' '+str(first_name)+' '+str(last_name)+' '+str(site)+' '+info_grup)
            print ('[+] Фиксируем транзакцию')        
            db.commit()        
            iz_pause (10)
            #time.sleep (10)
        iz_pause (60*5)        
            
if options.menu == '4':
    print ("    [+] Обновляем информацию о клиентах в базе. И обновляю базу в группе.")
    import random
    import iz_func
    import json
    import requests
    import time
    print ('    [+] Текущее время:',int(time.time()))
    import pymysql
    db = pymysql.connect(host='localhost',
                            user='izofen',
                            password='Podkjf3141!',
                            database='site_rus',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()  
    sql = "select id,first_name,last_name from vk_user where unixtime_update = 0 limit 10;"   ### Обновление по unixtime
    print ('    [+] Получение данных из базы')
    cursor.execute(sql)
    data = cursor.fetchall()
    nm = ''
    for rec in data: 
        id,first_name,last_name = rec.values()
        print ('    [+] ',id,first_name,last_name)
        nm = nm + str(id)+','
    
    list_token = get_token () 
    random.shuffle(list_token)
    token = list_token[0][1] 
    
    url = ''
    url = url + 'https://api.vk.com/method/users.get'
    url = url + '?access_token='+str(token)
    url = url + '&user_ids='+str(nm)
    url = url + '&fields=sex,site,city&v=5.131'

    response = requests.get(url)
    parsed_string = response.json()
    response = parsed_string['response']
                
    #if 1==1:
    for line in response:
        id          = line['id'] 
        first_name  = line['first_name'] 
        last_name   = line['last_name']
        site = ''           
        try:
            site        = line['site']
        except Exception as e:
            site = '' 

        city = ''
        city_id = 0 
        city_title = ''            
        try:    
            city        = line['city']  
            city_id     = city['id']
            city_title  = city['title']
        except Exception as e:
            city = ''
            city_id = 0
            city_title = ''

        unixtime = int(time.time())
        print ('        [+]',first_name,last_name,city_title,site)
        try: 
            sql = "UPDATE vk_user SET site = '"+str(site)+"',city_title = '"+str(city_title)+"', city_id = "+str(city_id)+", unixtime_update = "+str(unixtime)+" WHERE id = "+str(id)+""
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print ('[+]', e)   
    print ('    [+] Пауза 15 мин') 
    time.sleep (60*15)

if options.menu == '3':
    print ("[+] Проставляем названия группам. У наших аккаунтов")
    import iz_func
    import json
    import requests
    import time
    import random
    list_token = get_token () 
    random.shuffle(list_token)
    token = list_token[0][1] 
    import pymysql
    db = pymysql.connect(host='localhost',
                            user='izofen',
                            password='Podkjf3141!',
                            database='site_rus',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()    
    sql = "select id,name,description from vk_grup where unixtime = 0 limit 500;"
    cursor.execute(sql)
    data = cursor.fetchall()
    sm = '0'
    for rec in data: 
        id,name,description = rec.values()
        #print ("[+] name",id,name,str(description)[0:30])
        sm = sm + ','+str(id) 
        
    url = "https://api.vk.com/method/groups.getById?access_token="+str(token)+"&v=5.131&group_ids="+str(sm)+"&fields=description,members_count";
    response = requests.get(url)
    parsed_string = response.json()
    #print (parsed_string)
    #exit (0)
    try:
        response = parsed_string["response"]
    except Exception as e:
        response = []
        time.sleep (60*30)
        #exit (0)       

    for line in response:
        name = ''
        screen_name = ''
        members_count = 0
        description = ''
        unixtime = 0
        id       = 0
        name          = line['name']
        screen_name   = line['screen_name']
        
        id = line['id']
        
        try:
            members_count = line['members_count']
        except: 
            members_count = 0
        try:    
            description = line['description'] 
        except: 
            description = ''
        unixtime = int(time.time ())
        name = change (name)
        screen_name   = change (screen_name)
        description   = change (description)
        print ('[+] ',name)
        #print ('[+] ',description)
        #print ('[+] description',description)
        try:
            sql = "UPDATE vk_grup SET name = '"+str(name)+"' WHERE id = "+str(id)+""
            cursor.execute(sql)
            db.commit()
        except: 
            sql = "UPDATE vk_grup SET name = 'Ошибка записи' WHERE id = "+str(id)+""
            cursor.execute(sql)
            db.commit()
        sql = "UPDATE vk_grup SET screen_name = '"+str(screen_name)+"' WHERE id = "+str(id)+""
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE vk_grup SET members_count = "+str(members_count)+" WHERE id = "+str(id)+""
        cursor.execute(sql)
        db.commit()
        try:
            sql = "UPDATE vk_grup SET description = '"+str(description)+"' WHERE id = "+str(id)+""
            cursor.execute(sql)
            db.commit()        
        except: 
            sql = "UPDATE vk_grup SET description = '' WHERE id = "+str(id)+""
            cursor.execute(sql)
            db.commit()        
 
        sql = "UPDATE vk_grup SET unixtime = "+str(unixtime)+" WHERE id = "+str(id)+""
        #print (sql)
        cursor.execute(sql)
        db.commit() 

    print ('Pause',5,'min')
    time.sleep (60*5)

if options.menu == '2':
    print ("[+] Проставляем данные пользователя. У наших аккаунтов")
    import iz_func
    import json
    import requests
    import time
    db,cursor = iz_func.connect ()
    sql = "select id,name,token from vk_accound where 1=1;"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name,token = rec.values()
        print ("[+] name",name)
        url = "https://api.vk.com/method/users.get?access_token="+str(token)+"&v=5.131";
        response = requests.get(url)
        parsed_string = response.json()
        print ("[+] parsed_string",parsed_string)
        error    = ''
        try: 
            error    = parsed_string["error"] 
        except:
            error    = ''

        if error  == '':
            response = parsed_string["response"]
            for line in response:
                first_name = line["first_name"] 
                last_name  = line["last_name"] 
                user_id    = line["id"]   
                sql = "UPDATE vk_accound SET user_id = "+str(user_id)+" WHERE id = "+str(id)+""
                cursor.execute(sql)
                db.commit()
                sql = "UPDATE vk_accound SET first_name = '"+str(first_name)+"' WHERE id = "+str(id)+""
                cursor.execute(sql)
                db.commit()
                sql = "UPDATE vk_accound SET last_name = '"+str(last_name)+"' WHERE id = "+str(id)+""
                cursor.execute(sql)
                db.commit()
                sql = "UPDATE vk_accound SET name = '"+str(first_name) + " " + str(last_name)+"' WHERE id = "+str(id)+""
                cursor.execute(sql)
                db.commit()        
            print ('[+] 10 сек.')    
            time.sleep (10)    
                     
if options.menu == '1':
    print ("[+] Читаю новости у группы и проставляю нравится. Используется для автоматической работы страницы")
    import iz_func
    import json
    import requests
    import time
    import random
    db,cursor = iz_func.connect ()
    sql = "select id,name,token,user_id from vk_accound where status = 'main' or status = 'like';"
    cursor.execute(sql)
    data = cursor.fetchall()
    tm_like = 2
    tm_see = 2
    #grup_like = -90064209  ## Моя группа телеграмм бота
    grup_like = 24709387    ## Моя учетка основная
    #grup_like = -209085681 ## 1С Предприятие API VK
    
    list = []    
    for rec in data: 
        id,name,token,user_id = rec.values()
        list.append ([id,name,token,user_id])
        
    random.shuffle(list)    
    for rec in list:    
        id,name,token,user_id = rec
        print ("[+] name",name)
        url = "https://api.vk.com/method/wall.get?access_token="+str(token)+"&owner_id="+str(grup_like)+"&v=5.131&offset=0&count=1";
        response = requests.get(url)
        parsed_string = response.json()
        try:
            error = ''
            error = parsed_string ['error']
        except:
            error = ''
            print ('[parsed_string]',parsed_string)

        if error == '':
            response = parsed_string['response']
            items    = response["items"]
            new_id = 0
            new_text = ''
            for line in items:
                new_id   = line["id"]
                new_text = line["text"] 
            print ("[+] new_id:",new_id) 
            print ('[+] Проверяем ранее выставленные значения у пользователя')
            url = "https://api.vk.com/method/likes.isLiked?access_token="+str(token)+"&user_id="+str(user_id)+"&type=post"+"&owner_id="+str(grup_like)+"&item_id="+str(new_id)+"&v=5.131";
            response = requests.get(url)
            parsed_string = response.json()
            print ("[+] Ответ проверки на ранее выставленный лайк: ",parsed_string)
            response = parsed_string['response']
            liked = response["liked"]
            copied = response["copied"]    
            if liked == 0:
                tm = tm_see
                print ('[+] Ожидаем ',tm,'мин')
                time.sleep (tm*60)        
                url = "https://api.vk.com/method/likes.add?access_token="+str(token)+"&owner_id="+str(grup_like)+"&v=5.131&&type=post&item_id="+str(new_id);
                response = requests.get(url)
                parsed_string = response.json()
                print ('[+] Выставленный лайк',parsed_string)
                #response = parsed_string['response']
                tm = tm_like
                print ('[+] Ожидаем ',tm,'мин')
                time.sleep (tm*60)
     