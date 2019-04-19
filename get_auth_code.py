#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from time import sleep
from selenium import webdriver

def GetAuthCode(driver, outlook_user_name, outlook_password):
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
    return re.sub(u"^.*確認コード: (\d*) 最近.*$", r"\1", element.text, flags=(re.MULTILINE | re.DOTALL))
