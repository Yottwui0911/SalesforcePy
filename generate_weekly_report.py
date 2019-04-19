#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import get_auth_code as gac
import salesforce
import create_template as ct

try:
    setting_path = "./setting.json"
    setting = open(setting_path, "r")
    setting_json = json.load(setting)
except:
    print(u'setting.jsonを同じ階層に配置してください。')
    exit

while True:
    print (u'取得したい週の日付を入力してください。')
    print (u'例：2019-11-18')
    input_test_word = raw_input('>>>  ')
    try:
        tdatetime = datetime.datetime.strptime(input_test_word, '%Y-%m-%d')
        date = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)
    except:
        print(u'日付のフォーマットで入力してください。')
        continue
    break

try:
    driver=webdriver.Chrome(executable_path=r'chromedriver.exe')
except:
    print(u'chromedriver.exeを同じ階層に配置してください。')
    exit

login_url = setting_json['salseforce']['team_url']

user_name = setting_json['salseforce']['user_name']
password = setting_json['salseforce']['password']

# salesforceの画面を開く
salesforce.OpenSalesForce(driver, login_url, user_name, password)

# 新しいウィンドウを開く
driver.execute_script("window.open('https://outlook.office.com/mail/')")

# 新しいタブの出現を待つ
sleep(3)
driver.switch_to.window(driver.window_handles[1])

# outlookのID,passwordを設定ファイルから取得
outlook_user_name = setting_json['outlook']['user_name']
outlook_password = setting_json['outlook']['password']

# 2段階認証コードの取得
auth_code = gac.GetAuthCode(driver, outlook_user_name, outlook_password)

# エラー処理
if(auth_code == 0):
    print('認証コードを取得できませんでした')
    exit

driver.switch_to.window(driver.window_handles[0])

# salesforceにlogin
salesforce.Login(driver, auth_code)

result = salesforce.GetServiceRecord(driver, date)

# ドライバを閉じる
driver.quit()

ct.CreateTemplate(result)

sleep(10000)
