#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')

@client_commentaire.route('/client/comment/add', methods=['GET'])
def add_commentaire():
    mycursor = get_db().cursor()
    sql='''SELECT * FROM avis'''
    mycursor.execute(sql)
    region = mycursor.fetchall()
    return render_template('client/article/add_adresse.html', region=region)

@client_commentaire.route('/client/comment/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    id = session["user_id"]
    commentaire = request.form.get('commentaire', '')
    note = request.form.get('note', '')
    tuple_insert = (commentaire, note, id)
    article_id = request.form.get('idArticle', None)

    return redirect('/client/article/details/'+article_id)
    #return redirect(url_for('client_article_details', id=int(article_id)))

@client_commentaire.route('/client/comment/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)

    return redirect('/client/article/details/'+article_id)
    #return redirect(url_for('client_article_details', id=int(article_id)))