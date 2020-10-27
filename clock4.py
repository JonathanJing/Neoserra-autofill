from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import signal
import datetime
import pandas as pd
delay = 2
hour_total = 4
#hour_total = 8

def log_in(browser):
    time.sleep(delay)
    username = browser.find_element_by_id('LogOnEmployeeId')
    username.send_keys('888165875')
    signInButton = browser.find_element_by_class_name('tcp-btn.BtnFeature.WideDashboardButton.DefaultSubmitBehavior')
    signInButton.click()
    time_check = datetime.datetime.now()
    print('Successful Log In \n')
    return browser, time_check

def get_status(browser):
    time.sleep(delay)
    status = browser.find_element_by_class_name('ClockStatusContainer.ng-binding')
    status = status.text
    print('Current Statue is: ', status)
    lunch_time = 0
    if status.rsplit(None, 1)[-1] == 'Lunch':
        st_status = 'Lunch'
        lunch_time = int(status.split(' ')[2])
    elif status.split(' ')[1] == 'in':
        st_status = 'Clocked in'
    elif status.split(' ')[1] == 'out':
        st_status = 'Clocked out'
    else:
        st_status = 'Unknown'
    return st_status, lunch_time

def logout_time(time_check, hour_left):
    time_lougout = time_check + datetime.timedelta(hours=hour_left)
    print('Log out time should be: ', time_lougout)
    return time_lougout

def get_hours(browser):
    time.sleep(delay)
    hours = browser.find_element_by_class_name('WidgetTable.ng-scope')
    text = hours.text
    text = text.split("\n")
    text = text[2:]
    Date = []
    Hour = []
    for i in text:
        i = i.split()
        Date.append(i[0])
        Hour.append(float(i[10]))
    df = pd.DataFrame({'Date': Date, 'Hour': Hour})
    sum = df.groupby(['Date']).sum()
    print(sum)
    hour_today = sum.iloc[-1].Hour
    week_rolling = sum.rolling(min_periods=1, window=4).sum()
    hour_week = week_rolling.iloc[-1].Hour
    print('Current total hour of today is: ', hour_today)
    print('Current total hout of this week is: ', hour_week)
    return hour_today, hour_week

def clock_out():
    clockout = browser.find_element_by_id('ClockOut')
    clockout.click()
    time.sleep(delay)
    cont = browser.find_element_by_class_name('tcp-btn.BtnAction.DefaultSubmitBehavior')
    cont.click()
    time.sleep(delay)
    cont = browser.find_element_by_class_name('tcp-btn.BtnAction.DefaultSubmitBehavior')
    cont.click()
    print('\n Clocked out')

def clock_in():
    clockout = browser.find_element_by_id('ClockIn')
    clockout.click()
    time.sleep(delay)
    cont = browser.find_element_by_class_name('tcp-btn.BtnAction.DefaultSubmitBehavior')
    cont.click()
    time.sleep(delay)
    cont = browser.find_element_by_class_name('tcp-btn.BtnAction.DefaultSubmitBehavior')
    cont.click()
    time.sleep(delay)
    cont = browser.find_element_by_class_name('tcp-btn.BtnAction.DefaultSubmitBehavior')
    cont.click()
    print('\n Clocked in')

def lunch_out():
    clockout = browser.find_element_by_id('Break')
    clockout.click()
    time.sleep(delay)
    cont = browser.find_element_by_class_name('tcp-btn.BtnAction.DefaultSubmitBehavior')
    cont.click()
    time.sleep(delay)
    cont = browser.find_element_by_class_name('tcp-btn.BtnAction.DefaultSubmitBehavior')
    cont.click()
    print('\n Lunch out')

def lunch_back():
    clockout = browser.find_element_by_id('ReturnFromBreak')
    clockout.click()
    time.sleep(delay)
    cont = browser.find_element_by_class_name('tcp-btn.BtnAction.DefaultSubmitBehavior')
    cont.click()
    time.sleep(delay)
    cont = browser.find_element_by_class_name('tcp-btn.BtnAction.DefaultSubmitBehavior')
    cont.click()
    time.sleep(delay)
    cont = browser.find_element_by_class_name('tcp-btn.BtnAction.DefaultSubmitBehavior')
    cont.click()
    print('\n Lunch back')

def tick(hour_total):
    print('Tick! The time is: %s' % datetime.datetime.now())
    global browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")       # define headless
    browser = webdriver.Chrome(chrome_options=chrome_options)
    #browser = webdriver.Chrome()
    browser.get('https://182629.tcplusondemand.com/app/webclock/#/EmployeeLogOn/182629')
    browser, time_check = log_in(browser)
    status, lunch_time = get_status(browser)
    hour_today, hour_week = get_hours(browser)
    if hour_week > 20:
        week_left = 40 - hour_week
    else:
        week_left = 20 - hour_week

    if week_left < hour_total:
        hour_left = week_left - hour_today
    else:
        hour_left = hour_total - hour_today
    #hour_left = hour_total - hour_today

    time_lougout = logout_time(time_check, hour_left)
    return status, hour_today, time_lougout, lunch_time

def handler(signum, frame):
    print ("Quit program")
    quit()

if __name__ == '__main__':
    print ('Enter "ctrl + c" to quit program \n')
    signal.signal(signal.SIGINT, handler)
    status, hour_today, time_lougout, lunch_time = tick(hour_total)
    if status == 'Clocked in':
        k=1
        while k<2:
            now = time.strftime('%H_%M',time.localtime())
            now = now.split('_')
            hour = int(now[0])
            minute = int(now[1])
            print('Current: \t', hour, minute)
            lougout = time_lougout - datetime.timedelta(minutes = 1)
            print('Clock out time: ', lougout.hour, lougout.minute)
            if hour == lougout.hour and minute == lougout.minute:
                print ('start to run scripts')
                tick(hour_total)
                clock_out()
                break
            else:
                time.sleep(50)
                print ("Wait:",  datetime.datetime.now())
    elif status =='Lunch':
        if lunch_time > 30:
            lunch_back()
        else:
            time_back = datetime.datetime.now() + datetime.timedelta(minutes=(30-lunch_time))
            k = 1
            while k<2:
                now = time.strftime('%H_%M',time.localtime())
                now = now.split('_')
                hour = int(now[0])
                minute = int(now[1])
                print('Current lunch: \t', hour, minute)
                print('Lunch back time: \t',time_back.hour, time_back.minute)
                if hour == time_back.hour and minute == time_back.minute:
                    print ('start to run scripts')
                    tick(hour_total)
                    lunch_back()
                    break
                else:
                    time.sleep(60)
                    print ("Wait:",  datetime.datetime.now())

    elif status == 'Clocked out':
        clock_in()
    elif status == 'Unknown':
        print('Unknown Status')
    else:
        print('Unknown')
