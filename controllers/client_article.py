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
    sql = "select *, fabricant.nom_fabricant, type_ski.libelle from ski join fabricant on ski.fabricant_id = fabricant.id_fabricant join type_ski on type_ski.id_type_ski=ski.type_ski_id order by fabricant.nom_fabricant"
    mycursor.execute(sql)
    skis = mycursor.fetchall()
    articles = skis
    sql = "select * from type_ski"
    mycursor.execute(sql)
    type_ski = mycursor.fetchall()
    types_articles = type_ski
    sql = "select * , ski.prix_ski as prix , concat(fabricant.nom_fabricant ,ski_id) as nom from panier join ski on panier.ski_id = ski.id_ski join fabricant on ski.fabricant_id = fabricant.id_fabricant"
    mycursor.execute(sql)
    articles_panier = mycursor.fetchall()
    #prix_total = articles_panier
    return render_template('client/boutique/panier_article.html', articles=articles, articlesPanier=articles_panier, itemsFiltre=types_articles)
#prix_total=prix_total,

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
    sql = "select * from avis"
    mycursor.execute(sql)
    commentaires = mycursor.fetchall()
    return render_template('client/boutique/article_details.html', article=article, commentaires=commentaires, commandes_articles=commandes_articles)
