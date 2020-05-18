# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import smtplib
import os
import mysql.connector




class TestprojectPipeline(object):

    def __init__(self):
        self.create_conn()

    def create_conn(self):
        self.conn = mysql.connector.connect(
            host= 'scrapy.c2td2vggsyn1.ap-south-1.rds.amazonaws.com',
            user = 'scrapy',
            passwd = 'joydeepbiswas',
            database = 'scraping'

        )
        self.curr = self.conn.cursor()
    def process_item(self, item, spider):
        if item['job_type']=='govt':
            self.insert_db_govt(item)
        else:
            self.insert_db_it(item)
        #self.select_db(item)
        return item
    # def select_db(self,item):
    #     self.curr.execute("SELECT * FROM jobs")
    #     rows = self.curr.fetchall()
    #     j=1
    #     for i in range(len(item['job_name'])):
    #         for record in rows:
    #             if(item['job_name'][i]!=record[0]):
    #                 job_name = item['job_name'][i]
    #                 job_link = item['job_link'][j]
    #
    #                 self.insert_db(job_name,job_link)
    #                 j+=2
    def insert_db_govt(self,item):
        self.EMAIL_ID = os.environ.get('EMAIL_ID')
        self.EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
        self.curr.execute("select job_name from jobs")

        rows = self.curr.fetchall()
        row_len = len(rows)
        item_len = len(item['job_name'])
        lenngth = item_len-row_len
        #self.conn.commit()
        j=1
        # print(rows)
        self.curr.execute("delete from jobs where 1")
        for i in range(len(item['job_name'])):
            #print("yes")



            self.curr.execute("""insert into `jobs` values(%s,%s)""",(
                item['job_name'][i],
                item['job_link'][j]
            ))
            j+=2
            self.conn.commit()
        if(lenngth>0):
            print("change"+str(self.EMAIL_ID)+" "+str(self.EMAIL_PASSWORD))
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(self.EMAIL_ID, self.EMAIL_PASSWORD)
                print('login sucess')
                subject = 'New Job Notification'
                j=1
                body=''
                for i in range(lenngth):

                    body += 'Job Name:' + item['job_name'][i]+'\n'+'Job Link: '+ item['job_link'][j]+'\n'
                    j+=2
                msg = f'subject: {subject}\n\n{body}'
                smtp.sendmail(self.EMAIL_ID, 'joydeepdj@gmail.com', msg.encode("UTF-8"))
                print("Successfully sent email")

        else:
            print("No Change")

            #print("no")
        # self.curr.execute("""insert into jobs values(%s,%s) """, (
        #                 job_name,
        #                 job_link
        #             ))
        # #self.conn.commit()


    def insert_db_it(self, item):
        self.EMAIL_ID = os.environ.get('EMAIL_ID')
        self.EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
        self.curr.execute("select job_name from itjobs")

        rows = self.curr.fetchall()
        row_len = len(rows)
        item_len = len(item['job_name'])
        #lenngth = item_len - row_len
        # self.conn.commit()
        #j = 0
        # print(rows)
        #self.curr.execute("delete from itjobs where 1")
        #i=item_len-1

        #ind = []
        #for i in range(item_len):
            #print("yes")
            #if(j==item_len):
                #break
        if(row_len==0):
            self.curr.execute("""insert into `itjobs` values(%s,%s)""", (
                item['job_name'][0],
                item['job_link'][0]
            ))
            self.conn.commit()
        else:
            count =0
            for j in range(row_len):
                #print("yes")
                if(rows[j][0]!=item['job_name'][0]):
                    # self.curr.execute("""insert into `itjobs` values(%s,%s)""", (
                    #     item['job_name'][0],
                    #     item['job_link'][0]
                    # ))
                    # self.conn.commit()
                    # self.send_mail(item['job_name'][0],item['job_link'][0])
                    #ind.append()
                    count+=1
                    print("yes ")
                else:
                    print("no")
            if(count==row_len):
                self.curr.execute("""insert into `itjobs` values(%s,%s)""", (
                    item['job_name'][0],
                    item['job_link'][0]
                ))
                self.conn.commit()
                print("change" + str(self.EMAIL_ID) + " " + str(self.EMAIL_PASSWORD))
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login(self.EMAIL_ID, self.EMAIL_PASSWORD)
                    print('login sucess')
                    subject = 'New Job Notification'
                    # j = 0
                    body = 'Job Name:' + item['job_name'][0] + '\n' + 'Job Link: ' + item['job_link'][0] + '\n'
                    # for i in range(count):
                    #     body += 'Job Name:' + item['job_name'][ind[i]] + '\n' + 'Job Link: ' + item['job_link'][ind[i]] + '\n'
                    #     #j += 2
                    msg = f'subject: {subject}\n\n{body}'
                    smtp.sendmail(self.EMAIL_ID, 'joydeepdj@gmail.com', msg.encode("UTF-8"))
                    print("Successfully sent email")




