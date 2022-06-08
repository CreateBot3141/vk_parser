from flask import Flask
from flask import request
from flask import send_file
app = Flask(__name__)

from threading import Thread

def get_data_in_list (name,data_big):
    data = ''

    

    #try: 
    #    data = data_big[name]
    #except Exception as e:
    #    print ('[+]',e)    
    #    data = ''
    return data    
        
def connect ():
    import pymysql
    import socket
    db = pymysql.connect(host='localhost',
                        user='izofen',
                        password='Podkjf3141!',
                        database='site_rus',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()    
    return db,cursor

def xor_cipher(strg, key ):
    encript_str = ''
    while strg != '':
        print ('[+] strg',strg)
        kodansii = int(int(strg[0:4])/3)
        print ('[+] strg',kodansii)
        #sm = chr(int(strg[0:3])/key)
        #for letter in str:
        #    encript_str += chr( ord(letter) ^ key )
        encript_str = encript_str + chr(kodansii)
        strg = strg[4:]        
    print ('[+] encript_str',encript_str)
    return  encript_str   

def ekran (message_in):
    message_in = message_in.replace ("<1>","'")
    message_in = message_in.replace ("<2>",'"')
    message_in = message_in.replace ("<7>","/")
    message_in = message_in.replace ("<8>","?")
    message_in = message_in.replace ("<9>","#")

    message_in = message_in.replace ("**7**","/")
    print ('[+] message_in',message_in)

    if message_in == 'not':
        message_in = ''
    return message_in

@app.route('/')
def hello_world():
    return 'API'


def get_file_answer (task_id):
    import iz_func
    import json   
    import iz_telegram    
    db,cursor = iz_func.connect ()            
    st = '<BR>'
    #st = '\n'
    sql = "select id,name from vk_task where id = "+str(task_id)+""
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id_t,name_t = rec.values()         
        print ('[+]',id_t,name_t) 
    answer = ''
    ##### ШАПКА ВЫВОДА ИНФОРМАЦИИ
    
    namebot  = '@parser3141_bot'
    variable = name_t+'_Шапка'
    hat = iz_telegram.load_setting (namebot,variable)
    if hat != '':
        answer = answer + hat + st 
   
   
    if hat =='' and name_t == 'get_news_in_group'  or name_t == 'get_posts_by_group' :
        answer = answer + 'nm;text'+st
    if hat =='' and name_t == 'get_news_in_user' or name_t == 'get_posts_by_user':
        answer = answer + 'nm;text'+st
    if hat =='' and name_t == 'get_subscribers_in_user':
        answer = answer + 'nm;text'+st
    if hat =='' and name_t == 'get_info_user':
        answer = answer + 'nm;text'+st
    if hat =='' and name_t == 'full_info_post':
        answer = answer + 'nm;text'+st
    if hat =='' and name_t == 'get_user_in_group':
        answer = answer + 'nm;avtor;name;user_id'+st
    if hat =='' and name_t == 'get_friend_in_user':
        answer = answer + 'nm;name;user_id'+st
    if  hat =='' and name_t == 'get_group_in_user':
        answer = answer + 'nm;name;user_id'+st
    if  hat =='' and name_t == 'get_friend_in_user_Yes':
        answer = answer + 'nm;name;user_id'+st
    sql = "select id,name,data_id,data_name,data_big,comment,additional from vk_answer where task_id = "+str(task_id)+""
    cursor.execute(sql)
    data = cursor.fetchall()    

    nm = 0
    for rec in data:
        id,name,data_id,data_name,data_big,comment,additional = rec.values()         
        nm = nm + 1 
        
        namebot  = '@parser3141_bot'
        variable = name_t+'_Тело'
        body = iz_telegram.load_setting (namebot,variable)
        if body != '':
            body = body.replace("%nm%",str(nm))
            body = body.replace("%name%",str(name))
            body = body.replace("%data_id%",str(data_id))
            body = body.replace("%data_name%",str(data_name))
            body = body.replace("%data_big%",str(data_big))
            body = body.replace("%comment%",str(comment))
            body = body.replace("%additional%",str(additional))
            answer = answer + body + st 
        
        
        if body == '' and (name_t == 'get_news_in_group' or name_t == 'get_posts_by_group'):
            answer = answer + str(nm) +';'+name +';'+data_name +';'+data_id +';'+data_big + st
        if body == '' and (name_t == 'get_news_in_user'  or name_t == 'get_posts_by_user'):
            answer = answer + str(nm) +';'+name +';'+data_name +';'+data_id +';'+data_big + st
        if body == '' and (name_t == 'get_subscribers_in_user'):
            answer = answer + str(nm) +';'+name +';'+data_name +';'+data_id +';'+data_big + st
        if body == '' and (name_t == 'get_info_user'):
            answer = answer + str(nm) +';'+name +';'+data_name +';'+data_id +';'+data_big + st
        if body == '' and (name_t == 'full_info_post'):
            answer = answer + str(nm) +';'+data_name+ st
        if body == '' and (name_t == 'get_user_in_group'):
            answer = answer + str(nm) +';'+name+';'+data_name +';'+data_id + st
        if body == '' and (name_t == 'get_friend_in_user'):
            answer = answer + str(nm) +';'+name +';'+data_name +';'+data_id + st
        if body == '' and (name_t == 'get_group_in_user'):    
            answer = answer + str(nm) +';'+name +';'+data_name +';'+data_id + st
        if body == '' and (name_t == 'get_friend_in_user_Yes'):
            answer = answer + str(nm) +';'+name +';'+data_name +';'+data_id +';'+data_big + st
    return answer

############################################################################################################################################

@app.route('/<access_code>/testVK/<task_id>')   
def get_test (access_code,task_id): 
    answer = get_file_answer (task_id)
    #answer = answer.replace("<BR>","\n")
    #name_file = "task_"+str(task_id)+".csv" 
    #my_file = open(name_file, "w+") 
    #my_file.write(answer)
    #my_file.close()  
    #absolute_image_path = name_file
    #response = send_file(absolute_image_path, mimetype='image/jpeg', attachment_filename=name_file, as_attachment=True)
    #response.headers["x-filename"] = name_file
    #response.headers["Access-Control-Expose-Headers"] = 'x-filename'  
    #return response    
    return answer

@app.route('/<access_code>/microVK/<task_id>')   
def get_csv (access_code,task_id): 
    answer = get_file_answer (task_id)
    answer = answer.replace("<BR>","\n")
    name_file = "task_"+str(task_id)+".csv" 
    my_file = open(name_file, "w+") 
    my_file.write(answer)
    my_file.close()  
    absolute_image_path = name_file
    response = send_file(absolute_image_path, mimetype='image/jpeg', attachment_filename=name_file, as_attachment=True)
    response.headers["x-filename"] = name_file
    response.headers["Access-Control-Expose-Headers"] = 'x-filename'  
    return response    
    #return answer

@app.route('/<access_code>/microVK/', methods=["GET", "POST"])   ### 
def microVK (access_code):   ### 
    from flask import request
    answer = 'OK'  
    if request.method == "POST":
        print ('[+]----V 1. 224--------------------------------------------------------------[+]')
        print ('[+]',str(request.data))
        print ('[+]',request.json)
        print ('[+]--------------------------------------------------------------------------[+]')  
        parsed_string   = request.json  
        try:
            command = parsed_string['command']
            print ('    [+] [command]',command)
        except Exception as e:
            command = ''      
        try:
            id_task = parsed_string['id_task']
            print ('    [+] [id_task]',id_task)
        except Exception as e:
            id_task = 0    
        try:
            limitP = parsed_string['limit']
            print ('    [+] [limitP]',limitP)
        except Exception as e:
            limitP = 10    
        try:
            offsetP = parsed_string['offset']
            print ('    [+]     [offsetP]',offsetP)
        except Exception as e:
            offsetP = 0      
        if command == 'add_to_task':
            b = request.json
            try:
                data = b['data']
            except Exception as e:    
                data = []
            try:    
                main = data['main']  
            except Exception as e:           
                main = 'Тестовое задание'    
            print ('[+]----------------------------------------------------------[+]')
            print ('[+] main',main)    
            import iz_func
            db,cursor = iz_func.connect ()
            sql = "INSERT INTO vk_task (answer,dataT,name,namebot,status,status_task,user_id,report) VALUES ('{}','{}','{}','{}','{}','{}','{}','')".format ('',iz_func.change(str(request.json)),main,'','','Ожидание','VK')
            cursor.execute(sql)
            db.commit()
            lastid = cursor.lastrowid
            answer = {'task_id':lastid}
        
        if command == 'register':
            b = request.json
            try:
                data = b['data']
            except Exception as e:    
                data = []
            try:    
                main = data['main']  
            except Exception as e:           
                main = 'Тестовое задание'    
            print ('[+]----------------------------------------------------------[+]')
            print ('[+] main',main)                
            import iz_func
            db,cursor = iz_func.connect ()
            sql = "INSERT INTO vk_task (answer,dataT,name,namebot,status,status_task,user_id,report) VALUES ('{}','{}','{}','{}','{}','{}','{}','')".format ('',iz_func.change(str(request.json)),main,'','','Ожидание','VK')
            cursor.execute(sql)
            db.commit()
            lastid = cursor.lastrowid
            answer = {'task_id':lastid}

        if command == 'task_start':
            answer = "Запускает задание"

        if command == 'task_stop':
            answer = "Останавливает задание"

        if command == 'task_skip':
            answer = "Пропускает задание, ставит задачу в конец списка"

        if command == 'task_list':
            answer = "Возвращает список запланированных задач"

        if command == 'task_edit':
            answer = "Изменение параметров задачи"

        if command == 'help':
            answer = "Выдает список доступных задач для данного пользователя"

        if command == 'delete':
            answer = "Удаляет задание"
            sql = "UPDATE vk_task SET `status` = 'stop' WHERE `id` = "+str(id_task)+""
            cursor.execute(sql)
            db.commit() 

        if command == 'progress':
            answer = "Возвращает текущий прогресс, и примерное время на выполнение.общее колличество, и отработанное на данный момен записей"

        if command == 'save_csv':
            answer = "Отдает на скачку хранимый уже на сервере csv"

        if command == 'logging':
            answer = "Получить лог выполняемой задачи"

        if command == 'status':    
            import iz_func
            import json
            db,cursor = iz_func.connect ()
            sql = "select id,name,status_task from vk_task where id = "+str(id_task)+" "
            cursor.execute(sql)
            data = cursor.fetchall()
            status_task = 'Не найдена задача'
            for rec in data:
                id,name,status_task = rec.values()
            result = {'status':status_task,'accomplishment':0}    
            answer = json.dumps (result)
            print ('    [+][answer]',answer)

        if command == 'answer':
            import iz_func
            import json   
            answer = get_file_answer (id_task)
            answer = answer.replace("<BR>","\n")
            print ('[+] answer:',answer)  
            #db,cursor = iz_func.connect ()            
            #sql = "select id,name,status_task,answer from vk_task where id = "+str(id_task)+" limit 1"        
            #cursor.execute(sql)
            #data = cursor.fetchall()
            #answer = ""        
            #for rec in data:
            #    id,name,status_task,answer = rec.values()

            #if answer != '':
            #    sql = iz_func.change_back(answer)+" limit "+str(offsetP)+","+str(limitP)+""            
            #    cursor.execute(sql)
            #    data = cursor.fetchall()
            #    list = []
            #    sum = 0
            #    for rec in data:
            #        sum = sum + 1 
            #        list.append(rec)    
            #else:
            #    sum = 0
            #    list = []
            sum = 0
            result = {'sum':sum,'answer':answer,'comment':'no comment',}            
            answer = json.dumps(result)         
  
    print ("answer [+]:",answer)     
    return answer        

############################################################################################################################################
@app.route('/<access_code>/microFB/', methods=["GET", "POST"])   ### 
def microFB (access_code):   ### 
    from flask import request
    
    if request.method == "POST":
        print ('[+]----V 1. 224--------------------------------------------------------------[+]')
        print (str(request.data))
        print (request.json)
        print ('[+]--------------------------------------------------------------------------[+]')  

    parsed_string   = request.json    
    try:
        command = parsed_string['command']
        print ('[command]',command)
    except Exception as e:
        command = ''
        
    try:
        id_task = parsed_string['id_task']
        print ('[id_task]',id_task)
    except Exception as e:
        id_task = 0    

    answer = 'Нет задачи'
    if command == 'register':
        import iz_func
        db,cursor = iz_func.connect ()
        sql = "INSERT INTO vk_task (answer,dataT,name,namebot,status,status_task,user_id,report) VALUES ('{}','{}','{}','{}','{}','{}','{}','')".format ('',iz_func.change(str(request.json)),'Тестовое задание','','','Ожидание','FB')
        cursor.execute(sql)
        db.commit()
        lastid = cursor.lastrowid
        answer = {'task_id':lastid}

    if command == 'task_start':
        answer = "Запускает задание"

    if command == 'task_stop':
        answer = "Останавливает задание"

    if command == 'task_skip':
        answer = "Пропускает задание, ставит задачу в конец списка"

    if command == 'task_list':
        answer = "Возвращает список запланированных задач"

    if command == 'task_edit':
        answer = "Изменение параметров задачи"

    if command == 'help':
        answer = "Выдает список доступных задач для данного пользователя"

    if command == 'delete':
        answer = "Удаляет задание"

    if command == 'progress':
        answer = "Возвращает текущий прогресс, и примерное время на выполнение.общее колличество, и отработанное на данный момен записей"

    if command == 'save_csv':
        answer = "Отдает на скачку хранимый уже на сервере csv"

    if command == 'logging':
        answer = "Получить лог выполняемой задачи"

    if command == 'status':    
        import iz_func
        import json
        db,cursor = iz_func.connect ()
        sql = "select id,name,status_task from vk_task where id = "+str(id_task)+" "
        cursor.execute(sql)
        data = cursor.fetchall()
        status_task = 'Не найдена задача'
        for rec in data:
            id,name,status_task = rec.values()
        result = {'status':status_task,'accomplishment':0}    
        answer = json.dumps (result)
        print ('[answer]',answer)

    if command == 'answer':
        import iz_func
        import json   
        db,cursor = iz_func.connect ()            
        sql = "select id,name,status_task,answer from vk_task where id = "+str(id_task)+" limit 1"
        print (sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        answer = ""        
        for rec in data:
            id,name,status_task,answer = rec.values()
        if answer != '':
            sql = iz_func.change_back(answer)        
            cursor.execute(sql)
            data = cursor.fetchall()
            list = []
            sum = 0
            for rec in data:
                sum = sum + 1 
                list.append(rec)    
        else:
            sum = 0
            list = []
        result = {'sum':sum,'answer':list,'comment':'no comment',}            
        answer = json.dumps(result)         
    print ("answer [+]:",answer)     
    return answer        


@app.route('/<access_code>/microInsta/', methods=["GET", "POST"])   ### 
def microInsta (access_code):   ### 
    from flask import request
    
    if request.method == "POST":
        print ('[+]----V 1. 224--------------------------------------------------------------[+]')
        print (str(request.data))
        print (request.json)
        print ('[+]--------------------------------------------------------------------------[+]')  

    parsed_string   = request.json    
    try:
        command = parsed_string['command']
        print ('[command]',command)
    except Exception as e:
        command = ''
        
    try:
        id_task = parsed_string['id_task']
        print ('[id_task]',id_task)
    except Exception as e:
        id_task = 0    

    answer = 'Нет задачи'
    if command == 'register':
        import iz_func
        db,cursor = iz_func.connect ()
        sql = "INSERT INTO vk_task (answer,dataT,name,namebot,status,status_task,user_id,report) VALUES ('{}','{}','{}','{}','{}','{}','{}','')".format ('',iz_func.change(str(request.json)),'Тестовое задание','','','Ожидание','Insta')
        cursor.execute(sql)
        db.commit()
        lastid = cursor.lastrowid
        answer = {'task_id':lastid}

    if command == 'task_start':
        answer = "Запускает задание"

    if command == 'task_stop':
        answer = "Останавливает задание"

    if command == 'task_skip':
        answer = "Пропускает задание, ставит задачу в конец списка"

    if command == 'task_list':
        answer = "Возвращает список запланированных задач"

    if command == 'task_edit':
        answer = "Изменение параметров задачи"

    if command == 'help':
        answer = "Выдает список доступных задач для данного пользователя"

    if command == 'delete':
        answer = "Удаляет задание"

    if command == 'progress':
        answer = "Возвращает текущий прогресс, и примерное время на выполнение.общее колличество, и отработанное на данный момен записей"

    if command == 'save_csv':
        answer = "Отдает на скачку хранимый уже на сервере csv"

    if command == 'logging':
        answer = "Получить лог выполняемой задачи"

    if command == 'status':    
        import iz_func
        import json
        db,cursor = iz_func.connect ()
        sql = "select id,name,status_task from vk_task where id = "+str(id_task)+" "
        cursor.execute(sql)
        data = cursor.fetchall()
        status_task = 'Не найдена задача'
        for rec in data:
            id,name,status_task = rec.values()
        result = {'status':status_task,'accomplishment':0}    
        answer = json.dumps (result)
        print ('[answer]',answer)

    if command == 'answer':
        import iz_func
        import json   
        db,cursor = iz_func.connect ()            
        sql = "select id,name,status_task,answer from vk_task where id = "+str(id_task)+" limit 1"
        print (sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        answer = ""        
        for rec in data:
            id,name,status_task,answer = rec.values()
        if answer != '':
            sql = iz_func.change_back(answer)        
            cursor.execute(sql)
            data = cursor.fetchall()
            list = []
            sum = 0
            for rec in data:
                sum = sum + 1 
                list.append(rec)    
        else:
            sum = 0
            list = []
        result = {'sum':sum,'answer':list,'comment':'no comment',}            
        answer = json.dumps(result)         
    print ("answer [+]:",answer)     
    return answer        

@app.route('/<access_code>/microYT/', methods=["GET", "POST"])   ### 
def microYT (access_code):   ### 
    from flask import request
    
    if request.method == "POST":
        print ('[+]----V 1. 224--------------------------------------------------------------[+]')
        print (str(request.data))
        print (request.json)
        print ('[+]--------------------------------------------------------------------------[+]')  

    parsed_string   = request.json    
    try:
        command = parsed_string['command']
        print ('[command]',command)
    except Exception as e:
        command = ''
        
    try:
        id_task = parsed_string['id_task']
        print ('[id_task]',id_task)
    except Exception as e:
        id_task = 0    

    answer = 'Нет задачи'
    if command == 'register':
        import iz_func
        db,cursor = iz_func.connect ()
        sql = "INSERT INTO vk_task (answer,dataT,name,namebot,status,status_task,user_id,report) VALUES ('{}','{}','{}','{}','{}','{}','{}','')".format ('',iz_func.change(str(request.json)),'Тестовое задание','','','Ожидание','YT')
        cursor.execute(sql)
        db.commit()
        lastid = cursor.lastrowid
        answer = {'task_id':lastid}

    if command == 'task_start':
        answer = "Запускает задание"

    if command == 'task_stop':
        answer = "Останавливает задание"

    if command == 'task_skip':
        answer = "Пропускает задание, ставит задачу в конец списка"

    if command == 'task_list':
        answer = "Возвращает список запланированных задач"

    if command == 'task_edit':
        answer = "Изменение параметров задачи"

    if command == 'help':
        answer = "Выдает список доступных задач для данного пользователя"

    if command == 'delete':
        answer = "Удаляет задание"

    if command == 'progress':
        answer = "Возвращает текущий прогресс, и примерное время на выполнение.общее колличество, и отработанное на данный момен записей"

    if command == 'save_csv':
        answer = "Отдает на скачку хранимый уже на сервере csv"

    if command == 'logging':
        answer = "Получить лог выполняемой задачи"

    if command == 'status':    
        import iz_func
        import json
        db,cursor = iz_func.connect ()
        sql = "select id,name,status_task from vk_task where id = "+str(id_task)+" "
        cursor.execute(sql)
        data = cursor.fetchall()
        status_task = 'Не найдена задача'
        for rec in data:
            id,name,status_task = rec.values()
        result = {'status':status_task,'accomplishment':0}    
        answer = json.dumps (result)
        print ('[answer]',answer)

    if command == 'answer':
        import iz_func
        import json   
        db,cursor = iz_func.connect ()            
        sql = "select id,name,status_task,answer from vk_task where id = "+str(id_task)+" limit 1"
        print (sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        answer = ""        
        for rec in data:
            id,name,status_task,answer = rec.values()
        if answer != '':
            sql = iz_func.change_back(answer)        
            cursor.execute(sql)
            data = cursor.fetchall()
            list = []
            sum = 0
            for rec in data:
                sum = sum + 1 
                list.append(rec)    
        else:
            sum = 0
            list = []
        result = {'sum':sum,'answer':list,'comment':'no comment',}            
        answer = json.dumps(result)         
    print ("answer [+]:",answer)     
    return answer        

@app.route('/<access_code>/microOK/', methods=["GET", "POST"])   ### 
def microOK (access_code):   ### 
    from flask import request
    
    if request.method == "POST":
        print ('[+]----V 1. 224--------------------------------------------------------------[+]')
        print (str(request.data))
        print (request.json)
        print ('[+]--------------------------------------------------------------------------[+]')  

    parsed_string   = request.json    
    try:
        command = parsed_string['command']
        print ('[command]',command)
    except Exception as e:
        command = ''
        
    try:
        id_task = parsed_string['id_task']
        print ('[id_task]',id_task)
    except Exception as e:
        id_task = 0    

    answer = 'Нет задачи'
    if command == 'register':
        import iz_func
        db,cursor = iz_func.connect ()
        sql = "INSERT INTO vk_task (answer,dataT,name,namebot,status,status_task,user_id,report) VALUES ('{}','{}','{}','{}','{}','{}','{}','')".format ('',iz_func.change(str(request.json)),'Тестовое задание','','','Ожидание','OK')
        cursor.execute(sql)
        db.commit()
        lastid = cursor.lastrowid
        answer = {'task_id':lastid}

    if command == 'task_start':
        answer = "Запускает задание"

    if command == 'task_stop':
        answer = "Останавливает задание"

    if command == 'task_skip':
        answer = "Пропускает задание, ставит задачу в конец списка"

    if command == 'task_list':
        answer = "Возвращает список запланированных задач"

    if command == 'task_edit':
        answer = "Изменение параметров задачи"

    if command == 'help':
        answer = "Выдает список доступных задач для данного пользователя"

    if command == 'delete':
        answer = "Удаляет задание"

    if command == 'progress':
        answer = "Возвращает текущий прогресс, и примерное время на выполнение.общее колличество, и отработанное на данный момен записей"

    if command == 'save_csv':
        answer = "Отдает на скачку хранимый уже на сервере csv"

    if command == 'logging':
        answer = "Получить лог выполняемой задачи"

    if command == 'status':    
        import iz_func
        import json
        db,cursor = iz_func.connect ()
        sql = "select id,name,status_task from vk_task where id = "+str(id_task)+" "
        cursor.execute(sql)
        data = cursor.fetchall()
        status_task = 'Не найдена задача'
        for rec in data:
            id,name,status_task = rec.values()
        result = {'status':status_task,'accomplishment':0}    
        answer = json.dumps (result)
        print ('[answer]',answer)

    if command == 'answer':
        import iz_func
        import json   
        db,cursor = iz_func.connect ()            
        sql = "select id,name,status_task,answer from vk_task where id = "+str(id_task)+" limit 1"
        print (sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        answer = ""        
        for rec in data:
            id,name,status_task,answer = rec.values()
        if answer != '':
            sql = iz_func.change_back(answer)        
            cursor.execute(sql)
            data = cursor.fetchall()
            list = []
            sum = 0
            for rec in data:
                sum = sum + 1 
                list.append(rec)    
        else:
            sum = 0
            list = []
        result = {'sum':sum,'answer':list,'comment':'no comment',}            
        answer = json.dumps(result)         
    print ("answer [+]:",answer)     
    return answer        

############################################################  ОБЪШИЕ ВОПРОСЫ ###############################################################

@app.route('/parser_picture/<access_code>/<url>/<name>/')   ### 
def parser_picture (access_code,url,name):
    url_picture = 'https://bilder.bild.de/fotos-skaliert/ex-us-praesident-donald-trump-75-besuchte-2019-us-truppen-auf-der-bagram-air-base-noerdlich-von-kabu-aa74ab4812ee4b3099b4f6efd73d8834-77332302/3,w=993,q=high,c=0.bild.jpg'
    name_file_save = 'save_picture_003.jpg'
    from  urllib.request import urlopen 
    urlt = urlopen(url_picture)
    f = urlt.read()
    open(name_file_save,"wb").write(f)
    return "ОК"

@app.route('/random/<access_code>/')   ### 
def random (access_code):   ### 
    import iz_func
    import iz_main
    import iz_color
    print (iz_color.c2+'[+] Процедура: Получение случайного числа (random)'+iz_color.c23)
    access = iz_main.test_access_code (access_code)
    if access == True:
        answer = iz_func.get_pass ()
    else:
        answer = "Отказано в доступе ..."        
    print ('[+] Ответ:',answer)
    return answer

@app.route('/load_capcha/<access_code>/<id>/')
def load_capcha (access_code,id):
    import iz_func
    import iz_telegram
    print ('[+] id:',id)
    db,cursor = iz_func.connect ()
    sql = "select id,capcha from vk_capcha where id = "+str(id)+";".format()
    cursor.execute(sql)
    data = cursor.fetchall()
    capcha = ""
    for rec in data:
        id,capcha = rec.values()
    db.close    
    return str(capcha)

@app.route('/save_capcha/<access_code>/<captcha_img>/')
def save_capcha (access_code,captcha_img):
    captcha_img = captcha_img.replace ('**1**','/')
    captcha_img = captcha_img.replace ('**2**','&')
    captcha_img = captcha_img.replace ('**3**','?')
    namebot = '@ask_314_bot';
    url = ''
    user_id = '399838806'
    print ('[+] access_code',access_code)
    print ('[+] captcha_img',captcha_img)
    import iz_telegram
    import iz_func
    db,cursor = iz_func.connect ()
    sql = "INSERT INTO vk_capcha (namebot,unixtime,url,capcha,status) VALUES ('{}',{},'{}','','')".format (namebot,0,url)
    cursor.execute(sql)
    db.commit()
    lastid = cursor.lastrowid
    message_out,menu = iz_telegram.get_message (user_id,'Проверка капчи',namebot)
    message_out = message_out.replace('%%captcha_img%%',str(captcha_img))   
    markup = ''
    answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
    iz_telegram.save_variable (user_id,namebot,"status",'Ввод капчи')
    return str(lastid) 

@app.route('/vk_get_grup/<access_code>/<limit>/<offset>/')   ### 
def vk_get_grup (access_code,limit,offset):   ### 
    import pymysql
    import json
    db = pymysql.connect(host='localhost',
                            user='izofen',
                            password='Podkjf3141!',
                            database='site_rus',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()   
    sql = "select * from vk_grup where 1=1 ORDER BY id limit "+str(limit)+","+str(offset)
    print ("[sql]",sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    #list = []
    #for rec in data:
    #    id,name = rec.values()
    #    list.append([id,first_name,last_name,bdate,site,sex,city_title]) 
    answer = json.dumps(data)         
    return answer

@app.route('/vk_user/<limit>/<offset>/<city>/<dt>/<site>/')   ### 
def vk_user (limit,offset,city,dt,site):   ### 
    import pymysql
    db = pymysql.connect(host='localhost',
                            user='izofen',
                            password='Podkjf3141!',
                            database='site_rus',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()   
    sql = "select id,first_name,last_name,bdate,site,sex,city_title from vk_user where 1=1 "
    if city != 'No': 
        sql_city = "and city_title = '"+str(city)+"' "  
        sql = sql + sql_city
    if dt != 'No': 
        sql_bdate = "and bdate like '"+str(dt)+"' "  
        sql = sql + sql_bdate    
    if site == "Yes":
        sql_site = "and site <> '' "  
        sql = sql + sql_site    
    sql = sql + " limit "+str(limit)+" offset "+str(offset)
    print ("[sql]",sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    list = []
    for rec in data:
        id,first_name,last_name,bdate,site,sex,city_title = rec.values()
        list.append([id,first_name,last_name,bdate,site,sex,city_title]) 
    answer = json.dumps(list)         
    return answer

@app.route('/vk_get_message/<namebot>/')   ### 
def vk_message (namebot):   ### 
    import iz_func
    import iz_vk          
    db,cursor = iz_func.connect ()
    sql = "select id,name from vk_message where namebot = '"+str(namebot)+"' "
    cursor.execute(sql)
    data = cursor.fetchall()
    return str(data)

@app.route('/vk_accound/')   ### 
def vk_accound ():   ### 
    import iz_func
    import iz_vk          
    db,cursor = iz_func.connect ()
    sql = "select id,token from vk_accound where 1=1"
    cursor.execute(sql)
    data = cursor.fetchall()
    return str(data)

@app.route('/vkmessage/', methods=["GET", "POST"])   ### 
def vkmessage ():   ### 
    namebot = "TEST"
    user_id = "TEST"
    message = "TEST"
    import iz_func
    import iz_vk
    from flask import request
    if request.method == "POST":
        print ('[+]----V 1. 224--------------------------------------------------------------[+]')
        print (request.json)
        print ('[+]--------------------------------------------------------------------------[+]')        
        parsed_string   = request.json
        type_message = parsed_string['type']
        try:
            namebot      = parsed_string['secret'] 
        except Exception as e:
            namebot      = 'не определен'
        print ("")
        print ("[+] VK бот: ",namebot) 
        if type_message == 'group_join':
            user_id = parsed_string['object']['user_id']
            print ('[+] Зафиксирован новый пользователь')

        if type_message == 'message_new': 
            user_id = parsed_string['object']['message']['from_id'] 
            event_id = parsed_string['event_id']           
            event_id = iz_vk.event_test(event_id)
            if event_id != 0:
                return "repid"      
            iz_vk.save_user (namebot,user_id) 
            message = parsed_string['object']['message']['text']
            print ("[+] user_id:",user_id)
            print ("[+] message:",message)
            group_id = parsed_string['group_id']
            print ("[+] group_id:",group_id)
            namebot = str(group_id)
            status  = iz_vk.load_variable (user_id,namebot,"status")
            print ("[+] status:",status)
            #message_out = ""
            #menu        = "";

            answer = iz_vk.send_text (user_id,namebot,message)    

            #if message_out != "":
            #    if menu != "":
            #        vk.messages.send(peer_id=user_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message=message_out)
            #    else:
            #        vk.messages.send(peer_id=user_id,random_id=get_random_id(),message=message_out)

            if message == 'Список уроков':
                import iz_func
                import iz_vk
                db,cursor = iz_func.connect ()
                sql = "select id,name,about from vk_product where 1=1".format()
                cursor.execute(sql)
                data = cursor.fetchall()
                for rec in data:
                    id,name,about = rec.values()
                    message_out   = about
                    menu    = ''
                    answer  = iz_vk.send_message (user_id,namebot,message_out,menu)
    #vk.messages.send(peer_id=user_id,random_id=get_random_id(),message=message_out)


            if status == "Введите ваше прозвище": 
                message_out = 'Ваше имя: '+ str(message) + '\n' + "Вас приняли в фракцию 'Охотники'"
                menu        = 'Главное меню'   
                iz_vk.send_text (user_id,namebot,message_out,menu)
                #keyboard = VkKeyboard(one_time=True)
                #text = "Отмена"
                #keyboard.add_button(text, color=VkKeyboardColor.SECONDARY)
                #vk.messages.send(peer_id=user_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message=message_out)
                iz_vk.save_variable (user_id,namebot,"status","")
                iz_vk.save_variable (user_id,namebot,"Имя игрока",message)
   
            if message == 'Регистрация':
                iz_vk.send_message (user_id,namebot,'Введите ваше прозвище')
                iz_vk.save_variable (user_id,namebot,"status","Введите ваше прозвище")

            if message == '2':
                iz_vk.send_message (user_id,namebot,'1')

    return "4e201ce1"


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)

