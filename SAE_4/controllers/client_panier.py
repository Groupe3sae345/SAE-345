#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    client_id = session['user_id']
    id_article = request.form.get('idArticle')
    sql = "SELECT * FROM panier WHERE ski_id = %s AND user_id=%s"
    mycursor.execute(sql, (id_article, client_id))
    article_panier = mycursor.fetchone()
    mycursor.execute("SELECT * FROM ski WHERE id_ski = %s", (id_article))
    article = mycursor.fetchone()
    if not (article_panier is None) and article_panier['quantite'] >= 1:
        tuple_update = (client_id, id_article)
        sql = "UPDATE panier SET quantite = quantite+1 WHERE user_id = %s AND ski_id=%s"
        mycursor.execute(sql, tuple_update)
        tuple_update2 = (id_article)
        sql = "UPDATE ski SET stock = stock-1 WHERE id_ski=%s"
        mycursor.execute(sql, tuple_update2)
    else:
        quantite = request.form.get('quantite')
        tuple_insert = (client_id, id_article, quantite)
        sql = "INSERT INTO panier(user_id,ski_id,quantite) VALUES (%s,%s,%s)"
        mycursor.execute(sql, tuple_insert)
        tuple_update2 = (quantite, id_article)
        sql = "UPDATE ski SET stock = stock-%s WHERE id_ski=%s"
        mycursor.execute(sql, tuple_update2)
    get_db().commit()
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    client_id = session['user_id']
    id_article = request.form.get('idArticle')
    sql = "SELECT * FROM panier WHERE ski_id = %s AND user_id=%s"
    mycursor.execute(sql, (id_article, client_id))
    article_panier = mycursor.fetchone()
    mycursor.execute("SELECT * FROM ski WHERE id_ski = %s", (id_article))
    article = mycursor.fetchone()
    id_article = request.form.get('idArticle')
    tuple_delete = (client_id, id_article)
    quantite = request.form.get('quantite')
    if (article_panier['quantite'] > 1):
        sql = "UPDATE panier set quantite = quantite-1 WHERE user_id = %s AND ski_id=%s"
        mycursor.execute(sql, tuple_delete)
        id_article = request.form.get('idArticle')
        tuple_update2 = (id_article)
        sql = "UPDATE ski SET stock = stock+1 WHERE id_ski=%s"
        mycursor.execute(sql, tuple_update2)
    else:
        id_article = request.form.get('idArticle')
        tuple_delete = (id_article)
        sql = "DELETE FROM panier WHERE ski_id=%s"
        mycursor.execute(sql, tuple_delete)
        id_article = request.form.get('idArticle')
        tuple_update2 = (id_article)
        sql = "UPDATE ski SET stock = stock+1 WHERE id_ski=%s"
        mycursor.execute(sql, tuple_update2)
    get_db().commit()
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    idUser = session['user_id']
    sql = '''select quantite, ski_id from panier where user_id = %s;'''
    mycursor.execute(sql, idUser)
    panier = mycursor.fetchall()
    for i in range(0, len(panier)):
        lignePanier = panier[i]
        sql = '''update ski set stock = stock + %s where id_ski = %s;'''
        mycursor.execute(sql, (lignePanier['quantite'], lignePanier['ski_id']))
        get_db().commit()
    sql = "delete from panier where user_id = %s;"
    mycursor.execute(sql, idUser)
    get_db().commit()
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    client_id = session['user_id']
    id_article = request.form.get('idArticle')
    mycursor = get_db().cursor()
    tuple_select = (client_id, id_article)
    print(tuple_select)
    sql = "SELECT quantite FROM panier WHERE user_id = %s AND ski_id=%s"
    mycursor.execute(sql, tuple_select)
    quantite = mycursor.fetchone()['quantite']
    print(quantite)
    tuple_update2 = (quantite, id_article)
    sql = "UPDATE ski SET stock = stock+%s WHERE id_ski=%s"
    mycursor.execute(sql, tuple_update2)
    tuple_delete = id_article
    sql = "DELETE FROM panier WHERE ski_id=%s"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word')
    filter_types = request.form.getlist('filter_types')
    filter_prix_min = request.form.get('filter_prix_min')
    filter_prix_max = request.form.get('filter_prix_max')
    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u' votre Mot de recherch?? doit ??tre compos?? uniquement de lettres')
        else:
            if len(filter_word) == 1:
                flash(u'votre Mot recherch?? doit ??tre compos?? de au moins 2 lettres')
            else:
                session.pop('filter_word', None)
    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash(u'min < max')
        else:
            flash(u'min et max doivent ??tre des num??riques')
    if filter_types and filter_types != []:
        print("filter_types:", filter_types)
        if isinstance(filter_types, list):
            check_filter_type = True
            for number_type in filter_types:
                print("test", number_type)
                if not number_type.isdecimal():
                    check_filter_type = False
                if check_filter_type:
                    session['filter_types'] = filter_types
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))
