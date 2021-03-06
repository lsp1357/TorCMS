# -*- coding: utf-8 -*-

import config
from torcms.core import tools
from torcms.model.post_model import MPost
from torcms.model.post_hist_model import MPostHist
from torcms.model.wiki_model import MWiki
from torcms.model.wiki_hist_model import MWikiHist
from difflib import HtmlDiff
from torcms.core.tool.send_email import send_mail
from config import smtp_cfg
from config import site_url
from config_email import post_emails
import os
from torcms.core.tools import diff_table
import re

import datetime
from config import router_post

now = datetime.datetime.now()

datestr = now.strftime('%Y-%m-%d %H:%M:%S')


def run_edit_diff():
    email_cnt = '''<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title></title>
    <style type="text/css">
        table.diff {font-family:Courier; border:medium;}
        .diff_header {background-color:#e0e0e0}
        td.diff_header {text-align:right}
        .diff_next {background-color:#c0c0c0}
        .diff_add {background-color:#aaffaa}
        .diff_chg {background-color:#ffff77}
        .diff_sub {background-color:#ffaaaa}
    </style></head><body>'''

    idx = 1

    email_cnt = email_cnt + '<table border=1>'

    mpost = MPost()
    mposthist = MPostHist()

    recent_posts = mpost.query_recent_edited(tools.timestamp() - 24 * 60 * 60)
    for recent_post in recent_posts:
        hist_rec = mposthist.get_last(recent_post.uid)
        if hist_rec:
            foo_str = '''
                <tr><td>{0}</td><td>{1}</td><td class="diff_chg">Edit</td><td>{2}</td>
                <td><a href="{3}">{3}</a></td></tr>
                '''.format(idx, recent_post.user_name, recent_post.title,
                           os.path.join(site_url, 'post', recent_post.uid + '.html'))
            email_cnt = email_cnt + foo_str
        else:
            foo_str = '''
                <tr><td>{0}</td><td>{1}</td><td class="diff_add">New </td><td>{2}</td>
                <td><a href="{3}">{3}</a></td></tr>
                '''.format(idx, recent_post.user_name, recent_post.title,
                           os.path.join(site_url, 'post', recent_post.uid + '.html'))
            email_cnt = email_cnt + foo_str
        idx = idx + 1

    recent_posts = mpost.query_recent_edited(tools.timestamp() - 24 * 60 * 60, kind='2')
    for recent_post in recent_posts:
        hist_rec = mposthist.get_last(recent_post.uid)
        if hist_rec:
            foo_str = '''
                <tr><td>{0}</td><td>{1}</td><td class="diff_chg">Edit</td><td>{2}</td>
                <td><a href="{3}">{3}</a></td></tr>
                '''.format(idx, recent_post.user_name, recent_post.title,
                           os.path.join(site_url, router_post['2'], recent_post.uid))
            email_cnt = email_cnt + foo_str
        else:
            foo_str = '''
                <tr><td>{0}</td><td>{1}</td><td class="diff_add">New </td><td>{2}</td>
                <td><a href="{3}">{3}</a></td></tr>
                '''.format(idx, recent_post.user_name, recent_post.title,
                           os.path.join(site_url, router_post['2'], recent_post.uid))
            email_cnt = email_cnt + foo_str
        idx = idx + 1

    mpost = MWiki()
    mposthist = MWikiHist()

    recent_posts = mpost.query_recent_edited(tools.timestamp() - 24 * 60 * 60)
    for recent_post in recent_posts:
        hist_rec = mposthist.get_last(recent_post.uid)
        if hist_rec:
            foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_chg">Edit</td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(idx, recent_post.user_name, recent_post.title,
                               os.path.join(site_url, 'wiki', recent_post.title ))
            email_cnt = email_cnt + foo_str
        else:
            foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_add">New </td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(idx, recent_post.user_name, recent_post.title,
                               os.path.join(site_url, 'wiki', recent_post.title ))
            email_cnt = email_cnt + foo_str
        idx = idx + 1

    recent_posts = mpost.query_recent_edited(tools.timestamp() - 24 * 60 * 60, kind='2')
    for recent_post in recent_posts:
        hist_rec = mposthist.get_last(recent_post.uid)
        if hist_rec:
            foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_chg">Edit</td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(idx, recent_post.user_name, recent_post.title,
                               os.path.join(site_url, 'page', recent_post.uid + '.html'))
            email_cnt = email_cnt + foo_str
        else:
            foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_add">New </td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(idx, recent_post.user_name, recent_post.title,
                               os.path.join(site_url, 'page', recent_post.uid + '.html'))
            email_cnt = email_cnt + foo_str
        idx = idx + 1

    email_cnt = email_cnt + '</table>'

    mpost = MPost()
    mposthist = MPostHist()
    diff_str = ''
    ######################################################
    recent_posts = mpost.query_recent_edited(tools.timestamp() - 24 * 60 * 60)
    for recent_post in recent_posts:
        hist_rec = mposthist.get_last(recent_post.uid)
        if hist_rec:
            print('=' * 10)
            print(recent_post.title)

            raw_title = hist_rec.title
            new_title = recent_post.title

            infobox = diff_table(raw_title, new_title)

            # if len(test) > 1:
            # start = test.find('<table class="diff"')  # 起点记录查询位置
            # end = test.find('</table>')
            # infobox = test[start:end] + '</table>'
            # if ('diff_add' in infobox) or ('diff_chg' in infobox) or ('diff_sub' in infobox):
            diff_str = diff_str + '<h2 style="color:red; font-size:larger; font-weight:70;">TITLE: {0}</h2>'.format(
                    recent_post.title) + infobox

            test = diff_table(hist_rec.cnt_md, recent_post.cnt_md)
            print(test)
            # if len(test) >1 :
            # start = test.find('<table class="diff"')  # 起点记录查询位置
            # end = test.find('</table>')

            # infobox = test[start:end] + '</table>'
            # if ('diff_add' in infobox) or ('diff_chg' in infobox) or ('diff_sub' in infobox):
            diff_str = diff_str + '<h3>CONTENT</h3>'.format(
                    recent_post.title) + test + '</hr>'
        else:
            continue
    ######################################################
    recent_posts = mpost.query_recent_edited(tools.timestamp() - 24 * 60 * 60, kind='2')
    for recent_post in recent_posts:
        hist_rec = mposthist.get_last(recent_post.uid)
        if hist_rec:
            print('=' * 10)

            print(recent_post.title)

            raw_title = hist_rec.title
            new_title = recent_post.title

            infobox = diff_table(raw_title, new_title)
            # infobox = test[start:end] + '</table>'
            # if ('diff_add' in infobox) or ('diff_chg' in infobox) or ('diff_sub' in infobox):
            diff_str = diff_str + '<h2 style="color:red; font-size:larger; font-weight:70;">TITLE: {0}</h2>'.format(
                    recent_post.title) + infobox

            infobox = diff_table(hist_rec.cnt_md, recent_post.cnt_md)

            diff_str = diff_str + '<h3>CONTENT</h3>'.format(
                    recent_post.title) + infobox + '</hr>'
        else:
            continue
    ###########################################################
    if len(diff_str) < 20000:
        email_cnt = email_cnt + diff_str
    email_cnt = email_cnt + '''<table class="diff" summary="Legends">
        <tr> <th colspan="2"> Legends </th> </tr>
        <tr> <td> <table border="" summary="Colors">
                      <tr><th> Colors </th> </tr>
                      <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>
                      <tr><td class="diff_chg">Changed</td> </tr>
                      <tr><td class="diff_sub">Deleted</td> </tr>
                  </table></td>
             <td> <table border="" summary="Links">
                      <tr><th colspan="2"> Links </th> </tr>
                      <tr><td>(f)irst change</td> </tr>
                      <tr><td>(n)ext change</td> </tr>
                      <tr><td>(t)op</td> </tr>
                  </table></td> </tr>
    </table></body>'''

    # print (email_cnt)
    print('edit diff count:', idx)
    if idx > 1:
        send_mail(post_emails, "{0}|{1}|{2}".format(smtp_cfg['name'], '文档更新情况', datestr), email_cnt)
