#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_type_article = Blueprint('admin_type_article', __name__,
                        template_folder='templates')

@admin_type_article.route('/admin/type-article/show')
def show_type_article():
    mycursor = get_db().cursor()
    sql = '''
        SELECT type_ski.*, 
            COUNT(id_ski) as nb_ski 
        FROM type_ski 
        LEFT JOIN ski on ski.type_ski_id = type_ski.id_type_ski 
        group by id_type_ski 
        order by id_type_ski'''
    mycursor.execute(sql)
    type_ski = mycursor.fetchall()
    return render_template('admin/type_article/show_type_article.html', types_articles=type_ski)

@admin_type_article.route('/admin/type-article/add', methods=['GET'])
def add_type_article():
    return render_template('admin/type_article/add_type_article.html')

@admin_type_article.route('/admin/type-article/add', methods=['POST'])
def valid_add_type_article():
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle)
    sql = "INSERT INTO type_ski(libelle) VALUES (%s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message)
    return redirect('/admin/type-article/show') #url_for('show_type_article')

@admin_type_article.route('/admin/type-article/delete', methods=['GET'])
def delete_type_article():
    type_ski_id = request.args.get('id', '')
    tuple_delete = (type_ski_id)
    mycursor = get_db().cursor()
    sql = "SELECT COUNT(type_ski_id) as nb_ski FROM ski where type_ski_id = %s "
    mycursor.execute(sql, tuple_delete)
    nb = mycursor.fetchall()
    if (nb[0]['nb_ski'] == 0):
        type_ski_id = request.args.get('id', '')
        tuple_delete = (type_ski_id)
        sql = "DELETE FROM type_ski WHERE id_type_ski = %s;"
        mycursor.execute(sql, tuple_delete)
        get_db().commit()
        return redirect('/admin/type-article/show')
    else:
        type_ski_id = request.args.get('id', '')
        tuple_delete = (type_ski_id)
        sql = "SELECT ski.*, fabricant.nom_fabricant FROM ski join fabricant on ski.fabricant_id = fabricant.id_fabricant WHERE type_ski_id = %s "
        mycursor.execute(sql, tuple_delete)
        ski = mycursor.fetchall()
        get_db().commit()
        return render_template('/admin/type_article/delete_type_article.html', ski=ski, id=type_ski_id)

@admin_type_article.route('/admin/type-article/edit/<int:id>', methods=['GET'])
def edit_type_article(id):
    mycursor = get_db().cursor()
    sql = "SELECT id_type_ski, libelle FROM type_ski WHERE id_type_ski = %s;"
    mycursor.execute(sql, (id))
    type_article = mycursor.fetchone()
    return render_template('admin/type_article/edit_type_article.html', type_article=type_article)

@admin_type_article.route('/admin/type-article/edit', methods=['POST'])
def valid_edit_type_article():
    libelle = request.form.get('libelle', '')
    id_type_article = request.form.get('id', '')
    tuple_update = (libelle, id_type_article)
    mycursor = get_db().cursor()
    sql = '''UPDATE type_ski SET libelle = %s WHERE id_type_ski = %s; '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type article modifié, id: ' + id_type_article + " libelle : " + libelle)
    return redirect('/admin/type-article/show') #url_for('show_type_article')






