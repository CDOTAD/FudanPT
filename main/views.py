from django.shortcuts import render, redirect
from urllib import request
from http import cookiejar
import urllib
from .forms import StudentForm
import json
from django.shortcuts import HttpResponse
from urllib import parse
from bs4 import BeautifulSoup
import pymysql.cursors
import pymysql
import numpy as np
# import tesserocr

# Create your views here.


def index(req):

    login_url = 'https://gsas.fudan.edu.cn/sscjcx/index'
    code_url = 'https://gsas.fudan.edu.cn/captcha/imageCode'

    user_agent = r'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 r'Chrome/27.0.1453.94 Safari/537.36'
    
    head = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

    cookie = cookiejar.CookieJar()
    handler = request.HTTPCookieProcessor(cookie)

    opener = request.build_opener(handler)

    req_crawler = request.Request(url=login_url, headers=head)
    req_code = request.Request(url=code_url, headers=head)

    response = opener.open(req_crawler)
    for item in cookie:
        cookie_name = item.name
        cookie_value = item.value
    
    response_code = opener.open(req_code)
    code = response_code.read()
    with open('main/static/'+str(cookie_value)+'.png','wb') as code_img:
        code_img.write(code)
    response.close()
    response_code.close()
    return render(req, 'base.html', {'string': str(cookie_value)})


def test_post(req):
    if req.method == 'GET':
        return HttpResponse('get')
    else:
        req_data = json.loads(req.body)
        username = req_data['username']
        password = req_data['password']
        varycode = req_data['varycode']
        cookie = req_data['crawcookie']
        print('username', username)
        # print(type(username))
        # print(username, password, varycode, cookie)

        # img_file = 'main/static/'+str(cookie)+'.png'
        # varycode = tesserocr.file_to_text(img_file)
        # varycode = str(varycode).strip().strip(b'\x00'.decode())
        # print('varycode', varycode)

        user_agent = r'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 r'Chrome/27.0.1453.94 Safari/537.36'
        
        head = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

        head['Cookie'] = 'cn_com_southsoft_gms='+str(cookie)
        post_url = 'https://gsas.fudan.edu.cn/sscjcx/28198B369067E88DAB9FEFE85484DBF4'
        try:
            post_data = {}
            post_data['nd'] = '2019'
            post_data['username'] = username
            post_data['password'] = password
            post_data['validateCode'] = varycode
            # print(post_data)
            datepostdata = parse.urlencode(post_data).encode('utf-8')
            
            craw_req = request.Request(url=post_url, data=datepostdata, headers=head)

            craw_response = urllib.request.urlopen(craw_req)
            html = craw_response.read().decode('utf-8')
        
            soup = BeautifulSoup(html, "lxml")
            craw_response.close()
            
            result = soup.select("#errorInfo")
            if len(result)<1:
                # print('success')

                table = soup.table
                trs = table.find_all('tr')
                total_grade_tr = trs[-1]
                name_tr = trs[0]
                type_tr = trs[1]

                # 总成绩    
                total_grade = total_grade_tr.find_all('td')[-1].get_text()
                
                # 报考类型
                st_type = type_tr.find_all('td')[-1].get_text()
                st_type = str(st_type).strip().strip(b'\x00'.decode())
                # print(st_type)
                
                # 姓名
                st_name = name_tr.find_all('td')[-1].get_text()
                st_name = str(st_name).strip().strip(b'\x00'.decode())

                
                student_type = 0

                # if '计算机' in st_type:
                #     if '专' in st_type:
                #         student_type = 0
                #     else:
                #         student_type = 1
                # else:
                #     student_type = 2

                # 专硕
                if '085211' in st_type:
                    student_type = 0
                # 学硕
                elif '081201' in st_type or '081202' in st_type or '081203' in st_type or '083900' in st_type:
                    student_type = 1
                else:
                    student_type = 2

                rep = {'status': 0, 'st_type': student_type, 'total_grade': total_grade, 'st_name': st_name}
                
                if student_type !=2:
                    # 插入数据库
                    connect = pymysql.Connect(
                        host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='zhangzhao1996',
                        db='student',
                        charset='utf8'
                    )

                    cursor = connect.cursor()

                    sql = "SELECT * FROM student WHERE number = %d;"
                    cursor.execute(sql % int(username))
                    if cursor.rowcount > 0:
                        pass
                    else:
                        sql = "INSERT INTO student(number, type, grade) VALUES (%s, %d, %d);"
                        insert_data = (str(username), student_type, int(total_grade))
                        cursor.execute(sql % insert_data)
                        connect.commit()
                    if student_type == 0:
                        sql = "SELECT grade FROM student WHERE type = 0 ORDER BY grade desc;"
                        cursor.execute(sql)
                        grade_list = []
                        for item in cursor.fetchall():
                            grade_list.append(int(item[0]))
                        # print(grade_list)
                        total_grade = int(total_grade)
                        index = grade_list.index(total_grade)
                        total = cursor.rowcount

                        rep['rank'] = str(index+1) + '/' + str(total)
                    elif student_type == 1:
                        
                        sql = "SELECT grade FROM student WHERE type = 1 ORDER BY grade desc;"
                        cursor.execute(sql)
                        grade_list = []
                        for item in cursor.fetchall():
                            grade_list.append(int(item[0]))
                        # print(grade_list)
                        total_grade = int(total_grade)
                        index = grade_list.index(total_grade)
                        total = cursor.rowcount

                        rep['rank'] = str(index+1) + '/' + str(total)

                    
                    cursor.close()
                    connect.close()
                
                return HttpResponse(json.dumps(rep, ensure_ascii=False), content_type="application/json, charset=utf-8")
            else:
                result = result[0].get_text()
                result = str(result).strip().strip(b'\x00'.decode())
                print(result)
                rep = {'status': 1, 'data': result}
                return HttpResponse(json.dumps(rep, ensure_ascii=False), content_type="application/json, charset=utf-8")

        except urllib.error.URLError as e:
            print(e.reason)
            rep = {'status': 1, 'data': 'error'}
            return HttpResponse(json.dumps(rep, ensure_ascii=False), content_type="application/json, charset=utf-8")                


def rank(req):

    connect = pymysql.Connect(
                        host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='zhangzhao1996',
                        db='student',
                        charset='utf8'
                    )

    cursor = connect.cursor()

    sql = "SELECT grade FROM student WHERE type = 0 ORDER BY grade desc;"
    cursor.execute(sql)
    
    grade_list = []
    for item in cursor.fetchall():
        grade_list.append(int(item[0]))
    # print(grade_list)
    
    cursor.close()
    connect.close()

    grade_set = np.unique(grade_list)

    rank_list = []
    for grade in grade_set[::-1]:
        rank_list.append({'grade': str(grade), 'rank': str(grade_list.index(grade)+1)})
    
    return HttpResponse(json.dumps(rank_list, ensure_ascii=False), content_type="application/json, charset=utf-8")


def ranking(req):
    return render(req, 'rank.html')


        