# SalesforcePy
Access SalesforceTeam by Selenium

## 自動週報ジェネレート
### セットアップ
`generate_weekly_report.py` と同階層に `setting.json`, `template.tpl`, `chromedriver.exe`を配置

#### setting.json
salesforceの項目に、salesforceのUrl,user_name（メールアドレス）,passwordを記入  
outlookの項目に、user_name（メールアドレス）,passwordを記入

#### template.tpl
お好きなフォーマットで記入

- `${work_period}` : 入力した日が含まれる期間を出力
- `${work_records}` : 入力した日が含まれる期間の勤務状況を出力

#### chromedriver.exe
ご自身のchromeのバージョンに合わせて、以下からdriverをダウンロードください。(現在配置しているものは、ver 73)  
http://chromedriver.chromium.org/downloads

### 実行
1. `generate_weekly_report.py`を実行
1. 指定したい期間が含まれる日付を入力
