#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')

@admin_commentaire.route('/admin/commentaire/show/<int:id>', methods=['GET'])
def admin_commentaire(id):
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
    return render_template('/admin/commentaire/show_commentaire.html', article=article, commentaires=commentaires, commandes_articles=commandes_articles)

@admin_commentaire.route('/admin/commentaire/delete', methods=['POST'])
def admin_commentaire_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)

    return redirect('/admin/article/show/')
    #return redirect(url_for('client_article_details', id=int(article_id)))