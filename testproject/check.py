import mysql.connector
import smtplib
import os
os.system("scrapy crawl it")
os.system("scrapy crawl product")



EMAIL = os.environ.get("EMAIL_ID")
PASSWORD = os.environ.get("EMAIL_PASSWORD")


conn = mysql.connector.connect(
    host='scrapy.c2td2vggsyn1.ap-south-1.rds.amazonaws.com',
    user='scrapy',
    passwd='joydeepbiswas',
    database='scraping'

)
curr = conn.cursor()

curr.execute("select * from itjobs")
it_rows = curr.fetchall()
it_rows_len = len(it_rows)
curr.execute("select * from jobs")
govt_rows = curr.fetchall()
govt_rows_len = len(govt_rows)

curr.execute("select * from users")
user_rows = curr.fetchall()

user_rows_len = len(user_rows)
#print(user_rows_len)


def send_mail(email,job_name,job_link,user_name):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL, PASSWORD)
        print('login sucess')
        subject = 'Alert! New Job Notification'
        # j = 0
        body = 'Greetings '+user_name+ ' here is your job alert\n'
        body += 'Job Name:\n' + job_name + '\n' + 'Job Link: \n' + job_link + '\n\n\n\n'
        body += 'Admin JB\n'+'If there is any issue please fell free to contact\n'+'Your feedback can make this service better\n'
        # for i in range(count):
        #     body += 'Job Name:' + item['job_name'][ind[i]] + '\n' + 'Job Link: ' + item['job_link'][ind[i]] + '\n'
        #     #j += 2
        msg = f'subject: {subject}\n\n{body}'
        smtp.sendmail(EMAIL, email, msg.encode("UTF-8"))
        print("Successfully sent email")


for i in range(user_rows_len):
    user_id = str(user_rows[i][0])
    #print(user_id)

    curr.execute("select * from user_jobs where user_id="+user_id)
    user_jobs_rows = curr.fetchall()
    user_jobs_rows_len = len(user_jobs_rows)
    # for x in user_jobs_rows:
    #     print(x)

    print(user_jobs_rows_len)
    if(user_jobs_rows_len==0):
        for j in range(it_rows_len):
            curr.execute("""insert into `user_jobs` values(%s,%s,%s)""", (
                it_rows[j][0],
                it_rows[j][1],
                user_id
            ))
            #send_mail(str(user_rows[i][2]),it_rows[j][0],it_rows[j][1],user_rows[i][1])
            conn.commit()
        for j in range(govt_rows_len):
            curr.execute("""insert into `user_jobs` values(%s,%s,%s)""", (
                govt_rows[j][0],
                govt_rows[j][1],
                user_id
            ))
            #send_mail(str(user_rows[i][2]), govt_rows[j][0], govt_rows[j][1], user_rows[i][1])
            conn.commit()
    else:
        for j in range(it_rows_len):
            count = 0
            for k in range(user_jobs_rows_len):
                if(it_rows[j][0]!=user_jobs_rows[k][0]):
                    count+=1
            if(count==user_jobs_rows_len):
                curr.execute("""insert into `user_jobs` values(%s,%s,%s)""", (
                    it_rows[j][0],
                    it_rows[j][1],
                    user_id
                ))
                send_mail(str(user_rows[i][2]), it_rows[j][0], it_rows[j][1], user_rows[i][1])
                conn.commit()
        for j in range(govt_rows_len):
            count = 0
            for k in range(user_jobs_rows_len):
                if(govt_rows[j][0]!=user_jobs_rows[k][0]):
                    count+=1
            if(count==user_jobs_rows_len):
                curr.execute("""insert into `user_jobs` values(%s,%s,%s)""", (
                    govt_rows[j][0],
                    govt_rows[j][1],
                    user_id
                ))
                send_mail(str(user_rows[i][2]), govt_rows[j][0], govt_rows[j][1], user_rows[i][1])
                conn.commit()






print(user_rows[1][0])


#print(rows[0][0])
#print(len(rows))




