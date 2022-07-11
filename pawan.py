
from datetime import datetime
import mysql.connector
from prettytable import PrettyTable
from time import sleep
con=mysql.connector.connect(host="localhost",user='pawan',password='mysql',database='hospitaldb')
cur=con.cursor()
def date():
    print("-"*90)
    date=datetime.now().strftime("%d/%m/%y")
    print("\t\t\ttoday's date is : ",date)
def login():
    pas_count = 0
    while(True):
        print("="*90)
        sleep(0.5)
        print("\n\t\t\t\tLOGIN PAGE\n\t\t\t\t----------")
        sleep(1)
        username=input("ENTER USERNAME => ")
        password=input("ENTER PASSWORD => ")
        cur.execute(f"select username from accounts")
        res=cur.fetchall()
        j=0
        for i in res:
            if i[0]==username:
                j+=1
                break
        if j==0:
            sleep(0.5)
            print("\n\t\t\tUSERNAME NOT FOUND !!!\n\t\t\t{}\n".format("-"*30))
            while(True):
                sleep(1)
                option=input("DO YOU WANT TO CREATE ACCOUNT (Y/N) => ")
                if option=='y' or option=='Y':
                    sign_up()
                    break
                elif option=='n' or option=='N':
                    print("-"*90)
                    sleep(1)
                    print("\t\tTHANK YOU.. HAVE A NICE DAY")
                    print("-"*90)
                    exit()
                else:
                    sleep(0.5)
                    print("\nYOU ENTERED A WRONG INPUT\n")
                    continue
        if(j==1):
            cur.execute("select username from accounts where password='%s'"%(password))
            s=cur.fetchall()
            if len(s)==0:
                sleep(1)
                print("\n\n\t\t----  YOU ENTERED A WRONG PASSWORD PLEASE TRY AGAIN ! ----\n")
                pas_count += 1
                print(pas_count)
                if pas_count <= 3:pass
                else:
                    sleep(0.5)
                    print("\t\t\t========YOU HAVE REACHED THE LIMIT========")
                    sleep(1)
                    print("\t\t\t\tkindly sign up")
                    sign_up()
                    break
            elif s[0][0]==username:
                break
            else:
                sleep(1)
                print("\n ** YOUR ACCOUNT IS NOT THERE , KINDLY SIGN UP TO FIX APPOINMENT **")
                sign_up()
                break
def sign_up():
    print("="*90)
    sleep(1)
    print("\t\t\tSIGN UP PAGE\n\t\t\t------------")
    sleep(0.5)
    print("\n \t========= USERNAME AND PASSWORD MUST BE ALPHANUMERIC=========\n")
    sleep(0.5)
    username=input('ENTER YOUR USERNAME => ')
    password=input("ENTER YOU PASSWORD => ")
    cur.execute("insert into accounts values('%s','%s')" %(username,password))
    con.commit()
    sleep(1)
    print('\n\t\t\t**** SIGN UP SUCCESSFULLY ***')
    sleep(1)
    print("\n\t\t\t**** DONT FORGET YOU PASSWORD ***")
def account():
    print("-"*90)
    sleep(0.5)
    print("\t\tWELCOME TO HOSPITAL ONLINE BOOKIN APPOINMENT")
    sleep(1)
    while(True):
        input_=input("\nDo you have a account already [y/n] : ")
        if input_=='y' or input_=='Y':
            login()
            break
        elif input_=='n' or input_=='N':
            sign_up()
            break
        else:
            print("\n\t\t** PLEASE ENTER A RIGHT OPTION **")
            continue

pat_name   =" "
pat_age    =" "
pat_contact_num=" "
pat_prob   =" "
pat_dur    =" "
def pat_det():
    global pat_name,pat_age,pat_contact_num,pat_prob,pat_dur
    pat_name=input("\nENTER YOUR NAME => ")
    while(True):
        try:
            pat_age=int(input("ENTER YOUR AGE => "))
        except ValueError:
            print("\n\t\t** DON'T ENTER SYMBOLS/STRS/ALPHANUMERICS **\n")
        else:
            break
    pat_contact_num=input("ENTER CONTACT NUMBER => ")
    pat_prob=input("ENTER PROBLEM YOU HAVE => ")
    while(True):
        try:
            pat_dur=int(input("HOW MANY DAYS YOU HAVE {} (USE NUMBER) => ".format(pat_prob)))
        except ValueError:
            print("\n\t\t** DON'T ENTER SYMBOLS/STRS/ALPHANUMERICS **\n")
        else:
            break
    
def spacialist():
    cur.execute("select * from doctors")
    s=cur.fetchall()
    print("-"*90)
    print("\n\t\t\t\tSPACIALIST :")
    for i in s:
        print(f"{i[0]}   {i[1]}   {i[2]}")
def appoinment():
    print("\n\n\t\tREFER THE ABOVE LIST ( DONT USE DR. NAME)")
    while(True):
        while(True):
            try:
                doctor=int(input("\nENTER THE DOCTOR ID => "))
            except ValueError:
                print("\n\t\t ** DON'T ENTER SYMBOLS/STRS/ALPHANUMERICS **\n")
            else:
                break
        cur.execute('select id from doctors where id=%d'%(doctor))
        doctor_id=cur.fetchall()
        if len(doctor_id)==0:       
            print("\n\t\t** PLEASE CHOOSE ID FROM THE BELOW LIST **")
            spacialist()
            continue
        elif doctor_id[0][0]==doctor:
            break

    cur.execute(f"select name from doctors where id={doctor}")
    s=cur.fetchall()
    doc_name=s[0][0]
    appoinment_date=input("\n APPOINTMENT DATE (dd-mm-yyyy) => ")
    appoinment_time=input("APPOINTMENT TIME (use 24 hour) => ")
    cur.execute("insert into patients values('{}',{},'{}','{}',{},'{}','{}','{}')".format(pat_name,pat_age,pat_contact_num,pat_prob,pat_dur,doc_name,appoinment_date,appoinment_time))
    con.commit()
    sleep(0.6)
    print("-"*70)
    print("\n\t\t\t{}\n\t\t\tAPPOINTMENT DETAILS\n\t\t\t{}".format("-"*20,"-"*20))
    table=PrettyTable(['NAME',"AGE",'CONTACT NUMBER','PROBLEM','DURATION','DOCTOR NAME','APPOINMENT DATE','APPOINMENT TIME'])
    table.add_rows([[pat_name,pat_age,pat_contact_num,pat_prob,pat_dur,doc_name,appoinment_date,appoinment_time]])
    print(table)
    sleep(2)
    
    print("\n\t\t\t{}\n\t\t\tThank you, Have a nice day...!\n\t\t\t{}".format("-"*31,"-"*31))

if __name__ == "__main__":
    date()
    account()
    print("-------------------------------------------------------------------------------------------------------------")
    print("\t\t\t\tWELCOME")
    print("-------------------------------------------------------------------------------------------------------------")
    pat_det()
    spacialist()
    appoinment()


            







