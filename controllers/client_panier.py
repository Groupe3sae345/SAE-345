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
    quantite = request.form.get('quantite')

    sql = "SELECT * FROM panier WHERE article_id = %s AND user_id=%s"
    mycursor.execute(sql, (id_article, client_id))
    article_panier = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ski WHERE id_ski = %s", (id_article))
    article = mycursor.fetchone()

    if not (article_panier is None) and article_panier['quantite'] >= 1:
        tuple_update = (quantite, client_id, id_article)
        sql = "alter table panier drop foreign key fk_panier_article;" \
              "UPDATE panier SET quantite = quantite+%s WHERE user_id = %s AND article_id=%s"
        mycursor.execute(sql, tuple_update)
    else:
        tuple_insert = (client_id, id_article, quantite)
        sql = "INSERT INTO panier(user_id,article_id,quantite) VALUES (%s,%s,%s)"
        mycursor.execute(sql, tuple_insert)

    get_db().commit()
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()

    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()

    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()

    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    # SQL
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

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
