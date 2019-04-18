#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as dt
from datetime import timedelta
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re

def OpenSalesForce(driver, url, user_name, password):
    driver.get(url)

    # ユーザーネーム入力
    user_input=driver.find_element_by_id('username')
    user_input.send_keys(user_name)

    # パスワード入力
    pass_input=driver.find_element_by_id('password')
    pass_input.send_keys(password)

    # ログインボタンクリック
    driver.find_element_by_id('Login').click()

def Login(driver, auth_code):
    # 2段階認証コードの入力
    outlook_user_input=driver.find_element_by_id('emc')
    outlook_user_input.send_keys(auth_code)
    driver.find_element_by_id('save').click()

    # salesforceが開かれるのを待つ
    sleep(7)

def GetServiceRecord(driver, date):
    # 勤務表を開く
    driver.find_element_by_id('01r100000009sGt_Tab').click()
    sleep(7)

    # 月次報告サマリを開く
    driver.find_element_by_class_name('monthlySum').click()

    driver.switch_to_window(driver.window_handles[2])
    sleep(7)

    return GetDataFrame(driver, date)

def GetDataFrame(driver, date):
    current_url = driver.current_url

    # 取得したい日付
    date_from = date - timedelta(days=date.weekday())
    date_to = date_from + timedelta(days=4)

    urls = []
    urls.append([date_from.year ,re.sub('date=\d{8}', 'date=' + (date_from - timedelta(days=date_from.day - 1)).strftime('%Y%m%d'), current_url)])
    urls.append([date_to.year, re.sub('date=\d{8}', 'date=' + (date_to - timedelta(days=date_to.day - 1)).strftime('%Y%m%d'), current_url)])
    urls = GetUniqueList(urls)

    frame = pd.DataFrame()
    for url in urls:
        # 新しいウィンドウを開く
        driver.execute_script("window.open('"+ url[1] +"')")

        driver.get(url[1])
        sleep(3)

        df=pd.read_html(driver.page_source, attrs={"id": "workTable"}, header=0)[0]
        col = df.columns.values

        col[0] = u"日付"
        col[1] = u"曜日"
        col[2] = u"休日フラグ"
        df.columns = col

        # 日付を補完する
        prefix = re.match(r'\d{1}/', df[u'日付'][0].strip()).group()
        for i in range(len(df[u'日付'])):
            if(i == 0):
                df[u'日付'][i] = '2019/' + df[u'日付'][i]
                continue
            df[u'日付'][i] = '2019/' + prefix + df[u'日付'][i]

        df = df[df[u'日付'].str.contains(r"\d+/\d+/\d+")]
        df[u'日付'] = pd.to_datetime(df[u'日付'])
        frame = pd.concat([frame, df])
    return frame[(date_from <= frame[u'日付']) & (frame[u'日付'] < date_to + timedelta(days=1))].sort_values(by=[u'日付'], ascending=True)
def GetUniqueList(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]
