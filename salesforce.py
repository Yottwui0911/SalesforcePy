#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from selenium import webdriver

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

    return "hoge"