#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')


@client_article.route('/client/index')


@client_article.route('/client/article/show')      # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    sql = "select ski.*, avis.*, AVG(avis.note) as moy_notes, COUNT(id_avis) as nb_avis, fabricant.nom_fabricant, type_ski.libelle from ski join fabricant on ski.fabricant_id = fabricant.id_fabricant join type_ski on type_ski.id_type_ski=ski.type_ski_id left join avis on avis.ski_id = ski.id_ski"
    list_param = []
    condition_and = ""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " where "
    if "filter_word" in session:
        sql = sql + "fabricant.nom_fabricant like %s "
        recherche = "%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = "and "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sql = sql + condition_and + "prix_ski between %s and %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = "and "
    if "filter_types" in session:
        sql = sql + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sql = sql + "type_ski_id = %s "
            if item != last_item:
                sql = sql + "or "
            list_param.append(item)
        sql = sql + ")"
    sql = sql + " group by ski.id_ski, avis.id_avis, fabricant.nom_fabricant, type_ski.libelle order by fabricant.nom_fabricant, ski.id_ski;"
    print(sql)
    tuple_sql = tuple(list_param)
    mycursor.execute(sql, tuple_sql)
    skis = mycursor.fetchall()
    articles = skis
    sql = "select * from type_ski"
    mycursor.execute(sql)
    type_ski = mycursor.fetchall()
    types_articles = type_ski
    client_id = session['user_id']
    sql = "select * , ski.prix_ski as prix , concat(fabricant.nom_fabricant ,ski_id) as nom from panier join ski on panier.ski_id = ski.id_ski join fabricant on ski.fabricant_id = fabricant.id_fabricant WHERE user_id = %s"
    mycursor.execute(sql, client_id)
    articles_panier = mycursor.fetchall()
    sql = "select SUM(ski.prix_ski * panier.quantite) as sous_total from panier join ski on panier.ski_id = ski.id_ski where user_id = %s"
    mycursor.execute(sql, client_id)
    prix_total = mycursor.fetchone()['sous_total']
    print(prix_total)
    return render_template('client/boutique/panier_article.html', articles=articles, prix_total=prix_total, articlesPanier=articles_panier, itemsFiltre=types_articles)

@client_article.route('/client/article/details/<int:id>', methods=['GET'])
def client_article_details(id):
    mycursor = get_db().cursor()
    tuple_insert= (id)
    sql = "select *, fabricant.nom_fabricant, type_ski.libelle, ski.image from ski join fabricant on ski.fabricant_id = fabricant.id_fabricant join type_ski on type_ski.id_type_ski=ski.type_ski_id where ski.id_ski=%s"
    mycursor.execute(sql, tuple_insert)
    skis = mycursor.fetchall()
    article = skis
    sql = "select * , ski.prix_ski as prix , concat(fabricant.nom_fabricant ,ski_id) as nom from panier join ski on panier.ski_id = ski.id_ski join fabricant on ski.fabricant_id = fabricant.id_fabricant"
    mycursor.execute(sql)
    articles_panier = mycursor.fetchall()
    commandes_articles = articles_panier
    sql = "select * from avis where ski_id = %s"
    mycursor.execute(sql, id)
    commentaires = mycursor.fetchall()
    return render_template('client/boutique/article_details.html', article=article, commentaires=commentaires, commandes_articles=commandes_articles)
