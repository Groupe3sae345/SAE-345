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

@client_panier.route('/client/panier/filtre')
def show_selec():
    mycursor = get_db().cursor()
    sql = "select fabricant.nom_fabricant, ski.*, type_ski.* from ski join fabricant on ski.fabricant_id = fabricant.id_fabricant join type_ski on ski.type_ski_id = type_ski.id_type_ski"
    list_param = []
    condition_and=""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql=sql+" where "
    if "filter_word" in session:
        sql=sql+"nom_fabricant like %s "
        recherche="%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and="and "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sql=sql+condition_and+"prix_ski between %s and %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and="and "
    if "filter_types" in session:
        sql=sql+condition_and+"("
        last_item=session['filter_types'][-1]
        for item in session['filter_types']:
            sql=sql+"type_ski_id = %s "
            if item != last_item:
                sql=sql+"or "
            list_param.append(item)
        sql=sql+")"
    sql=sql+";"
    tuple_sql=tuple(list_param)
    mycursor.execute(sql, tuple_sql)
    ski=mycursor.fetchall()
    print(ski)
    return render_template('/client/boutique/_filtres.html', itemsFiltre=ski)

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
                flash(u' votre Mot de recherché doit être composé uniquement de lettres')
        else:
            if len(filter_word) == 1:
                flash(u'votre Mot recherché doit être composé de au moins 2 lettres')
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
            flash(u'min et max doivent être des numériques')
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
