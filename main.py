#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import re

setting_path = "./setting.json"
setting = open(setting_path, "r")
setting_json = json.load(setting)

login_url = setting_json['salseforce']['team_url']

driver=webdriver.Chrome(executable_path='chrome_drive_path')
driver.get(login_url)

user_name = setting_json['salseforce']['user_name']
password = setting_json['salseforce']['password']

# ユーザーネーム入力
user_input=driver.find_element_by_id('username')
user_input.send_keys(user_name)

# パスワード入力
pass_input=driver.find_element_by_id('password')
pass_input.send_keys(password)

# ログインボタンクリック
driver.find_element_by_id('Login').click()

# 新しいウィンドウを開く
driver.execute_script("window.open('https://outlook.office.com/mail/')")

# 新しいタブの出現を待つ
WebDriverWait(driver, 3).until(lambda d: len(d.window_handles) > 1)
driver.switch_to.window(driver.window_handles[1])

# outlookのID,passwordを設定ファイルから取得
outlook_user_name = setting_json['outlook']['user_name']
outlook_password = setting_json['outlook']['password']

# outookのIDの入力
outlook_user_input=driver.find_element_by_id('i0116')
outlook_user_input.send_keys(outlook_user_name)
driver.find_element_by_id('idSIButton9').click()

# outookのパスワードの入力
outlook_password_input=driver.find_element_by_id('i0118')
outlook_password_input.send_keys(outlook_password)

# サインインボタンクリック
sleep(3)
driver.find_element_by_id('idSIButton9').click()

# サインイン維持
sleep(3)
driver.find_element_by_id('idSIButton9').click()

# outlookが開かれるのを待つ
sleep(7)

# Salesforceから送られてくるID確認のメールから認証コードを取得する
element = driver.find_element_by_xpath("//div[contains(@aria-label, 'noreply@salesforce.com')]")
auth_code =  re.sub(u"^.*確認コード: (\d*) 最近.*$", r"\1", element.text, flags=(re.MULTILINE | re.DOTALL))

# エラー処理
if(auth_code == 0):
    print('認証コードを取得できませんでした')
    exit

driver.switch_to.window(driver.window_handles[0])

# 2段階認証コードの入力
outlook_user_input=driver.find_element_by_id('emc')
outlook_user_input.send_keys(auth_code)
driver.find_element_by_id('save').click()
