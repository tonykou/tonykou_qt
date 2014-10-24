#coding:utf-8
import hashlib
import json
import urllib, urllib2
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from lxml import etree

def auto_reply(a, b, c):
    pass

@csrf_exempt
def weixin_main(request):
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = "monatonykou"
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin index")
    else:
        xml_str = smart_str(request.body)
        xml = etree.fromstring(xml_str)
        msg_type = xml.find("MsgType").text
        from_user_name = xml.find("FromUserName").text
        if msg_type == "text":
            content = xml.find("Content").text
            return HttpResponse(auto_reply(from_user_name, content, msg_type))
        elif msg_type == "event":
            event = xml.find("Event").text
            if event == "subscribe":
                return HttpResponse(auto_reply(from_user_name, "用户关注事件", "text"))
            elif event == "unsubscribe":
                print "用户取消关注"
            elif event == "CLICK":
                event_key = xml.find("EventKey").text
                return HttpResponse(auto_reply(from_user_name, event_key, "text"))
            else:
                print "error"
        else:
            return HttpResponse(auto_reply(from_user_name, "不支持的消息类型", "text"))


def get_access_token():
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % ("1", "2")
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = json.loads(response.read())
    return content["access_token"]


@login_required(login_url="/login/")
def access_token(request):
    if not request.user.is_staff:
        return HttpResponse("权限错误")
    return render(request, "Weixin/access_token.html", {"access_token": get_access_token()})
