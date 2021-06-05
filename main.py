from flask import Flask, render_template,request, redirect, session
import mysql.connector
import os
from flask_mail import Mail, Message


app = Flask(__name__)
app.secret_key=os.urandom(24)
conn = mysql.connector.connect(host="remotemysql.com",user="OiKrXs98JB",password="rHJz5kQMmM",database="OiKrXs98JB")
cursor=conn.cursor()


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "websight18092001@gmail.com"
app.config["MAIL_PASSWORD"] = "softwareprojecttest"
app.config["MAIL_DEFAULT_SENDER"] ="websight18092001@gmail.com"

mail=Mail(app)

def send_mail(recieve_mail=None):
   msg = Message('Confirmation Mail',sender ="websight18092001@gmail.com",recipients = list(recieve_mail))
   msg.body = 'Hello User! \n Copy paste this link: http://127.0.0.1:5000/complete_profile/{} in your browser to complete your profile.'.format(recieve_mail)
   if recieve_mail!= None:
       msg.add_recipient(recieve_mail)
   mail.send(msg)
   print("\n\n E-mail sent\n\n")

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/complete_profile')
def complete():
    return render_template('testtaker_profile.html')

@app.route('/dashboard_tt')
def dashboard_testtaker():
    if 'user_id' in session:
        return render_template('dashboard_taker.html')
    else:
        redirect('/')

@app.route('/choice')
def choice():
    return render_template('page_2.html')


@app.route('/signup_testmaker',methods=['POST'])
def signup():
    return render_template('signup.html')

@app.route('/signup_testtaker',methods=['POST'])
def signin():
    return render_template('signin.html')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('login_email')
    password=request.form.get('login_password')
    cursor.execute("""SELECT `user_id`,`tester_type` FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users=cursor.fetchall()
    print(users) 
    if len(users)>0:
        session['user_id']=users[0][0]
        if users[0][1]=='test_maker':
            cursor.execute("""SELECT * FROM `test` WHERE `user_id`='{}'""".format(str(users[0][0])))
            user=cursor.fetchall()
            return render_template('dashboard_testmaker.html',data=user,userid=users[0][0]) # redirect('/signup_to_make_test)
        elif users[0][1]=='test_taker':
            cursor.execute("""SELECT  `test_id`, `test_name` FROM `available_tests` WHERE `user_id`='{}'""".format(users[0][0]))
            avail=cursor.fetchall()
            cursor.execute("""SELECT `test_id`, `test_name` FROM `test` WHERE `test_id` IN (SELECT DISTINCT `test_id` FROM `test_answers` WHERE `user_id`='{}')""".format(str(users[0][0])))
            comple=cursor.fetchall()
            return render_template('dashboard_taker.html',available=avail,completed=comple)
    else:
        return redirect('/')

@app.route('/sign_up',methods=['POST'])
def sign_up():
    first_name=request.form.get('first_name')
    last_name=request.form.get('last_name')
    email=request.form.get('email')
    password=request.form.get('password')
    job_title=request.form.get('job_title')
    company=request.form.get('company')
    phone=request.form.get('phone_number')
    cursor.execute("""SELECT COUNT(`user_id`) FROM `users`""")
    user=cursor.fetchall()
    userid=user[0][0]
    userid=userid+1
    cursor.execute("""INSERT INTO `test_maker`(`user_id`, `first_name`, `last_name`, `email`, `password`, `job_title`, `company`, `phone_number`) VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(str(userid),first_name, last_name, email, password, job_title, company, phone))
    conn.commit()
    cursor.execute("""SELECT * FROM `test_maker` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    cursor.execute("""INSERT INTO `users`(`user_id`, `email`, `password`, `tester_type`) VALUES ('{}','{}','{}','test_maker')""".format(str(userid), email, password))
    conn.commit()
    print(myuser)
    if len(myuser)>0:
        session['user_id']=myuser[0][0]
        print(myuser[0][0])
        return render_template("dashboard_testmaker.html")

@app.route('/sign_in',methods=['POST'])
def sign_in():
    email=request.form.get('email')
    send_mail(email)
    return render_template('email.html',result=email)

@app.route('/logout_tt',methods=['POST'])
def logout_taker():
    session.pop('user_id')
    return redirect('/')

@app.route('/logout_tm',methods=['POST'])
def logout_maker():
    session.pop('user_id')
    return redirect('/')

@app.route('/complete_profile/<result>')
def feed_taker_profile(result):
    return render_template('testtaker_profile.html',mail=result)

@app.route('/comp_profile',methods=['POST'])
def feed_taker_input():
    name=request.form.get('name')
    age=request.form.get('age')
    email=request.form.get('email')
    password=request.form.get('password')
    income=request.form.get('income')
    gender=request.form.get('gender')
    country=request.form.get('country')
    web_expertise=request.form.get('web_expertise')
    emp_status=request.form.get('empstat')
    industry=request.form.get('indus')
    company_size=request.form.get('comp')
    job_role=request.form.get('job')
    job_level=request.form.get('joblevel')
    lang=request.form.get('lang')
    parental_status=request.form.get('parental')
    cursor.execute("""SELECT COUNT(`user_id`) FROM `users`""")
    user=cursor.fetchall()
    userid=user[0][0]
    userid=userid+1
    cursor.execute("""INSERT INTO `users`(`user_id`,`email`, `password`, `tester_type`) VALUES ('{}','{}','{}','test_taker')""".format(str(userid),email,password))
    conn.commit()
    cursor.execute("""SELECT `user_id` FROM `users` WHERE `email` LIKE '{}'""".format(email))
    user=cursor.fetchall()
    userid=user[0][0]
    cursor.execute("""INSERT INTO `test_taker`(`User_id`, `Name`, `Age`, `Password`, `Income`, `Gender`, `country`, `Web_Expertise`, `Emp_Status`, `Industry`, `Company_size`, `Job_Role`, `Job_level`, `Language`, `Parental_status`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(userid, name, age, password, income, gender, country, web_expertise,emp_status, industry, company_size, job_role, job_level,lang, parental_status))
    conn.commit()
    cursor.execute("""SELECT `test_id` FROM `audience` WHERE (`age_ll`<='{}' AND `age_ul`>='{}') AND (`income_ll`<='{}' AND `income_ul`>='{}') AND (`gender`='{}') AND (`company_size`='{}') AND (`Web_Expertise`='{}') AND (`Language`='{}') AND (`Parental_Control`='{}')""".format(str(age),str(age), str(income), str(income), gender, company_size, web_expertise, lang, parental_status))
    tests=cursor.fetchall()
    lis1=[]
    for i in tests:
        cursor.execute("""SELECT `{}` FROM `country` WHERE `country`='{}'""".format(str(i[0]),country))
        ans=cursor.fetchall()
        if ans[0][0]=='yes':
            lis1.append(i[0])
    lis2=[]
    for i in lis1:
        cursor.execute("""SELECT `{}` FROM `emp_stat` WHERE `emp_stat`='{}'""".format(str(i),emp_status))
        ans=cursor.fetchall()
        if ans[0][0]=='yes':
            lis2.append(i)
    lis3=[]
    for i in lis2:
        cursor.execute("""SELECT `{}` FROM `industry` WHERE `industry`='{}'""".format(str(i),industry))
        ans=cursor.fetchall()
        if ans[0][0]=='yes':
            lis3.append(i)
    lis4=[]
    for i in lis3:
        cursor.execute("""SELECT `{}` FROM `job_role` WHERE `job_role`='{}'""".format(str(i),job_role))
        ans=cursor.fetchall()
        if ans[0][0]=='yes':
            lis4.append(i)
    lis5=[]
    for i in lis4:
        cursor.execute("""SELECT `{}` FROM `job_level` WHERE `job_level`='{}'""".format(str(i),job_level))
        ans=cursor.fetchall()
        if ans[0][0]=='yes':
            lis5.append(i)
    print(lis5)
    for i in lis5:
        cursor.execute("""SELECT `test_name` FROM `test` WHERE `test_id`='{}'""".format(str(i)))
        testname=cursor.fetchall()
        cursor.execute("""INSERT INTO `available_tests`(`user_id`, `test_id`, `test_name`) VALUES ('{}','{}','{}')""".format(str(userid),str(i),testname[0][0]))
        conn.commit()
    cursor.execute("""SELECT  `test_id`, `test_name` FROM `available_tests` WHERE `user_id`='{}'""".format(str(userid)))
    avail=cursor.fetchall()
    cursor.execute("""SELECT `test_id`, `test_name` FROM `test` WHERE `test_id` IN (SELECT DISTINCT `test_id` FROM `test_answers` WHERE `user_id`='{}')""".format(str(userid)))
    comple=cursor.fetchall()
    return render_template('dashboard_taker.html',available=avail,completed=comple)



@app.route('/create_audience/<id1>',methods=['POST'])
def create_audience_page(id1):
    # pass testid as <id>
    cursor.execute("""SELECT COUNT(`test_id`) FROM `test`""")
    user=cursor.fetchall()
    testid=user[0][0]
    testid=testid+1
    cursor.execute("""INSERT INTO `test`(`user_id`, `test_id`) VALUES ('{}','{}')""".format(id1,str(testid)))
    return render_template('create_audience.html',testid=testid)
    

@app.route('/create_new_audience/<id>',methods=['POST'])
def create_new_audience(id):
    name=request.form.get('test_name')
    print(name)
    cursor.execute("""UPDATE `test` SET `test_name`='{}' WHERE `test_id` LIKE '{}'""".format(name,str(id)))
    conn.commit()
    participants=request.form.get('participants')
    device=request.form.get('device')
    age_ll=request.form.get('age_ll')
    age_ul=request.form.get('age_ul')
    income_ll=request.form.get('income_ll')
    income_ul=request.form.get('income_ul')
    gender=request.form.get('gender')          
    country=request.form.getlist('country')
    web_expertise=request.form.get('web_expertise')
    emp_status=request.form.getlist('empstat')
    industry=request.form.getlist('indus')
    company_size=request.form.get('comp')
    job_role=request.form.getlist('job')
    job_level=request.form.getlist('joblevel')
    # social=request.form.getlist('social')
    language=request.form.get('lang')
    parental=request.form.get('parental')
    OS=request.form.get("OS")
    browser=request.form.get("browser")
    OR=request.form.get("OR")
    print(country)
    cursor.execute("""INSERT INTO `audience`(`test_id`, `participants`, `device`,`age_ll`, `age_ul`, `income_ll`, `income_ul`, `gender`,`Web_Expertise`, `Language`, `Parental_Control`,`company_size`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(id, participants,device,age_ll,age_ul,income_ll,income_ul,gender,web_expertise,language,parental,company_size))
    conn.commit() 
    cursor.execute("""ALTER TABLE `country` ADD `{}` VARCHAR(50) """.format(str(id)))
    conn.commit()
    for i in country:
        cursor.execute("""UPDATE `country` SET `{}`='yes' WHERE `country`='{}'""".format(str(id),i))
        conn.commit()
    cursor.execute("""ALTER TABLE `emp_stat` ADD `{}` VARCHAR(50) """.format(str(id)))
    conn.commit()
    for i in emp_status:
        cursor.execute("""UPDATE `emp_stat` SET `{}`='yes' WHERE `emp_stat`='{}'""".format(str(id),i))
        conn.commit()
    cursor.execute("""ALTER TABLE `industry` ADD `{}` VARCHAR(50) """.format(str(id)))
    conn.commit()
    for i in industry:
        cursor.execute("""UPDATE `industry` SET `{}`='yes' WHERE `industry`='{}'""".format(str(id),i))
        conn.commit()
    cursor.execute("""ALTER TABLE `job_level` ADD `{}` VARCHAR(50) """.format(str(id)))
    conn.commit()
    for i in job_level:
        cursor.execute("""UPDATE `job_level` SET `{}`='yes' WHERE `job_level`='{}'""".format(str(id),i))
        conn.commit()
    cursor.execute("""ALTER TABLE `job_role` ADD `{}` VARCHAR(50) """.format(str(id)))
    conn.commit()
    for i in job_role:
        cursor.execute("""UPDATE `job_role` SET `{}`='yes' WHERE `job_role`='{}'""".format(str(id),i))
        conn.commit()
    cursor.execute("""ALTER TABLE `web_browser` ADD `{}` VARCHAR(50) """.format(str(id)))
    conn.commit()
    for i in browser:
        cursor.execute("""UPDATE `web_browser` SET `{}`='yes' WHERE `browser`='{}'""".format(str(id),i))
        conn.commit()
    cursor.execute("""INSERT INTO `screener_1`(`test_id`, `other_rqts`, `OS`) VALUES ('{}','{}','{}')""".format(str(id),OR,OS))
    conn.commit()
    cursor.execute("""SELECT `User_id` FROM `test_taker` WHERE (`Age` BETWEEN '{}' AND '{}') AND (`Income` BETWEEN '{}' AND '{}') AND (`Gender`='{}') AND (`country` IN (SELECT `country` FROM `country` WHERE `{}`='yes')) AND (`Web_Expertise`='{}') AND (`Emp_Status` IN (SELECT `emp_stat` FROM `emp_stat` WHERE `{}`='yes')) AND (`Industry` IN (SELECT `industry` FROM `industry` WHERE `{}`='yes'))AND  (`Company_size`='{}') AND (`Job_Role` IN (SELECT `job_role` FROM `job_role` WHERE `{}`='yes')) AND (`Job_level` IN (SELECT `job_level` FROM `job_level` WHERE `{}`='yes')) AND (`Language`='{}') AND (`Parental_status`='{}')""".format(age_ll,age_ul,income_ll,income_ul, gender, str(id), web_expertise, str(id), str(id), company_size,  str(id), str(id),language,parental))
    takers=cursor.fetchall()
    for i in takers:
        cursor.execute("""INSERT INTO `available_tests`(`user_id`, `test_id`, `test_name`) VALUES ('{}','{}','{}')""".format(str(i[0]),str(id),name)) 
        conn.commit()
    return render_template("screener.html",testid=id)

@app.route('/added_tasks/<id>',methods=['POST'])
def added_tasks(id):
    tasks=request.form.getlist('task')
    print(tasks)
    for i in tasks:
        cursor.execute("""SELECT COUNT(*) FROM `tasks` WHERE  `test_id` LIKE '{}'""".format(str(id)))
        task=cursor.fetchall()
        taskid=task[0][0]
        taskid=taskid+1
        cursor.execute("""INSERT INTO `tasks`(`test_id`, `task_no`, `task`) VALUES ('{}','{}','{}')""".format(str(id),str(taskid),str(i)))
        conn.commit()
    cursor.execute("""SELECT `user_id` FROM `test` WHERE `test_id`='{}'""".format(str(id)))
    user=cursor.fetchall()
    userid=user[0][0]
    cursor.execute("""SELECT * FROM `test` WHERE `user_id`='{}'""".format(str(userid)))
    user=cursor.fetchall()
    print(user)
    return render_template("dashboard_testmaker.html",data=user)

@app.route('/create_screener/<id>',methods=['POST'])
def add_screener(id):
    question=request.form.getlist("question")
    mcq1=request.form.getlist("mcq1")
    acc_1=request.form.getlist("acc_1")
    mcq2=request.form.getlist("mcq2")
    acc_2=request.form.getlist("acc_2")
    mcq3=request.form.getlist("mcq3")
    acc_3=request.form.getlist("acc_3")
    mcq4=request.form.getlist("mcq4")
    acc_4=request.form.getlist("acc_4")
    print(question)
    print(mcq1)
    print(acc_1)
    print(mcq3)
    print(acc_3)
    n=len(question)
    for i in range(n):
        cursor.execute("""INSERT INTO `screener_2`(`screener_id`, `screener_qno`, `screener_quest`, `mcq1`, `acc_1`, `mcq2`, `acc_2`, `mcq_3`, `acc_3`, `mcq_4`, `acc_4`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(str(id),str(i),question[i],mcq1[i],acc_1[i],mcq2[i],acc_2[i],mcq3[i],acc_3[i],mcq4[i],acc_4[i]))
        conn.commit()
    return render_template('task.html',testid=id)

@app.route('/screener_test/<id>',methods=['POST'])
def show_screener(id):
    cursor.execute("""SELECT `other_rqts`, `OS` FROM `screener_1` WHERE `test_id`='{}'""".format(str(id)))
    screener1=cursor.fetchall()
    cursor.execute("""SELECT `browser` FROM `web_browser` WHERE `{}`='yes'""".format(str(id)))
    browser=cursor.fetchall()
    cursor.execute("""SELECT `screener_quest`, `mcq1`,`mcq2`,`mcq_3`, `mcq_4`  FROM `screener_2` WHERE `screener_id`='{}'""".format(str(id)))
    screener2=cursor.fetchall()
    print(screener2)
    n=len(screener2)
    return render_template('screener_test.html',id=id,screener1=screener1,screener2=screener2,browser=browser,n=range(n))
    


@app.route('/screener_over/<id>',methods=['POST'])
def screener_over(id):
    screener1=request.form.get('reqt_ans')
    screener2=request.form.getlist('screener_answers')
    cursor.execute("""SELECT `acc_1`,  `acc_2`, `acc_3`, `acc_4` FROM `screener_2` WHERE `screener_id`='{}'""".format(str(id)))
    answers=cursor.fetchall()
    output=[]
    for i in answers:
        for j in i:
            output.append(j)
    if output == screener2 and screener1=='yes':
        cursor.execute("""SELECT `task_no`,`task` FROM `tasks` WHERE `test_id`='{}' AND `task_no`='1'""".format(str(id)))
        tasks=cursor.fetchall()
        print(tasks)
        cursor.execute("""SELECT `user_id` FROM `available_tests` WHERE `test_id`='{}'""".format(str(id)))
        users=cursor.fetchall()
        cursor.execute("""SELECT `task` FROM `tasks` WHERE `test_id`='{}'""".format(str(id)))
        taskn=cursor.fetchall()
        if(len(taskn)==1):
            end='no'
        else:
            end='null'
        return render_template('test_page.html',testid=id,tasks=tasks[0],userid=users[0][0],taskno=1,end=end)
    else:
        cursor.execute("""SELECT `user_id` FROM `available_tests` WHERE `test_id`='{}'""".format(str(id)))
        users=cursor.fetchall()
        cursor.execute("""SELECT  `test_id`, `test_name` FROM `available_tests` WHERE `user_id`='{}'""".format(users[0][0]))
        avail=cursor.fetchall()
        cursor.execute("""SELECT `test_id`, `test_name` FROM `test` WHERE `test_id` IN (SELECT DISTINCT `test_id` FROM `test_answers` WHERE `user_id`='{}')""".format(str(users[0][0])))
        comple=cursor.fetchall()
        return render_template('dashboard_taker.html',available=avail,completed=comple)
    
# @app.route('/edittest/<id>')
# def edit_test(id):
# write function for editing the test and deleting it

@app.route('/tasks_over/<id1>/<id2>',methods=['POST'])
def task_answers(id1,id2):
    id3=int(request.form.get('taskno'))
    success=request.form.get("success")
    difficulty=request.form.get("difficult")
    print(success)
    print(difficulty)
    cursor.execute("""INSERT INTO `test_answers`(`test_id`, `task_no`, `success`, `difficulty`, `user_id`) VALUES ('{}','{}','{}','{}','{}')""".format(str(id1),str(id3),success,str(difficulty),str(id2)))
    conn.commit()
    cursor.execute("""SELECT `user_id` FROM `available_tests` WHERE `test_id`='{}'""".format(str(id1)))
    users=cursor.fetchall()
    id3=id3+1
    cursor.execute("""SELECT `task_no`,`task` FROM `tasks` WHERE `test_id`='{}' AND `task_no`='{}'""".format(str(id1),str(id3)))
    tasks=cursor.fetchall()
    cursor.execute("""SELECT `task` FROM `tasks` WHERE `test_id`='{}'""".format(str(id1)))
    taskn=cursor.fetchall()
    if(len(taskn)>(id3)):
        end='null'
        return render_template('test_page.html',testid=id1,tasks=tasks[0],userid=id2,taskno=id3,end=end)
    elif(len(taskn)==(id3)):
        end='no'
        return render_template('test_page.html',testid=id1,tasks=tasks[0],userid=id2,taskno=id3,end=end)


@app.route('/test_over/<id1>/<id2>',methods=['POST'])
def test_over(id1,id2):
    id3=int(request.form.get('taskno'))
    success=request.form.get("success")
    difficulty=request.form.get("difficult")
    print(success)
    print(difficulty)
    cursor.execute("""INSERT INTO `test_answers`(`test_id`, `task_no`, `success`, `difficulty`, `user_id`) VALUES ('{}','{}','{}','{}','{}')""".format(str(id1),str(id3),success,str(difficulty),str(id2)))
    conn.commit()
    cursor.execute("""DELETE FROM `available_tests` WHERE `available_tests`.`user_id` = '{}' AND `available_tests`.`test_id` = '{}'""".format(str(id2),str(id1)))
    conn.commit()
    cursor.execute("""SELECT  `test_id`, `test_name` FROM `available_tests` WHERE `user_id`='{}'""".format(str(id2)))
    avail=cursor.fetchall()
    print(avail)
    cursor.execute("""SELECT `test_id`, `test_name` FROM `test` WHERE `test_id` = (SELECT DISTINCT `test_id` FROM `test_answers` WHERE `user_id`='{}')""".format(str(id2)))
    comple=cursor.fetchall()
    return render_template('dashboard_taker.html',userid=str(id2),available=avail,completed=comple) 


@app.route('/result/<id>',methods=['POST'])
def result(id):
    cursor.execute("""SELECT COUNT(`test_id`) FROM `tasks` WHERE test_id='{}'""".format(str(id)))
    number=cursor.fetchall()
    n=int(number[0][0])
    succ_no_task=[]
    final1=[]
    for i in range(1,n+1):
        cursor.execute("""SELECT DISTINCT `success`, count(`success`) FROM `test_answers` where `task_no`='{}' group by `success`""".format(str(i),str(id)))
        success=cursor.fetchall()
        print(success)
        semifinal=[0,0,0,0,0,0,0]
        for a in success:
            if a[0]=="success1":
                semifinal[0]=a[1]
            elif a[0]=="success2":
                semifinal[1]=a[1]
            elif a[0]=="success3":
                semifinal[2]=a[1]
            elif a[0]=="success4":
                semifinal[3]=a[1]
            elif a[0]=="success5":
                semifinal[4]=a[1]
            elif a[0]=="success6":
                semifinal[5]=a[1]
            elif a[0]=="success7":
                semifinal[6]=a[1]
        final1.append(semifinal)
    final2=[]
    for i in range(1,n+1):
        cursor.execute("""SELECT DISTINCT `difficulty`, count(`difficulty`) FROM `test_answers` where `task_no`='{}' and `test_id`='{}' group by `difficulty`""".format(str(i),str(id)))
        difficulty=cursor.fetchall()
        semifinal=[0,0,0,0,0,0,0,0,0,0]
        print(difficulty)
        for a in difficulty:
            semifinal[a[0]-1]=a[1]            
        final2.append(semifinal)
    print(final1)
    print(final2)
    cursor.execute("""SELECT `task_no`,`task` FROM `tasks` WHERE `test_id`='{}'""".format(str(id)))
    tasks=cursor.fetchall()
    print(tasks)
    tasklist=[]
    for i in tasks:
        task=[i[0],i[1]]
        tasklist.append(task)
    print(tasklist)
    b=[]
    for i in range(n):
        sum1=final1[i][0]+final1[i][1]+final1[i][2]+final1[i][3]+final1[i][4]+final1[i][5]+final1[i][6]
        sum1=sum1/100
        sum2=final2[i][0]+final2[i][1]+final2[i][2]+final2[i][3]+final2[i][4]+final2[i][5]+final2[i][6]+final2[i][7]+final2[i][8]+final2[i][9]
        sum2=sum2/100
        av=[tasklist[i][0],tasklist[i][1],final1[i][0]/sum1,final1[i][1]/sum1,final1[i][2]/sum1,final1[i][3]/sum1,final1[i][4]/sum1,final1[i][5]/sum1,final1[i][6]/sum1,final2[i][0]/sum2,final2[i][1]/sum2,final2[i][2]/sum2,final2[i][3]/sum2,final2[i][4]/sum2,final2[i][5]/sum2,final2[i][6]/sum2,final2[i][7]/sum2,final2[i][8]/sum2,final2[i][9]/sum2]
        b.append(av)
    print(b)
    return render_template('result.html',result=b)




    
    


if __name__=="__main__":
    app.run(debug=True)

