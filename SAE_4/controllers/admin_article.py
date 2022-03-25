#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                        template_folder='templates')

@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = "SELECT ski.*, fabricant.nom_fabricant, type_ski.libelle, fournisseur.nom_fournisseur FROM ski join type_ski on ski.type_ski_id = type_ski.id_type_ski join fabricant on ski.fabricant_id = fabricant.id_fabricant join fournisseur on ski.fournisseur_id = fournisseur.id_fournisseur order by ski.id_ski"
    mycursor.execute(sql)
    ski = mycursor.fetchall()
    return render_template('admin/article/show_article.html', articles=ski)

@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM type_ski"
    mycursor.execute(sql)
    type_ski = mycursor.fetchall()
    sql = "SELECT * FROM fabricant"
    mycursor.execute(sql)
    fab = mycursor.fetchall()
    sql = "SELECT * FROM fournisseur"
    mycursor.execute(sql)
    frn = mycursor.fetchall()
    return render_template('admin/article/add_article.html', type_ski=type_ski, fab=fab, frn=frn)

@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    nom = request.form.get('nom', '')
    type_article_id = request.form.get('type_ski_id', '')
   # type_article_id = int(type_article_id)
    prix = request.form.get('prix', '')
    stock = request.form.get('stock', '')
    longueur = request.form.get('longueur', '')
    fournisseur = request.form.get('fournisseur', '')
    tuple_insert = (nom, type_article_id, prix, stock, longueur, fournisseur)
    mycursor = get_db().cursor()
    sql = '''INSERT INTO ski(fabricant_id,type_ski_id,prix_ski,stock,longueur,fournisseur_id) VALUES (%s, %s, %s, %s, %s, %s); '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print(u'article ajouté , nom: ', nom, ' - type_article:', type_article_id, ' - prix:', prix, ' - stock:', stock, ' - longueur:', longueur, ' - fournisseur:', fournisseur)
    message = u'article ajouté , nom:'+nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - stock:'+  stock + ' - longueur:' + longueur + ' - fournisseur:' + fournisseur
    flash(message)
    return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/delete', methods=['POST'])
def delete_article():
    id = request.args.get('id', '')
    tuple_delete = (id)
    mycursor = get_db().cursor()
    sql = "DELETE FROM ski WHERE id_ski = %s;"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    print("un article supprimé, id :", id)
    flash(u'un article supprimé, id : ' + id)
    return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/edit/<int:id>', methods=['GET'])
def edit_article(id):
    mycursor = get_db().cursor()
    sql = "SELECT * FROM ski WHERE id_ski = %s;"
    mycursor.execute(sql, (id))
    ski = mycursor.fetchone()
    sql = "SELECT * FROM type_ski;"
    mycursor.execute(sql)
    type_ski = mycursor.fetchall()
    sql = "SELECT * FROM fabricant"
    mycursor.execute(sql)
    fab = mycursor.fetchall()
    sql = "SELECT * FROM fournisseur"
    mycursor.execute(sql)
    frn = mycursor.fetchall()
    return render_template('admin/article/edit_article.html', ski=ski, type_ski=type_ski, fab=fab, frn=frn)

@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    id = request.args.get('id', '')
    nom = request.form.get('nom', '')
    type_article_id = request.form.get('type_ski_id', '')
    prix = request.form.get('prix', '')
    stock = request.form.get('stock', '')
    longueur = request.form.get('longueur', '')
    fournisseur = request.form.get('fournisseur', '')
    tuple_insert = (nom, type_article_id, prix, stock, longueur, fournisseur, id)
    print(tuple_insert)
    mycursor = get_db().cursor()
    sql = '''UPDATE ski SET fabricant_id = %s,type_ski_id = %s,prix_ski = %s,stock = %s,longueur = %s,fournisseur_id = %s WHERE id_ski = %s; '''
    print(sql)
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print(u'article modifié , nom: ', nom, ' - type_article:', type_article_id, ' - prix:', prix, ' - stock:', stock,' - longueur:', longueur, ' - fournisseur:', fournisseur)
    message = u'article modifié , nom:' + nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - stock:' + stock + ' - longueur:' + longueur + ' - fournisseur:' + fournisseur
    flash(message)
    return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/commentaire/<int:id>', methods=['GET'])
def admin_article_commentaire(id):
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
    return render_template('admin/article/commentaire_article.html', article=article, commentaires=commentaires, commandes_articles=commandes_articles)