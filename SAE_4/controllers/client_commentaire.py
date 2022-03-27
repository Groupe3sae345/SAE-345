#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')

@client_commentaire.route('/client/comment/add', methods=['GET'])
#@client_commentaire.route('/client/comment/add/<int:id>', methods=['GET'])
def add_commentaire():
    mycursor = get_db().cursor()
    sql='''SELECT * FROM avis'''
    mycursor.execute(sql)
    #mycursor.execute(sql, (id))
    return render_template('client/boutique/add_commentaire.html')

@client_commentaire.route('/client/comment/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    article_id = '6'
    #article_id = request.form.get('id', '')
    user_id = session["user_id"]
    commentaire = request.form.get('commentaire', '')
    note = request.form.get('note', '')
    tuple_insert = (article_id, user_id, commentaire, note)
    sql = '''INSERT INTO avis(ski_id,user_id,commentaire,note) VALUES (%s, %s, %s, %s); '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print(u'commentaire ajouté')
    message='commentaire ajouté'
    flash(message)

    return redirect('/client/article/details/'+article_id)
    #return redirect(url_for('client_article_details', id=int(article_id)))

@client_commentaire.route('/client/comment/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)

    return redirect('/client/article/details/'+article_id)
    #return redirect(url_for('client_article_details', id=int(article_id)))