import os
from flask import Flask, redirect, request, render_template, url_for, session
from flask_bcrypt import Bcrypt
from datetime import datetime
import MySQLdb

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
bcrypt = Bcrypt()

conn = MySQLdb.connect(host="127.0.0.1", user="root",
                       passwd="1234", db="testdb")
cursor = conn.cursor()

years = 110
semester = 2

studentid = None


def verify_is_new_semester(semester, years):
    query = "Select * From Takes Where Semester = {} And Years = {};".format(
        semester, years)
    cursor.execute(query)
    return not cursor.fetchall()


def fetch_student_list(semester, years):
    query = """Select StudentID, DepartmentName, ClassNo , students_year
            From Students Where Semester = {} And Years = {};
            """.format(semester, years)
    cursor.execute(query)
    return cursor.fetchall()


def get_student_required_courses(departmentName, studentYear, classNo, years, semester):
    query = """SELECT CourseID,TimeSlotID FROM Sections
            WHERE CourseID In (Select CourseID From Courses 
            Where DepartmentName = '{}' And course_years = {} And course_classNo = '{}' 
            And CreditType = '必修') And years= {} And semester= {}
            """.format(departmentName, studentYear, classNo, years, semester)
    cursor.execute(query)
    return cursor.fetchall()


def take_course_section(studentID, courseID, timeSlotID, semester, years):
    insert_query = """insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years,CreditType)
                    values('{}','{}','{}',{},{},'必修');
                    """.format(studentID, courseID, timeSlotID, semester, years)
    cursor.execute(insert_query)
    conn.commit()


def verify_student(studentid):
    query = "Select StudentID From UserID Where StudentID = '{}';".format(studentid)
    cursor.execute(query)
    return cursor.fetchone() != None


def verify_password(studentid, password):
    query = "Select IDPassword From UserID Where StudentID = '{}';".format(studentid)
    cursor.execute(query)
    password_check = cursor.fetchone()
    return bcrypt.check_password_hash(password, password_check[0])


def get_total_selected_credits(studentid, years, semester):
    query = """SELECT SUM(Credits) FROM Courses WHERE CourseID in 
            (SELECT DISTINCT CourseID FROM Takes WHERE StudentID = '{}' and years={} and semester={});
            """.format(studentid, years, semester)  # 抓取那個學生有修什麼課再加總
    cursor.execute(query)
    result = cursor.fetchone()

    if result[0] == None:  # 如果完全沒有修會抓取的總值是NONE，要把它設為0
        return 0

    return int(result[0]) # 抓取的值設給total_credits


def get_student_name(studentid):
    query = "SELECT StudentName From Students Where StudentID = '{}';".format(studentid)  # 根據學號抓取學生名字
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0]


def get_course_name(courseid):
    query = "SELECT CourseName FROM Courses WHERE courseid = '{}'".format(courseid)
    cursor.execute(query)
    return cursor.fetchone()


def get_course_credits(courseid):
    query = "SELECT Credits FROM Courses WHERE CourseID = '{}';".format(courseid)
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0]


def get_course_schedule(courseid, years, semester):
    query = "SELECT TimeSlotID FROM Sections WHERE CourseID = '{}' and years={} and semester={}".format(courseid, years, semester)
    cursor.execute(query)
    return cursor.fetchall()


def get_course_max_quota(courseid, years, semester):
    query = """SELECT MIN(Capacity) 
            FROM classrooms INNER JOIN sections ON 
            classrooms.Building = sections.Building AND classrooms.RoomNo = sections.RoomNo 
            WHERE courseid = '{}' and years={} and semester={};
            """.format(courseid, years, semester)
    cursor.execute(query)
    return cursor.fetchone()


def get_course_current_takes(courseid, years, semester):
    query = """SELECT COUNT(DISTINCT StudentID) 
            FROM takes WHERE CourseID = '{}' and years={} and semester={};
            """.format(courseid, years, semester)
    cursor.execute(query)
    return cursor.fetchone()


def get_student_schedule(studentid, years, semester):
    query = "SELECT TimeSlotID from takes WHERE studentid = '{}' and years={} and semester={}".format(studentid, years, semester)
    cursor.execute(query)
    return cursor.fetchall()


def fetch_followed_course(studentid, years, semester):
    query = """SELECT CourseID,CourseName,Sections.TimeSlotID,Building,RoomNo 
            FROM (Select Sections.CourseID,CourseName,TimeSlotID,Building,RoomNo,Sections.Semester,Sections.Years 
            From Sections Inner Join Courses On Sections.CourseID = Courses.CourseID) As Sections 
            Inner Join TimeSlot On Sections.TimeSlotID = TimeSlot.TimeSlotID WHERE courseid in 
            (SELECT CourseID FROM Follows WHERE StudentID = '{}')
            and years={} and semester={} Order By Sections.TimeSlotID ASC;
            """.format(studentid, years, semester)  # 先結合section and course再結合有在關注裡的courseID，抓取關注課程的時間表
    cursor.execute(query)
    return cursor.fetchall()


def fetch_selected_course(studentid, years, semester):
    query = """SELECT CourseID,CourseName,Sections.TimeSlotID,Building,RoomNo 
            FROM (Select Sections.CourseID,CourseName,TimeSlotID,Building,RoomNo,Sections.Semester,Sections.Years 
            From Sections Inner Join Courses On Sections.CourseID = Courses.CourseID) As Sections 
            Inner Join TimeSlot On Sections.TimeSlotID = TimeSlot.TimeSlotID WHERE courseid in 
            (SELECT CourseID FROM Takes WHERE StudentID = '{}' and years={} and semester={})
            and years={} and semester={} Order By Sections.TimeSlotID ASC;
            """.format(studentid, years, semester, years, semester)  # 合伴section and course,再結合該學生的takes,再抓出該學生修的課
    cursor.execute(query)
    return cursor.fetchall()


def is_course_exist(courseid):
    CourseID_query = "SELECT CourseID FROM Courses WHERE CourseID = '{}';".format(courseid)
    cursor.execute(CourseID_query)
    return cursor.fetchone() != None


def is_course_duplicate(studentid, courseid):
    query = """SELECT Coursename FROM Courses WHERE coursename IN 
            (SELECT DISTINCT coursename from takes INNER JOIN Courses 
            on takes.courseid = courses.courseid WHERE studentid = '{}')
            """.format(studentid)
    cursor.execute(query)
    for course in cursor.fetchall():
        # 檢查是否已選同名課程
        if get_course_name(courseid) == course:
            return True
    return False


def is_exceed_credits_limit(studentid, years, semester, courseid):
    current_total_credits = get_total_selected_credits(studentid, years, semester)
    return current_total_credits + get_course_credits(courseid) > 30


def is_course_schedule_conflict(studentid, courseid, years, semester):
    for schedule_timeslot in get_student_schedule(studentid, years, semester):
        for course_timeslot in get_course_schedule(courseid, years, semester):
            if schedule_timeslot == course_timeslot:
                return True
    return False


def is_course_full(courseid, years, semester):
    max_quota = get_course_max_quota(courseid, years, semester)
    current_takes = get_course_current_takes(courseid, years, semester)
    return current_takes >= max_quota


def is_not_in_queue(studentid, courseid):
    query = "Select * From CourseQueue Where StudentID = '{}' And CourseID = '{}';".format(studentid, courseid)
    cursor.execute(query)
    return cursor.fetchone() == None


def add_to_queue(studentid, courseid):
    if is_not_in_queue(studentid, courseid):
        query = "Insert Into CourseQueue Values('{}','{}','{}');".format(studentid, courseid, datetime.now())
        cursor.execute(query)
        conn.commit()


def unfollow_course(studentid, courseid):
    query = "Delete From Follows Where StudentID = '{}' And CourseID = '{}';".format(studentid, courseid)
    cursor.execute(query)
    conn.commit()

# 預選必修
def preselect_required_courses():
    if verify_is_new_semester(semester, years):
        # 抓取學生資料
        students = fetch_student_list(semester, years)
        # 根據每位學生的系所年紀班級，加入必修課程
        for StudentID, DepartmentName, ClassNo, StudentYear in students:
            for CourseID, TimeSlotID in get_student_required_courses(DepartmentName, StudentYear, ClassNo, years, semester):
                take_course_section(StudentID, CourseID, TimeSlotID, semester, years)


preselect_required_courses()


@app.route('/')
def start():
    return redirect(url_for('home'))


# 登入頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('studentid') and session.get('password'):
        studentid = session.get('studentid')
        if not verify_student(studentid):
            session['studentid'] = None
            return render_template('ErrorMessage.html', status=(("學號錯誤!", "login", "重新登入"),))
        if not verify_password(studentid, session.get('password')):
            session['password'] = None
            return render_template('ErrorMessage.html', status=(("請重新登入!", "login", "重新登入"),))
        return redirect(url_for('home'))
    session['studentid'] = None
    session['password'] = None
    return render_template('login.html')


# 主頁
@app.route('/home', methods=['GET', 'POST'])
def home():
    global studentid
    if not session.get('studentid'):
        # 檢查學號
        session['studentid'] = request.form.get('studentid')
        studentid = session.get('studentid')
        if studentid == '':
            return render_template('ErrorMessage.html', status=(("請輸入學號!", "login", "重新登入"),))
        elif studentid == None:
            return redirect(url_for('login'))

        # 檢查密碼
        password = request.form.get('password')
        if password == '':
            return render_template('ErrorMessage.html', status=(("請輸入密碼!", "login", "重新登入"),))
        elif password == None:
            return redirect(url_for('login'))

        # 密碼加密
        password = bcrypt.generate_password_hash(password=password)
        session['password'] = password

        if not verify_student(studentid):
            session['studentid'] = None
            return render_template('ErrorMessage.html', status=(("學號錯誤!", "login", "重新登入"),))
        if not verify_password(studentid, session.get('password')):
            session['password'] = None
            return render_template('ErrorMessage.html', status=(("密碼錯誤!", "login", "重新登入"),))
        session.permanent = True

    else:
        studentid = session.get('studentid')
        if not verify_student(studentid):
            session['studentid'] = None
            return render_template('ErrorMessage.html', status=(("學號錯誤!", "login", "重新登入"),))
        if not verify_password(studentid, session.get('password')):
            session['password'] = None
            return render_template('ErrorMessage.html', status=(("密碼錯誤!", "login", "重新登入"),))

    # 抓取已選總學分
    total_credits = get_total_selected_credits(studentid, years, semester)
    # 抓取學生名字
    studentName = get_student_name(studentid)
    # 抓取已關注課程
    followed_course = fetch_followed_course(studentid, years, semester)
    # 抓取已選課程
    selected_course = fetch_selected_course(studentid, years, semester)

    return render_template('home.html', studentName=studentName, sum_Credits=total_credits, section=selected_course, follows=followed_course)


# 登出頁面
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global studentid
    studentid = None
    session['studentid'] = None
    session['password'] = None
    return render_template('logout.html')


# 加選課程
@app.route('/add', methods=['GET', 'POST'])
def add():
    if not session.get('studentid'):
        return redirect(url_for('login'))
    else:
        global studentid
        studentid = session.get('studentid')
        if not verify_password(studentid, session.get('password')):
            return render_template('ErrorMessage.html', status=(("密碼錯誤!", "login", "重新登入"),))

    courseid = request.form.get('courseid')

    # 檢查是否有這堂課
    if not is_course_exist(courseid):
        return render_template('ErrorMessage.html', status=(("找不到這堂課", "home", "返回"),))

    # 找出已選的課程名稱
    if is_course_duplicate(studentid, courseid):
        return render_template('ErrorMessage.html', status=(("不可加選與已選課程同名的課程", "home", "返回"),))

    # 檢查加選後是否超出30學分
    if is_exceed_credits_limit(studentid, years, semester, courseid):
        return render_template('ErrorMessage.html', status=(("不可超過30學分", "home", "返回"),))

    # 檢查是否衝堂
    if is_course_schedule_conflict(studentid, courseid, years, semester):
        return render_template('ErrorMessage.html', status=(("不可加選衝堂的課程", "home", "返回"),))

    # 檢查是否人數已滿
    # 若人數已滿，加入排隊列表
    if is_course_full(courseid, years, semester):
        add_to_queue(studentid, courseid)
        return render_template('ErrorMessage.html', status=(("人數已滿，已加入排隊列表", "home", "返回"),))

    # 加選課程
    for TimeSlotID in get_course_schedule(courseid, years, semester):
        take_course_section(studentid, courseid, TimeSlotID, semester, years)

    unfollow_course(studentid, courseid)
    return render_template('ErrorMessage.html', status=(("加選成功", "home", "返回"),))


# 退選
@app.route('/drop', methods=['GET', 'POST'])
def drop():
    if not session.get('studentid'):
        return redirect(url_for('login'))
    else:
        global studentid
        studentid = session.get('studentid')
        if not verify_password(studentid, session.get('password')):
            return render_template('ErrorMessage.html', status=(("密碼錯誤!", "login", "重新登入"),))

    courseid = request.form.get('courseid')

    # 檢查是否已選此課程
    query = "SELECT CourseID FROM Courses WHERE courseid = '{}';".format(
        courseid)
    cursor.execute(query)
    course_id = cursor.fetchone()
    query = """SELECT CourseID FROM Courses WHERE courseID IN 
            (SELECT DISTINCT courseid from takes 
            WHERE studentid = '{}' and semester={} and years={});
            """.format(studentid, semester, years)  # 根據學生所選的課找出有沒有選這堂課
    cursor.execute(query)
    flag = 0  # 如果沒有在裡面就設零
    for course in cursor.fetchall():
        if course_id == course:  # 如果有flag=1
            flag = 1
    if flag == 0:
        return render_template('ErrorMessage.html', status=(("無此課程", "home", "返回"),))

    # 檢查是否該學生的必修課
    query = "SELECT CreditType from takes where courseid='{}' and studentid='{}';".format(
        courseid, studentid)
    cursor.execute(query)
    drop_Credits = cursor.fetchone()
    if drop_Credits[0] == "必修":
        return render_template('ErrorMessage.html', status=(("這是必修不可手動退選", "home", "返回"),))

    # 檢查退選後是否低於9學分
    query = """SELECT SUM(Credits) FROM Courses 
            WHERE CourseID in (SELECT DISTINCT CourseID FROM Takes
            WHERE StudentID = '{}' and years={} and semester={});
            """.format(studentid, years, semester)
    cursor.execute(query)
    sum_Credits = cursor.fetchone()
    query = "SELECT Credits FROM Courses WHERE CourseID = '{}';".format(
        courseid)
    cursor.execute(query)
    drop_Credits = cursor.fetchone()
    if sum_Credits[0] - drop_Credits[0] < 9:
        return render_template('ErrorMessage.html', status=(("不可少於9學分", "home", "返回"),))

    # 退選課程
    delete_query = """delete from Takes where studentid='{}' and courseid='{}' and semester={} and years={};
                    """.format(studentid, courseid, semester, years)
    cursor.execute(delete_query)
    conn.commit()

    # 依照預選此課的排隊列表（按時間順序）
    query = "Select StudentID From CourseQueue Where CourseID = '{}' Order By TimeQueue ASC;".format(
        courseid)
    cursor.execute(query)
    add_student = cursor.fetchall()
    # 加選最早排隊選課且符合加選規定的學生
    count = 0
    if add_student:  # 如果有人排隊就會進入迴圈
        while add_student[count]:
            flag = 0  # 有沒有符合規定（符合規定是0）
            # 檢查是否已選同名課程
            # 找出該課程代碼的課程名稱
            query = "SELECT CourseName FROM Courses WHERE courseid = '{}'".format(
                courseid)
            cursor.execute(query)
            course_name = cursor.fetchone()
            # 找出已選的課程名稱
            query = """SELECT Coursename FROM Courses WHERE coursename IN 
                    (SELECT DISTINCT coursename from takes INNER JOIN Courses 
                    on takes.courseid = courses.courseid WHERE studentid = '{}')
                    """.format(add_student[count][0])
            cursor.execute(query)
            for course in cursor.fetchall():
                if course_name == course:
                    flag = 1  # 不符合flag設為1

            # 檢查退選後是否超出30學分
            # 抓取總學分
            query = """SELECT SUM(Credits) FROM Courses WHERE CourseID in 
                    (SELECT DISTINCT CourseID FROM Takes WHERE StudentID = '{}' and years={} and semester={});
                    """.format(add_student[count][0], years, semester)
            cursor.execute(query)
            sum_Credits = cursor.fetchone()
            # 抓取加選課程學分
            query = "SELECT Credits FROM Courses WHERE CourseID = '{}';".format(
                courseid)
            cursor.execute(query)
            add_Credits = cursor.fetchone()
            if sum_Credits[0] + add_Credits[0] > 30:
                flag = 1

            # 檢查是否衝堂
            # 抓取該課程上課時間
            query = "SELECT TimeSlotID FROM Sections WHERE CourseID = '{}' and years={} and semester={}".format(
                courseid, years, semester)
            cursor.execute(query)
            course_timeslot = cursor.fetchall()
            # 抓取學生已選課表的上課時間
            query = "SELECT TimeSlotID from takes WHERE studentid = '{}' and years={} and semester={}".format(
                add_student[count][0], years, semester)
            cursor.execute(query)
            for schedule_timeslot in cursor.fetchall():
                for timeslot in course_timeslot:
                    if schedule_timeslot == timeslot:
                        flag = 1

            # 判斷是否不符合規定
            if flag == 1:
                count += 1
                continue

            # 最先符合規定的學生加選課程
            query = """SELECT TimeSlotID,Semester,Years FROM Sections
                    WHERE CourseID = '{}' and years={} and semester={}
                    """.format(courseid, years, semester)
            cursor.execute(query)
            for TimeSlotID, Semester, Years in cursor.fetchall():
                insert_query = """insert into Takes(StudentID,CourseID,TimeSlotID,Semester,Years)
                                values('{}','{}','{}',{},{});
                                """.format(add_student[count][0], courseid, TimeSlotID, Semester, Years)
                cursor.execute(insert_query)
                conn.commit()
            break
    return render_template('ErrorMessage.html', status=(("退選成功", "home", "返回"),))


# 顯示可選課程
@app.route('/course_list', methods=['GET', 'POST'])
def course_list():
    if not session.get('studentid'):
        return redirect(url_for('login'))
    else:
        global studentid
        studentid = session.get('studentid')
        if not verify_password(studentid, session.get('password')):
            return render_template('ErrorMessage.html', status=(("密碼錯誤!", "login", "重新登入"),))

    query = """Select Current.CourseID, CourseCode, CourseName, DepartmentName, Credits, CreditType, CurrentAmount, TotalAmount From 
            (Select Courses.CourseID, Courses.CourseCode, Courses.CourseName, Courses.DepartmentName, Courses.Credits, Courses.CreditType, 
            count(Distinct StudentID) As CurrentAmount From Courses Left Outer Join Takes On Courses.CourseID = Takes.CourseID 
            Where Courses.Semester = {} And Courses.Years = {} Group By Courses.CourseID) As Current Inner Join 
            (Select CourseID, Min(Capacity) As TotalAmount From Classrooms Inner Join Sections 
            On Classrooms.Building = Sections.Building And Classrooms.RoomNo = Sections.RoomNo Group By CourseID) As Max 
            On Current.CourseID = Max.CourseID;
            """.format(semester, years)
    cursor.execute(query)
    return render_template('List.html', course=cursor.fetchall())


# 關注課程
@app.route('/follow_course', methods=['GET', 'POST'])
def follow_course():
    if not session.get('studentid'):
        return redirect(url_for('login'))
    else:
        global studentid
        studentid = session.get('studentid')
        if not verify_password(studentid, session.get('password')):
            return render_template('ErrorMessage.html', status=(("密碼錯誤!", "login", "重新登入"),))

    courseid = request.form.get('courseid')
    query = "Select * From Follows Where StudentID = '{}' And CourseID = '{}';".format(
        studentid, courseid)
    cursor.execute(query)
    if cursor.fetchone() == None:
        query = "Insert Into Follows Values('{}','{}');".format(
            studentid, courseid)
        cursor.execute(query)
        conn.commit()
    return render_template('ErrorMessage.html', status=(("課程已關注", "course_list", "返回"),), home=('home'))


# 已關注課程頁面
@app.route('/follow_list', methods=['GET', 'POST'])
def follow_list():
    if not session.get('studentid'):
        return redirect(url_for('login'))
    else:
        global studentid
        studentid = session.get('studentid')
        if not verify_password(studentid, session.get('password')):
            return render_template('ErrorMessage.html', status=(("密碼錯誤!", "login", "重新登入"),))

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
            """.format(studentid, semester, years)
    cursor.execute(query)
    return render_template('Follow.html', course=cursor.fetchall())


# 取消關注
@app.route('/cancel_follow', methods=['GET', 'POST'])
def cancel_follow():
    if not session.get('studentid'):
        return redirect(url_for('login'))
    else:
        global studentid
        studentid = session.get('studentid')
        if not verify_password(studentid, session.get('password')):
            return render_template('ErrorMessage.html', status=(("密碼錯誤!", "login", "重新登入"),))

    courseid = request.form.get('courseid')
    unfollow_course(studentid, courseid)
    return render_template('ErrorMessage.html', status=(("課程已取消關注", "follow_list", "返回"),), home=('home'))
