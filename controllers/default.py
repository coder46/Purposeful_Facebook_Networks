# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
from facepy import GraphAPI
from facepy.utils import get_extended_access_token
import urllib2
import json
import sys
app_id='674585182560146'
app_sec='a5246f1ee31ff7716e84e97b9b29eb7d'

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Welcome to web2py!")
    #return dict(message=T('Hello World'))
    #print dir(request.env)
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


def create_users():
    return dict()
    
def login():
    return dict()
    
def echo():
    session.URL2=str(request.vars.URL)
    return request.vars.URL


def oauth():
    STR=str(request.env.query_string)
    #long_lived_access_token , expires_at= get_extended_access_token(token,app_id,app_sec)
    print "HELLO"
    if(STR):
        print STR
        TK=STR.split("&")
        AT=TK[0]
        AT=AT.split("=")
        access_token=AT[1]
        #print access_token
        graph=GraphAPI(access_token)
        #a=urllib2.urlopen("http://www.google.com") 
        print "MYACCESS "+access_token
        #long_lived_access_token , expires_at= get_extended_access_token(access_token,app_id,app_sec)
        #lac=graph.get('/oauth/access_token?grant_type=fb_exchange_token&client_id=674585182560146&client_secret=a5246f1ee31ff7716e84e97b9b29eb7d&fb_exchange_token='+access_token)
        
        #print "LONG LIVED JKSDHAK "+lac
        #graph=GraphAPI(long_lived_access_token)
        #graph=GraphAPI(access_token)
        print graph
        data=graph.get('/me')
        print data["id"],data["name"]
        rows=db(db.Users.user_id==data["id"]).select(db.Users.ALL)
        if(len(rows)==0):
            lac=graph.get('/oauth/access_token?grant_type=fb_exchange_token&client_id=674585182560146&client_secret=a5246f1ee31ff7716e84e97b9b29eb7d&fb_exchange_token='+access_token)
            lac=lac.split("=")
            lac=lac[1]
            #long_lived_access_token , expires_at= get_extended_access_token(access_token,app_id,app_sec)
            #db.Users.insert(Name=str(data["name"]),user_id=str(data["id"]),access_token=str(long_lived_access_token))
            db.Users.insert(Name=str(data["name"]),user_id=str(data["id"]),access_token=str(lac))
            print "Inserted"
        else:
            row=rows.first()
            #row.update(access_token=str(long_lived_access_token))
            #print "Row updated"
            print "Already there"
            print len(rows)
        
        pages=graph.get('/me/accounts')
        #print pages["data"][0]["name"]
        #print pages["data"][0]["access_token"]
        pages_len=len(pages["data"])
        for i in range(0,pages_len):
            page_name=pages["data"][i]["name"]
            page_id=pages["data"][i]["id"]
            page_token=pages["data"][i]["access_token"]
            print page_name,page_id,page_token
            rows=db(db.FBPages.page_id==page_id).select(db.FBPages.ALL)
            if(len(rows)==0):
                db.FBPages.insert(page_name=page_name,page_id=page_id,page_token=page_token)
                row1=db(db.Users.user_id==data["id"]).select().first()
                row2=db(db.FBPages.page_id==page_id).select().first()
                db.Has_page.insert(UserDBid=row1.id,PageDBid=row2.id)
            else:
                print page_name+" is already present"
                
        redirect(URL(r=request,f="search"))
                
          
        
        
    
    return dict()
def hello():
    print "HEY !!!"

count=0
def init_testusers():
    res=urllib2.urlopen('https://graph.facebook.com/'+app_id+'/accounts/test-users?access_token='+app_id+'|'+app_sec+'&limit=25')
    msg=json.load(res)
    tlen=len(msg["data"])
    for i in range(0,tlen):
        uid=msg["data"][i]["id"]
        name="User"+str(i)
        utoken=msg["data"][i]["access_token"]
        print uid,name,utoken
        rows=db(db.Users.user_id==uid).select(db.Users.ALL)
        if(len(rows)==0):
            db.Users.insert(Name=name,user_id=uid,access_token=utoken)
            print "ADDED"
        else:
            hello()
        post_on_wall(uid,"HELLO",utoken)
      
        
    return dict()



def post_on_wall(user_id,message,access_token):
    #rows=db(db.Users.user_id==user_id).select(db.Users.ALL)
    #row=rows[0]
    #access_token=row.access_token
    graph=GraphAPI(access_token)
    message=message.split("-")
    message='/'.join(message)
    #print graph.post(path=user_id+'/feed',message=message,access_token=access_token)
    '''try:
        print graph.post(path='me/feed',message=message,access_token=access_token)
        print "SENT MESSAGE "+message
    except:
        print "Could not send message "+message
        print "ERROR",sys.exec_info()[0]
        pass'''
    print graph.post(path='me/feed',message=(user_id+" From Purposeful Facebook Networks :D "+message),access_token=access_token)
    print "psoted "+message +" on "+user_id
    
def add_page():
    form=SQLFORM.factory(
         Field('page_name','string',label=""),
         #Field('cat','list:string',requires=IS_IN_SET(["BY NAME","BY TAGS","BY BRAND"]),label="")
         )
    print form.vars.page_name
    return dict(form=form)
    
    
    
def search():
    form=SQLFORM.factory(
         Field('topic','string',label="Search for a topic"),
         #Field('cat','list:string',requires=IS_IN_SET(["BY NAME","BY TAGS","BY BRAND"]),label="")
         )
         
    '''form.process(session=None, formname='test').accepted:
         redirect(URL(r=request,f="search_results",args=(form.vars.topic))
     #redirect(URL(r=request,f="search_results",args=['form.vars.name','form.vars.cat']))
    #lif form.errors:
    # response.flash="ERRORS!!!"'''
         
    if form.process(session=None,formname='test').accepted:
         redirect(URL(r=request,f="search_results",args=(form.vars.topic)))
    elif form.errors:
		response.flash="ERRORS!!!"
         
    return dict(form=form)
     
     
def search_results():
    topic=str(request.args[0])
    users=db(db.Users.id>0).select(db.Users.ALL)
    userlist=""
    for i in users:
        userlist=userlist+str(i.id)+" "
        print str(i.id)
    form=SQLFORM.factory(
         Field('pagelink','string',label="Enter Link for Facebook Page"),
         #Field('cat','list:string',requires=IS_IN_SET(["BY NAME","BY TAGS","BY BRAND"]),label="")
         )
    if form.process(session=None,formname='test1').accepted:
         #session.fblink=str(form.vars.pagel)
         pagelink=str(form.vars.pagelink).split('/')
         pagelink="-".join(pagelink)
         print pagelink
         redirect(URL(r=request,f="send_link",args=(userlist,pagelink)))
    elif form.errors:
		response.flash="ERRORS!!!"
    return dict(topic=topic,users=users,form=form)
    
def send_link():
    '''link=str(request.args[0])
    userlist=request.args[1]
    print userlist
    return dict(link=link)'''
    userlist=str(request.args[0])[:-1]
    pagelink=str(request.args[1])
    #pagelink=pagelink.split("-")
    #pagelink="/".join(pagelink)
    print pagelink
    print userlist
    userlist=userlist.split("_")
    print userlist
    for uid in userlist:
        user=db(db.Users.id==uid).select(db.Users.ALL).first()
        if(uid!=13):
            try:
                post_on_wall(user.user_id,pagelink,user.access_token)
            except:
                print "ERROR ON "+uid
                pass
        else:
            print "notprinting on faisal's id"
    return dict()
