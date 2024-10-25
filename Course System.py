import os
from flask import Flask, redirect, request, render_template, url_for, session
from flask_bcrypt import Bcrypt
from datetime import datetime
import MySQLdb

app = Flask(__name__) 
app.config['SECRET_KEY'] = os.urandom(24)
bcrypt = Bcrypt()

conn = MySQLdb.connect(host="127.0.0.1",user="root", passwd="1234",db="testdb")
cursor = conn.cursor()

years= 110
semester = 2


#預選必修
query = "Select * From Takes Where Semester = {} And Years = {};".format(semester,years)
cursor.execute(query)
if not cursor.fetchall():
    #抓取學生資料
    query = """Select StudentID, DepartmentName, ClassNo , students_year
            From Students Where Semester = {} And Years = {};
            """.format(semester,years)
    cursor.execute(query)
    students = cursor.fetchall()
    #根據每位學生的系所年紀班級，加入必修課程
    for StudentID, DepartmentName, ClassNo , StudentYear in students:
        query = """SELECT CourseID,TimeSlotID FROM Sections
                WHERE CourseID In (Select CourseID From Courses 
                Where DepartmentName = '{}' And course_years = {} And course_classNo = '{}' 
                And CreditType = '必修') And years= {} And semester= {}
                """.format(DepartmentName,StudentYear,ClassNo,years,semester)
        cursor.execute(query)
        for CourseID,TimeSlotID in cursor.fetchall():
            insert_query = """insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType)
                            values('{}','{}','{}',{},{},'必修');
                            """.format(StudentID,CourseID,TimeSlotID,semester,years)
            cursor.execute(insert_query)
            conn.commit()
                
studentid = None

@app.route('/')
def start(): 
    return redirect(url_for('home'))


#登入頁面
@app.route('/login',methods=['GET','POST'])
def login(): 
    if session.get('studentid') and session.get('password'):
        studentid = session.get('studentid')
        query = "Select StudentID From UserID Where StudentID = '{}';".format(studentid)
        cursor.execute(query)
        studentid_check = cursor.fetchone()
        if studentid_check == None:
            return render_template('ErrorMessage.html',status=(("學號錯誤!","login","重新登入"),))
        query = "Select IDPassword From UserID Where StudentID = '{}';".format(studentid)
        cursor.execute(query)
        password_check = cursor.fetchone()
        if not bcrypt.check_password_hash(session.get('password'),password_check[0]):
            session['password'] = None
            return render_template('ErrorMessage.html',status=(("請重新登入!","login","重新登入"),))
        return redirect(url_for('home'))
    session['studentid'] = None
    session['password'] = None
    return render_template('login.html')


#主頁
@app.route('/home', methods=['GET','POST'])
def home(): 
    global studentid
    if not session.get('studentid'):
        #檢查學號
        session['studentid']=request.form.get('studentid')
        studentid = session.get('studentid')
        if studentid == '':
            return render_template('ErrorMessage.html',status=(("請輸入學號!","login","重新登入"),))
        elif studentid == None:
            return redirect(url_for('login'))
        
        query = "Select StudentID From UserID Where StudentID = '{}';".format(studentid)
        cursor.execute(query)
        studentid_check = cursor.fetchone()
        if studentid_check == None:
            return render_template('ErrorMessage.html',status=(("學號錯誤!","login","重新登入"),))
        
        #檢查密碼
        password=request.form.get('password')
        if password == '':
            return render_template('ErrorMessage.html',status=(("請輸入密碼!","login","重新登入"),))
        elif password == None:
            return redirect(url_for('login'))
        #密碼加密
        password = bcrypt.generate_password_hash(password=password)
        session['password']=password
        query = "Select IDPassword From UserID Where StudentID = '{}';".format(studentid)
        cursor.execute(query)
        password_check = cursor.fetchone()
        if not bcrypt.check_password_hash(session.get('password'),password_check[0]):
            session['password'] = None
            return render_template('ErrorMessage.html',status=(("密碼錯誤!","login","重新登入"),))
        session.permanent=True
    else:
        studentid = session.get('studentid')
        query = "Select StudentID From UserID Where StudentID = '{}';".format(studentid)
        cursor.execute(query)
        studentid_check = cursor.fetchone()
        if studentid_check == None:
            session['studentid'] = None
            return render_template('ErrorMessage.html',status=(("學號錯誤!","login","重新登入"),))
        query = "Select IDPassword From UserID Where StudentID = '{}';".format(studentid)
        cursor.execute(query)
        password_check = cursor.fetchone()
        if not bcrypt.check_password_hash(session.get('password'),password_check[0]):
            return render_template('ErrorMessage.html',status=(("密碼錯誤!","login","重新登入"),))
        
    #抓取已選總學分
    query = """SELECT SUM(Credits) FROM Courses WHERE CourseID in 
            (SELECT DISTINCT CourseID FROM Takes WHERE StudentID = '{}' and years={} and semester={});
            """.format(studentid,years,semester)#抓取那個學生有修什麼課再加總
    cursor.execute(query)
    sum_Credits = cursor.fetchone()#抓取的值設給sum_Credits
    if sum_Credits[0] == None:#如果完全沒有修會抓取的總值是NONE，要把它設為0
        sum_Credits = (0,)
    
    #抓取學生名字
    query = """SELECT StudentName From Students Where StudentID = '{}';
            """.format(studentid)#根據學號抓取學生名字
    cursor.execute(query)
    studentName = cursor.fetchone()
    
    #抓取已關注課程
    query = """SELECT CourseID,CourseName,Sections.TimeSlotID,Building,RoomNo 
            FROM (Select Sections.CourseID,CourseName,TimeSlotID,Building,RoomNo,Sections.Semester,Sections.Years 
            From Sections Inner Join Courses On Sections.CourseID = Courses.CourseID) As Sections 
            Inner Join TimeSlot On Sections.TimeSlotID = TimeSlot.TimeSlotID WHERE courseid in 
            (SELECT CourseID FROM Follows WHERE StudentID = '{}')
            and years={} and semester={} Order By Sections.TimeSlotID ASC;
            """.format(studentid,years,semester)#先結合section and course再結合有在關注裡的courseID，抓取關注課程的時間表
    cursor.execute(query)
    follows = cursor.fetchall()
    
    #抓取已選課程
    query = """SELECT CourseID,CourseName,Sections.TimeSlotID,Building,RoomNo 
            FROM (Select Sections.CourseID,CourseName,TimeSlotID,Building,RoomNo,Sections.Semester,Sections.Years 
            From Sections Inner Join Courses On Sections.CourseID = Courses.CourseID) As Sections 
            Inner Join TimeSlot On Sections.TimeSlotID = TimeSlot.TimeSlotID WHERE courseid in 
            (SELECT CourseID FROM Takes WHERE StudentID = '{}' and years={} and semester={})
            and years={} and semester={} Order By Sections.TimeSlotID ASC;
            """.format(studentid,years,semester,years,semester)#合伴section and course,再結合該學生的takes,再抓出該學生修的課
    cursor.execute(query)
    return render_template('home.html',studentName=studentName[0],sum_Credits=int(sum_Credits[0]),section=cursor.fetchall(),follows=follows)
    
    
#登出頁面
@app.route('/logout',methods=['GET','POST'])
def logout(): 
    global studentid
    studentid = None
    session['studentid'] = None
    session['password'] = None
    return render_template('logout.html')


#加選課程
@app.route('/add', methods=['GET','POST'])
def add():
    if not session.get('studentid'):
        return redirect(url_for('login'))
    else:
        global studentid
        studentid = session.get('studentid')
        query = "Select IDPassword From UserID Where StudentID = '{}';".format(studentid)
        cursor.execute(query)
        password_check = cursor.fetchone()
        if not bcrypt.check_password_hash(session.get('password'),password_check[0]):
            return render_template('ErrorMessage.html',status=(("密碼錯誤!","login","重新登入"),))
        
    courseid = request.form.get('courseid')

    #檢查是否有這堂課
    # 用courseID檢查有無此課
    CourseID_query = "SELECT CourseID FROM Courses WHERE CourseID = '{}';".format(courseid)
    cursor.execute(CourseID_query)
    if cursor.fetchone() == None:
        return render_template('ErrorMessage.html',status=(("找不到這堂課","home","返回"),))
    
    #檢查是否已選同名課程
    #找出該課程代碼的課程名稱
    # 找出已選的課 判斷有沒有同名課程
    query = "SELECT CourseName FROM Courses WHERE courseid = '{}'".format(courseid)
    cursor.execute(query)
    course_name = cursor.fetchone()
    #找出已選的課程名稱
    # takes course合併找出修過課程的名稱
    query = """SELECT Coursename FROM Courses WHERE coursename IN 
            (SELECT DISTINCT coursename from takes INNER JOIN Courses 
            on takes.courseid = courses.courseid WHERE studentid = '{}')
            """.format(studentid)
    cursor.execute(query)
    for course in cursor.fetchall():
        if course_name == course:
            return render_template('ErrorMessage.html',status=(("不可加選與已選課程同名的課程","home","返回"),))

    #檢查退選後是否超出30學分
    #抓取總學分
    # 找出修課總學分
    query = """SELECT SUM(Credits) FROM Courses WHERE CourseID in 
            (SELECT DISTINCT CourseID FROM Takes WHERE StudentID = '{}' and years={} and semester={});
            """.format(studentid,years,semester)
    cursor.execute(query)
    sum_Credits = cursor.fetchone()
    #抓取加選課程學分
    #找出要加炫課的總學分
    query = "SELECT Credits FROM Courses WHERE CourseID = '{}';".format(courseid)
    cursor.execute(query)
    add_Credits = cursor.fetchone()
    if sum_Credits[0] + add_Credits[0] > 30:
        return render_template('ErrorMessage.html',status=(("不可超過30學分","home","返回"),))
 
    #檢查是否衝堂
    #抓取該課程上課時間
    #查看選課的時間表
    query = "SELECT TimeSlotID FROM Sections WHERE CourseID = '{}' and years={} and semester={}".format(courseid,years,semester)
    cursor.execute(query)
    course_timeslot = cursor.fetchall()
    #抓取學生已選課表的上課時間
    #找出以選課課程的時段
    query = "SELECT TimeSlotID from takes WHERE studentid = '{}' and years={} and semester={}".format(studentid,years,semester)
    cursor.execute(query)
    for schedule_timeslot in cursor.fetchall():
        for timeslot in course_timeslot:
            if schedule_timeslot == timeslot:
                return render_template('ErrorMessage.html',status=(("不可加選衝堂的課程","home","返回"),))

    #檢查是否人數已滿
    #找出該課程最小教室
    #找出課程最小教室能容納多少人
    query = """SELECT MIN(Capacity) 
            FROM classrooms INNER JOIN sections ON 
            classrooms.Building = sections.Building AND classrooms.RoomNo = sections.RoomNo 
            WHERE courseid = '{}' and years={} and semester={};
            """.format(courseid,years,semester)
    cursor.execute(query)
    min_capacity = cursor.fetchone()
    #找出修該課的學生總數
    #找出已修過這堂課的總數
    query = """SELECT COUNT(DISTINCT StudentID) 
            FROM takes WHERE CourseID = '{}' and years={} and semester={};
            """.format(courseid,years,semester)
    cursor.execute(query)
    course_student = cursor.fetchone()
    #若人數已滿，加入排隊列表
    if course_student >= min_capacity:
        #檢查是否已加入排隊列表
        query = "Select * From CourseQueue Where StudentID = '{}' And CourseID = '{}';".format(studentid,courseid)
        cursor.execute(query)
        if cursor.fetchone() == None:
            #加入排隊列表
            query = "Insert Into CourseQueue Values('{}','{}','{}');".format(studentid,courseid,datetime.now())
            cursor.execute(query)
            conn.commit()
        return render_template('ErrorMessage.html',status=(("人數已滿，已加入排隊列表","home","返回"),))
    
    #加選課程
    #抓取所有的section到takes裡面
    query = """SELECT TimeSlotID,Semester,Years FROM Sections
            WHERE CourseID = '{}' and years={} and semester={}
            """.format(courseid,years,semester)
    cursor.execute(query)
    for TimeSlotID,Semester,Years in cursor.fetchall():
        insert_query = """insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years)
                        values('{}','{}','{}',{},{});
                        """.format(studentid,courseid,TimeSlotID,Semester,Years)
        cursor.execute(insert_query)
        conn.commit()
    
    courseid = request.form.get('courseid')
    query = "Delete From Follows Where StudentID = '{}' And CourseID = '{}';".format(studentid,courseid)
    cursor.execute(query)
    conn.commit()
    return render_template('ErrorMessage.html',status=(("加選成功","home","返回"),))
 
 
#退選
@app.route('/drop', methods=['GET','POST'])
def drop():  
    if not session.get('studentid'):
        return redirect(url_for('login'))
    else:
        global studentid
        studentid = session.get('studentid')
        query = "Select IDPassword From UserID Where StudentID = '{}';".format(studentid)
        cursor.execute(query)
        password_check = cursor.fetchone()
        if not bcrypt.check_password_hash(session.get('password'),password_check[0]):
            return render_template('ErrorMessage.html',status=(("密碼錯誤!","login","重新登入"),))
        
    courseid=request.form.get('courseid')
    
    #檢查是否已選此課程
    query = "SELECT CourseID FROM Courses WHERE courseid = '{}';".format(courseid)
    cursor.execute(query)
    course_id = cursor.fetchone()
    query = """SELECT CourseID FROM Courses WHERE courseID IN 
            (SELECT DISTINCT courseid from takes 
            WHERE studentid = '{}' and semester={} and years={});
            """.format(studentid,semester,years)#根據學生所選的課找出有沒有選這堂課
    cursor.execute(query)
    flag = 0     #如果沒有在裡面就設零
    for course in cursor.fetchall():
        if course_id == course:  #如果有flag=1
            flag = 1
    if flag == 0:
        return render_template('ErrorMessage.html',status=(("無此課程","home","返回"),))
    
    #檢查是否該學生的必修課
    query="SELECT CreditType from takes where courseid='{}' and studentid='{}';".format(courseid,studentid)
    cursor.execute(query)
    drop_Credits=cursor.fetchone()
    if drop_Credits[0]=="必修":
         return render_template('ErrorMessage.html',status=(("這是必修不可手動退選","home","返回"),))
    
    #檢查退選後是否低於9學分
    query = """SELECT SUM(Credits) FROM Courses 
            WHERE CourseID in (SELECT DISTINCT CourseID FROM Takes
            WHERE StudentID = '{}' and years={} and semester={});
            """.format(studentid,years,semester)
    cursor.execute(query)
    sum_Credits = cursor.fetchone()
    query = "SELECT Credits FROM Courses WHERE CourseID = '{}';".format(courseid)
    cursor.execute(query)
    drop_Credits = cursor.fetchone()
    if sum_Credits[0] - drop_Credits[0] < 9:
        return render_template('ErrorMessage.html',status=(("不可少於9學分","home","返回"),))
    
    #退選課程
    delete_query = """delete from Takes where studentid='{}' and courseid='{}' and semester={} and years={};
                    """.format(studentid,courseid,semester,years)
    cursor.execute(delete_query)
    conn.commit()
    
    #依照預選此課的排隊列表（按時間順序）
    query = "Select StudentID From CourseQueue Where CourseID = '{}' Order By TimeQueue ASC;".format(courseid)
    cursor.execute(query)
    add_student = cursor.fetchall()
    #加選最早排隊選課且符合加選規定的學生
    count = 0
    if add_student: #如果有人排隊就會進入迴圈
        while add_student[count]:
            flag = 0 #有沒有符合規定（符合規定是0）
            #檢查是否已選同名課程
            #找出該課程代碼的課程名稱
            query = "SELECT CourseName FROM Courses WHERE courseid = '{}'".format(courseid)
            cursor.execute(query)
            course_name = cursor.fetchone()
            #找出已選的課程名稱
            query = """SELECT Coursename FROM Courses WHERE coursename IN 
                    (SELECT DISTINCT coursename from takes INNER JOIN Courses 
                    on takes.courseid = courses.courseid WHERE studentid = '{}')
                    """.format(add_student[count][0])
            cursor.execute(query)
            for course in cursor.fetchall():
                if course_name == course:
                    flag = 1 #不符合flag設為1

            #檢查退選後是否超出30學分
            #抓取總學分
            query = """SELECT SUM(Credits) FROM Courses WHERE CourseID in 
                    (SELECT DISTINCT CourseID FROM Takes WHERE StudentID = '{}' and years={} and semester={});
                    """.format(add_student[count][0],years,semester)
            cursor.execute(query)
            sum_Credits = cursor.fetchone()
            #抓取加選課程學分
            query = "SELECT Credits FROM Courses WHERE CourseID = '{}';".format(courseid)
            cursor.execute(query)
            add_Credits = cursor.fetchone()
            if sum_Credits[0] + add_Credits[0] > 30:
                flag = 1
        
            #檢查是否衝堂
            #抓取該課程上課時間
            query = "SELECT TimeSlotID FROM Sections WHERE CourseID = '{}' and years={} and semester={}".format(courseid,years,semester)
            cursor.execute(query)
            course_timeslot = cursor.fetchall()
            #抓取學生已選課表的上課時間
            query = "SELECT TimeSlotID from takes WHERE studentid = '{}' and years={} and semester={}".format(add_student[count][0],years,semester)
            cursor.execute(query)
            for schedule_timeslot in cursor.fetchall():
                for timeslot in course_timeslot:
                    if schedule_timeslot == timeslot:
                        flag = 1
                        
            #判斷是否不符合規定            
            if flag == 1:
                count+=1
                continue
            
            #最先符合規定的學生加選課程
            query = """SELECT TimeSlotID,Semester,Years FROM Sections
                    WHERE CourseID = '{}' and years={} and semester={}
                    """.format(courseid,years,semester)
            cursor.execute(query)
            for TimeSlotID,Semester,Years in cursor.fetchall():
                insert_query = """insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years)
                                values('{}','{}','{}',{},{});
                                """.format(add_student[count][0],courseid,TimeSlotID,Semester,Years)
                cursor.execute(insert_query)
                conn.commit()
            break
    return render_template('ErrorMessage.html',status=(("退選成功","home","返回"),))


#顯示可選課程
@app.route('/course_list', methods=['GET','POST'])
def course_list(): 
    if not session.get('studentid'):
        return redirect(url_for('login'))
    else:
        global studentid
        studentid = session.get('studentid')
        query = "Select IDPassword From UserID Where StudentID = '{}';".format(studentid)
        cursor.execute(query)
        password_check = cursor.fetchone()
        if not bcrypt.check_password_hash(session.get('password'),password_check[0]):
            return render_template('ErrorMessage.html',status=(("密碼錯誤!","login","重新登入"),))
        
    query = """Select Current.CourseID, CourseCode, CourseName, DepartmentName, Credits, CreditType, CurrentAmount, TotalAmount From 
            (Select Courses.CourseID, Courses.CourseCode, Courses.CourseName, Courses.DepartmentName, Courses.Credits, Courses.CreditType, 
            count(Distinct StudentID) As CurrentAmount From Courses Left Outer Join Takes On Courses.CourseID = Takes.CourseID 
            Where Courses.Semester = {} And Courses.Years = {} Group By Courses.CourseID) As Current Inner Join 
            (Select CourseID, Min(Capacity) As TotalAmount From Classrooms Inner Join Sections 
            On Classrooms.Building = Sections.Building And Classrooms.RoomNo = Sections.RoomNo Group By CourseID) As Max 
            On Current.CourseID = Max.CourseID;
            """.format(semester,years)
    cursor.execute(query)
    return render_template('List.html',course=cursor.fetchall())


#關注課程
@app.route('/follow_course', methods=['GET','POST'])
def follow_course():
    if not session.get('studentid'):
        return redirect(url_for('login'))
    else:
        global studentid
        studentid = session.get('studentid')
        query = "Select IDPassword From UserID Where StudentID = '{}';".format(studentid)
        cursor.execute(query)
        password_check = cursor.fetchone()
        if not bcrypt.check_password_hash(session.get('password'),password_check[0]):
            return render_template('ErrorMessage.html',status=(("密碼錯誤!","login","重新登入"),))
        
    courseid = request.form.get('courseid')
    query = "Select * From Follows Where StudentID = '{}' And CourseID = '{}';".format(studentid,courseid)
    cursor.execute(query)
    if cursor.fetchone() == None:
        query = "Insert Into Follows Values('{}','{}');".format(studentid,courseid)
        cursor.execute(query)
        conn.commit()
    return render_template('ErrorMessage.html',status=(("課程已關注","course_list","返回"),),home=('home'))


#已關注課程頁面
@app.route('/follow_list', methods=['GET','POST'])
def follow_list(): 
    if not session.get('studentid'):
        return redirect(url_for('login'))
    else:
        global studentid
        studentid = session.get('studentid')
        query = "Select IDPassword From UserID Where StudentID = '{}';".format(studentid)
        cursor.execute(query)
        password_check = cursor.fetchone()
        if not bcrypt.check_password_hash(session.get('password'),password_check[0]):
            return render_template('ErrorMessage.html',status=(("密碼錯誤!","login","重新登入"),))
    
    query = """Select Current.CourseID, CourseCode, CourseName, DepartmentName, Credits, CreditType, CurrentAmount, TotalAmount From 
            (Select Courses.CourseID, Courses.CourseCode, Courses.CourseName, Courses.DepartmentName, 
            Courses.Credits, Courses.CreditType, count(Distinct StudentID) As CurrentAmount From 
            (Select Courses.CourseID, Courses.CourseCode, Courses.CourseName, Courses.DepartmentName, 
            Courses.Credits, Courses.CreditType, Courses.Semester, Courses.Years
            From Courses Inner Join Follows On Courses.CourseID = Follows.CourseID 
            Where StudentID = '{}') As Courses Left Outer Join Takes On Courses.CourseID = Takes.CourseID 
            Where Courses.Semester = {} And Courses.Years = {} Group By Courses.CourseID) As Current Inner Join 
            (Select CourseID, Min(Capacity) As TotalAmount From Classrooms Inner Join Sections 
            On Classrooms.Building = Sections.Building And Classrooms.RoomNo = Sections.RoomNo Group By CourseID) As Max 
            On Current.CourseID = Max.CourseID;
            """.format(studentid,semester,years)
    cursor.execute(query)
    return render_template('Follow.html',course=cursor.fetchall())


#取消關注
@app.route('/cancel_follow', methods=['GET','POST'])
def cancel_follow():
    if not session.get('studentid'):
        return redirect(url_for('login'))
    else:
        global studentid
        studentid = session.get('studentid')
        query = "Select IDPassword From UserID Where StudentID = '{}';".format(studentid)
        cursor.execute(query)
        password_check = cursor.fetchone()
        if not bcrypt.check_password_hash(session.get('password'),password_check[0]):
            return render_template('ErrorMessage.html',status=(("密碼錯誤!","login","重新登入"),))
        
    courseid = request.form.get('courseid')
    query = "Delete From Follows Where StudentID = '{}' And CourseID = '{}';".format(studentid,courseid)
    cursor.execute(query)
    conn.commit()
    return render_template('ErrorMessage.html',status=(("課程已取消關注","follow_list","返回"),),home=('home'))
