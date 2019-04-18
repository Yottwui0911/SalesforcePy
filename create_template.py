#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import pandas as pd
from mako.template import Template
from mako.lookup import TemplateLookup

def CreateTemplate(df):
    work_records = GetWorkRecord(df)
    work_period = GetWorkPeriod(df)

    lookup = TemplateLookup(directories = [""],
                            output_encoding='utf-8',
                            input_encoding='utf-8',
                            default_filters=['decode.utf8'])
    template = lookup.get_template('template.tpl')
    sql = template.render(work_period = work_period, work_records=work_records).decode('utf-8')
    
    print '\n==============output==============\n\n'
    print sql
    print '\n==============output=============='

def GetWorkRecord(df):
    work_record = []
    for i, row in df.iterrows():
        s = row[u'日付'].strftime("%m/%d") + "(" + row[u'曜日']+ ")"
        if(row[u'出社'] != row[u'出社'] or row[u'退社'] != row[u'退社']):
            s += '\t' + u"休暇"
        else:
            s += '\t' + row[u'出社'] + ' ～ '.decode('utf-8') + row[u'退社']

        if(row[u'イベント／勤務状況'] == row[u'イベント／勤務状況']):
                s += '\t' + row[u'イベント／勤務状況']
        work_record.append(s)
    return work_record

def GetWorkPeriod(df):
    return min(df[u'日付']).strftime("%Y/%m/%d") + ' ～ '.decode('utf-8') + max(df[u'日付']).strftime("%Y/%m/%d")

