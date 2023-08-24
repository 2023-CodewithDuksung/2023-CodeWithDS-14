from flask import Flask, render_template, request, jsonify
from jinja2 import Template
from flaskext.mysql import MySQL
import mysql.connector
import json
import urllib.request as urllib
from bs4 import BeautifulSoup
import random
import time



mysql = MySQL()
app = Flask(__name__)

#MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'weatherhack'
app.config['MYSQL_DATABASE_PASSWORD'] = 'weatherhack99$' 
app.config['MYSQL_DATABASE_DB'] = 'weather'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'



mysql.init_app(app)




@app.route('/')
def hello_world():
    return "hello"


@app.route('/mainpage', methods = ['GET', 'POST'])
def view():
    conn = mysql.connect()  # DB와 연결
    cursor = conn.cursor()  # connection으로부터 cursor 생성 (데이터베이스의 Fetch 관리)
    sql = "SELECT curweather FROM dsweather"  # 실행할 SQL문
    cursor.execute(sql)
    weatherdata = cursor.fetchall()
    sql2 = "SELECT curstatus FROM dsweather"  # 실행할 SQL문
    cursor.execute(sql2)
    weatherstatus = cursor.fetchall()
    sql3 = "SELECT curcloth FROM dsweather"  # 실행할 SQL문
    cursor.execute(sql3)
    weathercloth = cursor.fetchall()
    sql4 = "SELECT curouter FROM dsweather"  # 실행할 SQL문
    cursor.execute(sql4)
    weatherouter = cursor.fetchall()
    

    userweather = []
    userstatus = []
    usercloth = []
    userouter = []

    for wd in weatherdata:
        userweather.append(wd[0])
    for ws in weatherstatus:
        userstatus.append(ws[0])
    for wc in weathercloth:
        usercloth.append(wc[0])
    for wo in weatherouter:
        userouter.append(wo[0])
    



   

    return render_template('start.html', userweather=userweather,userstatus=userstatus, usercloth=usercloth,userouter=userouter  )


@app.route('/submit', methods=['POST'])
def submit():
    weather = request.form['weather']
    status = request.form['status']
    cloth = request.form['cloth']
    outer = request.form['outer']
    condition = request.form['condition']

    conn = mysql.connect()  # DB와 연결
    cursor = conn.cursor()  # connection으로부터 cursor 생성 (데이터베이스의 Fetch 관리)
    cursor.execute("INSERT INTO dsweather (curweather, curstatus, curcondition, curcloth, curouter) VALUES (%s, %s, %s, %s, %s)", (weather, status,condition, cloth, outer))
    conn.commit()
    conn.close()

    print(weather)

    return jsonify({'message': 'success'})


@app.route('/pleasesubmit', methods=['POST'])
def pleasesubmit():
    weather = request.form['weather']
    status = request.form['status']
    condition = request.form['condition']

    conn = mysql.connect()  # DB와 연결
    cursor = conn.cursor()  # connection으로부터 cursor 생성 (데이터베이스의 Fetch 관리)
    cursor.execute("INSERT INTO dsweather (curweather, curstatus, curcondition) VALUES (%s, %s, %s)", (weather, status,condition))
    conn.commit()
    conn.close()

    print(weather)

    return jsonify({'message': 'success'})




@app.route('/max', methods=['GET', 'POST'])
def max_weather():
    conn = mysql.connect() #데이터베이스 연결 객체 생성
    cursor = conn.cursor() #데이터베이스 작업을 수행하기 위한 커서 객체 생성
    #커서는 데이터베이스 연결을 통해 SQL 쿼리 실행, 결과를 컴색, 커서를 통해 SQL문 실행하고 결과 가져오기 가능
    sql = "SELECT curweather FROM dsweather"
    cursor.execute(sql)#SQL쿼리를 실행
    weatherdata = cursor.fetchall()#실행된 커리를 모두 가져오는 역할
    #weatherdata 결과는 튜플의 리스트로 반환됨

    print(weatherdata)

    weather_count = {}

    #weather[0]는 맑음
    for weather in weatherdata:
        if weather[0] in weather_count:
            weather_count[weather[0]] += 1
        else:
            weather_count[weather[0]] = 1
    
    sql2 = "SELECT curstatus FROM dsweather"
    cursor.execute(sql2)
    statusdata = cursor.fetchall()

    status_count = {}

    for status in statusdata:
        if status[0] in status_count:
            status_count[status[0]] += 1
        else:
            status_count[status[0]] = 1

    sql3 = "SELECT curcloth FROM dsweather"
    cursor.execute(sql3)
    clothdata = cursor.fetchall()

    cloth_count = {}

    for cloth in clothdata:
        if cloth[0] in cloth_count:
            cloth_count[cloth[0]] += 1
        else:
            cloth_count[cloth[0]] = 1

    sql4 = "SELECT curouter FROM dsweather"
    cursor.execute(sql4)
    outerdata = cursor.fetchall()

    outer_count = {}

    for outer in outerdata:
        if outer[0] in outer_count:
            outer_count[outer[0]] += 1
        else:
            outer_count[outer[0]] = 1      

    sql5 = "SELECT curcondition FROM dsweather"
    cursor.execute(sql5)
    condition_count = {}
    conditiondata = cursor.fetchall()

    for condition in conditiondata:
        if condition[0] in condition_count:
            condition_count[outer[0]] += 1
        else:
            condition_count[outer[0]] = 1     


    max_weather = max(weather_count, key=weather_count.get)
    max_status = max(status_count, key=status_count.get)
    max_cloth = max(cloth_count, key=cloth_count.get)
    max_outer = max(outer_count, key=outer_count.get)
    max_condition = max(condition_count, key=condition_count.get)


    print("Weather Count:", weather_count)  # weather_count 딕셔너리 내용 확인

    return render_template('second.html', weather_count=weather_count, max_weather = max_weather, max_status=max_status, 
                           max_cloth=max_cloth, max_outer=max_outer, max_condition=max_condition)



@app.route("/board",  methods = ['GET', 'POST'])
def board():
    conn = mysql.connect()
    cursor = conn.cursor()
    #cursor.execute("SELECT content FROM board ORDER BY content DESC")
    cursor.execute("SELECT content FROM board")
    realboard = cursor.fetchall()
    conn.close()

 
    return render_template("board.html", realboard=realboard)


@app.route('/dd', methods=['POST'])
def dsboard():

    content = request.form['content']


    conn = mysql.connect()  # DB와 연결
    cursor = conn.cursor()  # connection으로부터 cursor 생성 (데이터베이스의 Fetch 관리)
    cursor.execute("INSERT INTO board (content) VALUES (%s)", (content))
    conn.commit()
    conn.close()

    
    return jsonify({'message': 'success'})
    


@app.route('/all', methods=['GET', 'POST'])
def allweather():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT curweather, curstatus, curcloth, curouter FROM dsweather")
    allweather = cursor.fetchall()
    conn.close()

 
    return render_template("four.html", allweather=allweather)


@app.route('/weather', methods=['GET', 'POST'])
def crawlweather():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT hour, temp, wfKor, pop, reh, wdKor FROM wweather")
    crawlweather = cursor.fetchall()
    conn.close()



    return render_template("weather.html", crawlweather=crawlweather)

    

@app.route("/lottery",  methods = ['GET', 'POST'])
def lottery():
    
 
    return render_template("lottery.html")

@app.route("/boardwrite", methods = ['GET', 'POST'])
def boardwrite():
    return render_template("boardwrite.html")


@app.route("/main", methods = ['GET', 'POST'])
def mainpage():
    return render_template("main.html")

@app.route("/select", methods = ['GET', 'POST'])
def select():
    return render_template("select.html")

@app.route("/nextselect", methods = ['GET', 'POST'])
def nextselect():
    return render_template("select2.html")


@app.route("/finish", methods = ['GET', 'POST'])
def finish():
    return render_template("finish.html")


@app.route("/lotto", methods = ['GET', 'POST'])
def lotto():
    return render_template("lotto.html")

@app.route("/todayweather", methods = ['GET', 'POST'])
def todayweather():
    conn = mysql.connect() #데이터베이스 연결 객체 생성
    cursor = conn.cursor() #데이터베이스 작업을 수행하기 위한 커서 객체 생성
    #커서는 데이터베이스 연결을 통해 SQL 쿼리 실행, 결과를 컴색, 커서를 통해 SQL문 실행하고 결과 가져오기 가능
    sql = "SELECT curweather FROM dsweather"
    cursor.execute(sql)#SQL쿼리를 실행
    weatherdata = cursor.fetchall()#실행된 커리를 모두 가져오는 역할
    #weatherdata 결과는 튜플의 리스트로 반환됨

    print(weatherdata)

    weather_count = {}

    #weather[0]는 맑음
    for weather in weatherdata:
        if weather[0] in weather_count:
            weather_count[weather[0]] += 1
        else:
            weather_count[weather[0]] = 1
    
    sql2 = "SELECT curstatus FROM dsweather"
    cursor.execute(sql2)
    statusdata = cursor.fetchall()

    status_count = {}

    for status in statusdata:
        if status[0] in status_count:
            status_count[status[0]] += 1
        else:
            status_count[status[0]] = 1

    sql3 = "SELECT curcloth FROM dsweather"
    cursor.execute(sql3)
    clothdata = cursor.fetchall()

    cloth_count = {}

    for cloth in clothdata:
        if cloth[0] in cloth_count:
            cloth_count[cloth[0]] += 1
        else:
            cloth_count[cloth[0]] = 1

    sql4 = "SELECT curouter FROM dsweather"
    cursor.execute(sql4)
    outerdata = cursor.fetchall()

    outer_count = {}

    for outer in outerdata:
        if outer[0] in outer_count:
            outer_count[outer[0]] += 1
        else:
            outer_count[outer[0]] = 1      

    sql5 = "SELECT curcondition FROM dsweather"
    cursor.execute(sql5)
    condition_count = {}
    conditiondata = cursor.fetchall()

    for condition in conditiondata:
        if condition[0] in condition_count:
            condition_count[outer[0]] += 1
        else:
            condition_count[outer[0]] = 1     


    max_weather = max(weather_count, key=weather_count.get)
    max_status = max(status_count, key=status_count.get)
    max_cloth = max(cloth_count, key=cloth_count.get)
    max_outer = max(outer_count, key=outer_count.get)
    max_condition = max(condition_count, key=condition_count.get)


    print("Weather Count:", weather_count)  # weather_count 딕셔너리 내용 확인

    return render_template("todayweather.html",weather_count=weather_count, max_weather = max_weather, max_status=max_status, 
                           max_cloth=max_cloth, max_outer=max_outer, max_condition=max_condition)




if __name__ == '__main__':
    app.run() 