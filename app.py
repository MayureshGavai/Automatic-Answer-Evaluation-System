from nltk.corpus import wordnet
import string
from nltk.corpus import stopwords
from email import charset
from unittest import result
from flask import Flask, render_template, redirect, request
from flask import Flask, render_template, request, session, url_for, redirect, jsonify, make_response, flash, session
import pymysql
#import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import os
from nltk.stem.wordnet import WordNetLemmatizer
import requests
#import pdfplumber
import re
import logging
import sys
# import PyPDF2
# =========================
from werkzeug.utils import secure_filename
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import language_tool_python
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import pickle

UPLOAD_FOLDER = 'static/upload_img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'docs'}
UPLOAD_FOLDER_2 = 'static/upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_2'] = UPLOAD_FOLDER_2
app.secret_key = 'random string'

stop_words = set(stopwords.words("english"))
punc = string.punctuation


def remove_stopwords(data):
    output_array = []
    for sentence in data:
        temp_list = []
        for word in sentence.split():
            if word.lower() not in stop_words:
                temp_list.append(word)
        output_array.append(' '.join(temp_list))
    return output_array


def remove_punc(data):
    output_array = []
    for sentence in data:
        temp_list = []
        for word in nltk.word_tokenize(sentence):
            if word not in punc:
                temp_list.append(word)
        output_array.append(' '.join(temp_list))
    return output_array


def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def lemmatization(data):
    output_array = []
    for sentence in data:
        temp_list = []
        for word in sentence.split():
            word = word.lower()
            from nltk.stem import WordNetLemmatizer
            lemma = WordNetLemmatizer()
            new_word = lemma.lemmatize(word, get_wordnet_pos(word))
            # print(new_word)
            temp_list.append(new_word)
        output_array.append(' '.join(temp_list))
    return output_array


def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root",
                                 database="qanlp", charset='utf8', use_unicode=True)
    return connection

# close DB connection


def dbClose():
    dbConnection().close()
    return

# logout code


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/studentlogin', methods=["GET", "POST"])
def studentlogin():
    msg = ''
    if request.method == "POST":
        # session.pop('user',None)
        email = request.form.get("email")
        password = request.form.get("pass")
        # print(mobno+password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM student WHERE email = %s AND pass = %s',
                                      (email, password))
        res = cursor.fetchone()
        if result_count > 0:
            print(result_count)
            session['name'] = res[1]
            session['id'] = res[0]
            session['user'] = email
            return redirect(url_for('studenthome'))
        else:
            print(result_count)
            msg = 'Incorrect username/password!'
    return render_template('studentlogin.html')


@app.route('/teacherlogin', methods=["GET", "POST"])
def teacherlogin():
    msg = ''
    if request.method == "POST":
        # session.pop('user',None)
        email = request.form.get("email")
        password = request.form.get("pass")
        # print(mobno+password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM teacher WHERE email = %s AND password = %s',
                                      (email, password))
        print("hello")
        print(result_count)
        if result_count > 0:
            print(result_count)
            session['user'] = email
            return redirect(url_for('teacherhome'))
        else:
            print(result_count)
            msg = 'Incorrect username/password!'
            return msg
        # dbClose()
    return render_template('teacherlogin.html')


@app.route('/teacherhome')
def teacherhome():
    if 'user' in session:
        return render_template('teacherhome.html')
    return render_template('teacherhome.html')


@app.route('/imgmarks', methods=["GET", "POST"])
def imgmarks():
    if 'user' in session:
        if request.method == "POST":
            studid = request.form.get("studid")
            imgnam = request.form.get("imgnam")
            mrks = request.form.get("marks")

            conn = dbConnection()
            curs = conn.cursor()
            sql = "SELECT pred_marks FROM marks WHERE sid=%s;"
            val = (studid)
            curs.execute(sql, val)
            res = curs.fetchone()
            result = list(res)
            print("printing result for pred marks")
            print(result)

            pred_mrk = []
            for i in result:
                a = int(i)
                print()
                print("printing a")
                print(a)
                pred_mrk.append(a)

            final_marks = pred_mrk[0]+int(mrks)
            print()
            print("printing final marks")
            print(final_marks)

            sql2 = "UPDATE marks set final_marks=%s where sid=%s"
            val2 = (str(final_marks), str(studid))
            curs.execute(sql2, val2)
            conn.commit()

            final_mrk = "Already image marks given to student"
            sql2 = "UPDATE answers set marks_given_not=%s where sid=%s"
            val2 = (str(final_mrk), str(studid))
            curs.execute(sql2, val2)
            conn.commit()

        return redirect(url_for('studentmarks'))
    return render_template('teacherhome.html')


@app.route('/createtest')
def createtest():
    if 'user' in session:
        return render_template('createtest.html')
    return render_template('createtest.html')


@app.route('/setquestion', methods=["GET", "POST"])
def setquestion():
    if 'user' in session:
        if request.method == "POST":
            # question1=request.form.get("question1")
            # answer1=request.form.get('description1')
            # question2=request.form.get('question2')
            # answer2=request.form.get('description2')
            # question3=request.form.get("question3")
            # answer3=request.form.get('description3')
            # question4=request.form.get("question4")
            # answer4=request.form.get('description4')
            # question5=request.form.get("question5")
            # answer5=request.form.get('description5')
            con = dbConnection()
            cursor = con.cursor()
            cursor.execute("delete FROM teacherquestion;")

            for i in range(1, 6):
                # question=''
                # answer=''
                question = request.form.get("question"+str(i))
                print(question)
                answer = request.form.get("description"+str(i))
                print(answer)

                sql = "INSERT INTO teacherquestion (question,answer) VALUES (%s, %s)"
                val = (question, answer)
                cursor.execute(sql, val)
                con.commit()
                print('success')
        return render_template('createtest.html')

    return render_template('createtest.html')


@app.route('/studentregister', methods=["GET", "POST"])
def studentregister():
    if request.method == "POST":
        try:
            status = ""
            name = request.form.get("name")
            mobile = request.form.get("mobile")
            mailid = request.form.get("email")
            pass1 = request.form.get("pass")

            print(name, mobile, mailid, pass1)

            con = dbConnection()
            cursor = con.cursor()
            cursor.execute('SELECT * FROM student WHERE mobile = %s', (mobile))
            res = cursor.fetchone()
            print(res)
            if not res:
                sql = "INSERT INTO student (name, mobile, email, pass) VALUES (%s, %s, %s, %s)"
                val = (name, str(mobile), mailid, pass1)
                cursor.execute(sql, val)
                con.commit()
                print("hii After commit")
                status = "success"
                print(status)
                return redirect(url_for('studentlogin'))
            else:
                status = "Already available"
            return status
        except:
            print("Exception occured at user registration")
            return redirect(url_for('index'))
        finally:
            dbClose()
    return render_template('studentregister.html')


@app.route('/studenthome')
def studenthome():
    if 'user' in session:

        return render_template('studenthome.html')
    return render_template('studenthome.html')


@app.route('/studentmarks')
def studentmarks():
    if 'user' in session:
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute("select * from marks")
        result = cursor.fetchall()  # data from database

        cursor.execute("select sid, img, marks_given_not from answers")
        result1 = cursor.fetchall()  # data from database
        result1 = list(result1)
        print(result1)
        sid = []
        fmarks = []
        imgs = []
        for i in result1:
            a = i[0]
            sid.append(a)

            b = i[1]
            imgs.append(b)

            c = i[2]
            print("printng c")
            print(c)
            if c==None:
                fmrk = "Marks not given"
                fmarks.append(fmrk)
            else:
                fmarks.append(c)

        import numpy as np
        unique_img = np.unique(imgs)
        
        unique_ids = np.unique(sid)

        unique_marks = np.unique(fmarks)

        flst = zip(unique_ids, unique_img,unique_marks)

        return render_template("studentmarks.html", result=result, flst=flst, fmarks=fmarks)
    return render_template('studentmarks.html')


@app.route('/givetest', methods=["GET", "POST"])
def givetest():
    if 'user' in session:
        con = dbConnection()
        cursor = con.cursor()

        cursor.execute("SELECT * FROM teacherquestion")
        result = cursor.fetchall()
        teacher_ans = []

        for i in result:
            print("######## Resut ############")
            print(i)
            a = i[2]
            teacher_ans.append(a)

        student_ans = []

        sql = "SELECT * from teacherquestion"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(type(res))
        cursor.execute('SELECT * FROM student WHERE name=%s',
                       (str(session['name'])))
        cursor.execute('SELECT * FROM student WHERE id=%s',
                       (str(session['id'])))
        if request.method == "POST":
            for i in range(1, 6):
                answer = request.form.get("description"+str(i))
                student_ans.append(answer)

                sql = "INSERT INTO answers (sid ,answers) VALUES (%s,%s)"
                val = ((session['id']), answer)
                cursor.execute(sql, val)
                con.commit()

            fl = request.files['file']
            filename_secure = secure_filename(fl.filename)
            print(filename_secure)
            fl.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_secure))
            print("print saved")
            filename = os.path.abspath(
                app.config['UPLOAD_FOLDER']+"//"+filename_secure)
            filename1 = filename_secure
            print(filename1)

            sql = "update answers set img=%s where sid=%s"
            val = (filename1, (session['id']))
            cursor.execute(sql, val)
            con.commit()

            cursor.execute(
                "select answers from answers where sid="+str(session['id']))
            stud = cursor.fetchall()
            cursor.execute('SELECT answer from teacherquestion')
            teach = cursor.fetchall()
            stud1 = []
            for l in stud:
                stud1.append(l[0])
            teach1 = []
            for k in teach:
                teach1.append(k[0])

            ########################### fuzzy wuzzyy ######################################
            print(teach1)
            print(stud1)
            output1 = remove_stopwords(teach1)
            output2 = remove_stopwords(stud1)
            output3 = remove_punc(output1)
            output4 = remove_punc(output2)
            output5 = lemmatization(output3)
            output6 = lemmatization(output4)
            marks = []
            finalmarks = []
            print(output3)
            print(output4)
            print(output5)
            print(output6)
            for i in range(len(teach)):
                m = output5[i]
                n = output6[i]
                print(m)
                print(n)
                from fuzzywuzzy import fuzz
                c = fuzz.ratio(output5[i], output6[i])
                # d=fuzz.token_set_ratio(output6[i],output5[i])
                print(c)
                # print(d)
                a = c/50
                print(a)
                finalmarks.append(a)
            finalmarks
            a = finalmarks[0]
            b = finalmarks[1]
            c = finalmarks[2]
            d = finalmarks[3]
            e = finalmarks[4]
            for i in finalmarks:
                a = i
            total = 0
            for ele in range(0, len(finalmarks)):
                print(ele)
                total = total + finalmarks[ele]
            import math
            print()
            print("printing total")
            print(total)
            ma = math.ceil(total)
            print()
            print("printing ma")
            print(ma)

            ans_ratio1 = fuzz.ratio(teacher_ans[0], student_ans[0])
            ans_ratio2 = fuzz.ratio(teacher_ans[1], student_ans[1])
            ans_ratio3 = fuzz.ratio(teacher_ans[2], student_ans[2])
            ans_ratio4 = fuzz.ratio(teacher_ans[3], student_ans[3])
            ans_ratio5 = fuzz.ratio(teacher_ans[4], student_ans[4])
            print(ans_ratio1, "\n", ans_ratio2, "\n", ans_ratio3,
                  "\n", ans_ratio4, "\n", ans_ratio5, "\n")

            print(ma)
            final_fuzz_marks = ma
            ################### grammer part #######################################

            mistake_lst = []
            tool = language_tool_python.LanguageTool('en-US')

            # get the matches
            mtch = []
            for i in student_ans:
                matches = tool.check(i)
                print()
                print("printing matches")
                print(matches)
                print()
                mtch.append(matches)

            lst = []
            for i in mtch:
                #     print(i)
                lst.append(i)

            import pandas
            import pandas as pd
            l1 = []
            for i in lst:
                k1 = pandas.DataFrame(i[:], columns=['ruleId', 'message', 'replacements', 'offsetInContext',
                                      'context', 'offset', 'errorLength', 'category', 'ruleIssueType', 'sentence'])
                l1.append(k1)
            df1 = l1[0]
            df2 = l1[1]
            df3 = l1[2]
            df4 = l1[3]
            df5 = l1[4]

            print()
            print("prinitgn l1:")
            print(l1)
            print()
            gram_marks = []
            for i in lst:
                a = len(i)
                fmarks = round(10-a*0.5)
                gram_marks.append(fmarks)
            final_gram_marks = sum(gram_marks)

            df1 = l1[0]
            df2 = l1[1]
            df3 = l1[2]
            df4 = l1[3]
            df5 = l1[4]

            #################################### cosine similarity ###############################
            # Cosine similarity
            count_vect = CountVectorizer()
            both_ans = zip(teacher_ans, student_ans)

            cosim_score = []
            for tecans, studans in both_ans:
                corpus = [tecans, studans]

                X_train_counts = count_vect.fit_transform(corpus)

                pd.DataFrame(X_train_counts.toarray(), columns=count_vect.get_feature_names(
                ), index=['Document 1', 'Document 2'])

                from sklearn.feature_extraction.text import TfidfVectorizer
                vectorizer = TfidfVectorizer()

                trsfm = vectorizer.fit_transform(corpus)
                pd.DataFrame(trsfm.toarray(), columns=vectorizer.get_feature_names(), index=[
                             'Document 1', 'Document 2'])

                sim_score = cosine_similarity(trsfm[0:1], trsfm)
                cosim_score.append(round(sim_score[0][1]*100, 2))

            print(cosim_score)
            sim1 = cosim_score[0]
            sim2 = cosim_score[1]
            sim3 = cosim_score[2]
            sim4 = cosim_score[3]
            sim5 = cosim_score[4]

            mar = []
            for i in cosim_score:
                a = i/10
                mar.append(a)
            total = 0
            for ele in range(0, len(mar)):
                total = total + mar[ele]
                print(total)

            import math
            print()
            print("printing total")
            print(total)
            ma = math.ceil(total)
            final_cosim_marks = ma

            ########################################### answer length ########################################
            stud_ans_len = []
            for i in student_ans:
                a = len(i)
                stud_ans_len.append(a)

            teach_ans_lngth = []
            for i in teacher_ans:
                a = len(i)
                teach_ans_lngth.append(a)

            len_lst = zip(teach_ans_lngth, stud_ans_len)

            mar_lst = []
            for i, j in len_lst:
                #     print(i-j)
                if (i-j) <= 150:
                    mar_lst.append(1)
                elif (i-j) > 150 and (i-j) <= 300:
                    mar_lst.append(2)
                elif (i-j) > 300 and (i-j) <= 450:
                    mar_lst.append(3)
                elif (i-j) > 600 and (i-j) <= 600:
                    mar_lst.append(4)
                else:
                    mar_lst.append(5)
            final_length_marks = sum(mar_lst)

            ######################################### Marks prediction ###############################
            df = pd.DataFrame(list(zip(str(final_fuzz_marks), str(final_gram_marks), str(final_cosim_marks), str(
                final_length_marks))), columns=["fuzzywuzzy_marks", "Grammer_marks", "cosine_similarity_marks", "Answer_len_marks"])

            with open(r"model/linear_pickle.pkl", "rb") as f:
                lrmodel = pickle.load(f)

            lrpred = lrmodel.predict(df)
            final_pred = int(round(lrpred[0]))
            ######################################### append all marks in database ###############################

            con = dbConnection()
            cursor = con.cursor()
            print()
            print()
            sql1 = "INSERT INTO marks (sid,studname,q1,q2,q3,q4,q5,final_fuzz_marks,final_gram_marks,final_cosim_marks,final_length_marks,pred_marks) VALUES (%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val2 = (str(session['id']), str(session['name']), str(a), str(b), str(c), str(d), str(e), str(
                final_fuzz_marks), str(final_gram_marks), str(final_cosim_marks), str(final_length_marks), str(final_pred))
            cursor.execute(sql1, val2)

            sql3 = "INSERT INTO fuzzy_wuzzy (sid,ans1_ratio,ans2_ratio,ans3_ratio,ans4_ratio,ans5_ratio) VALUES (%s,%s,%s, %s,%s,%s)"
            val3 = (str(session['id']), str(ans_ratio1), str(ans_ratio2), str(
                ans_ratio3), str(ans_ratio4), str(ans_ratio5))
            cursor.execute(sql3, val3)
            con.commit()

            con = dbConnection()
            cur = con.cursor()
            usrname = session.get('name')
            print()
            print("printing usrname: ", usrname)
            print()
            sql = 'SELECT studname,q1,q2,q3,q4,q5,final_fuzz_marks,final_gram_marks,final_cosim_marks,final_length_marks,pred_marks FROM marks where studname=%s ORDER BY id DESC LIMIT 1'
            val = (usrname)
            cur.execute(sql, val)
            fresult = cur.fetchall()
            print()
            print("printing fresult: ", fresult)
            print()
            fresult = list(fresult)
            studname = []
            ques1 = []
            ques2 = []
            ques3 = []
            ques4 = []
            ques5 = []
            fuzmark = []
            gramark = []
            cosinmark = []
            lenmark = []
            predmark = []

            for i in fresult:
                a = i[0]
                studname.append(a)

                b = i[1]
                ques1.append(b)

                c = i[2]
                ques2.append(c)

                d = i[3]
                ques3.append(d)

                e = i[4]
                ques4.append(e)

                f = i[5]
                ques5.append(f)

                g = i[6]
                fuzmark.append(g)

                h = i[7]
                gramark.append(h)

                j = i[8]
                cosinmark.append(j)

                k = i[9]
                lenmark.append(k)

                l = i[10]
                predmark.append(l)

            flst = zip(studname, ques1, ques2, ques3, ques4, ques5,
                       fuzmark, gramark, cosinmark, lenmark, predmark)

            return render_template('page.html', tables1=[df1.to_html(classes='female')], titles1=df1.columns.values, sim1=sim1, sim2=sim2, sim3=sim3, sim4=sim4, sim5=sim5, lngth1=stud_ans_len[0], lngth2=stud_ans_len[1], lngth3=stud_ans_len[2], lngth4=stud_ans_len[3], lngth5=stud_ans_len[4], name=session['name'], mistake_lst=mistake_lst, ans_ratio1=ans_ratio1, ans_ratio2=ans_ratio2, ans_ratio3=ans_ratio3, ans_ratio4=ans_ratio4, ans_ratio5=ans_ratio5,
                                   tables2=[df2.to_html(classes='female')], titles2=df2.columns.values,
                                   tables3=[df3.to_html(classes='female')], titles3=df3.columns.values,
                                   tables4=[df4.to_html(classes='female')], titles4=df4.columns.values,
                                   tables5=[df5.to_html(classes='female')], titles5=df5.columns.values, fresult=flst)

        return render_template('givetest.html', res=res)
    return render_template('givetest.html')


if __name__ == '__main__':
    app.run("0.0.0.0")
    # app.run(debug=True)
 