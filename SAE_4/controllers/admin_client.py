#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_client = Blueprint('admin_client', __name__,
                        template_folder='templates')

@admin_client.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')

@admin_client.route('/admin/client/show')
def admin_client_show():
    mycursor = get_db().cursor()
    sql='''select user.username, user.id_user, adresse.id_adresse, adresse.libelle_adresse, adresse.region_id, region.libelle_region as region, type_adresse.libelle_type_adresse as type_adresse FROM adresse JOIN user on user.id_user = adresse.user_id join type_adresse on type_adresse.id_type_adresse = adresse.type_adresse_id join region on region.id_region = adresse.region_id order by  user.username, adresse.id_adresse'''
    mycursor.execute(sql)
    adresse = mycursor.fetchall()
    return render_template('admin/client/show_client.html', adresse=adresse)

@admin_client.route('/admin/client/edit/<int:id>', methods=['GET'])
def admin_client_edit(id):
    mycursor = get_db().cursor()
    sql = "SELECT * FROM region"
    mycursor.execute(sql)
    region = mycursor.fetchall()
    sql = "SELECT id_user, username FROM user where id_user = %s"
    mycursor.execute(sql, id)
    user = mycursor.fetchone()
    print(user)
    sql = "SELECT * FROM adresse where user_id = %s"
    mycursor.execute(sql, id)
    adresse = mycursor.fetchone()
    sql = "SELECT * FROM type_adresse"
    mycursor.execute(sql)
    type_adresse = mycursor.fetchall()
    print(adresse)
    return render_template('admin/client/edit_client.html', region=region, user=user, adresse=adresse, type=type_adresse)

@admin_client.route('/admin/client/edit', methods=['POST'])
def valid_edit_client():
    id = request.form.get('id', '')
    adresse = request.form.get('adresse', '')
    region = request.form.get('region', '')
    type = request.form.get('type', '')
    tuple_update = (adresse, type, region, id)
    print(tuple_update)
    mycursor = get_db().cursor()
    sql = '''UPDATE adresse SET libelle_adresse = %s, type_adresse_id = %s, region_id = %s WHERE user_id = %s;'''
    debug = mycursor.execute(sql, tuple_update)
    print(debug)
    get_db().commit()
    return redirect(url_for('admin_client.admin_client_show'))

@admin_client.route('/admin/client/delete', methods=['GET'])
def delete_client():
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    sql='''SELECT COUNT(id_adresse) as nb_addr FROM adresse where user_id = %s'''
    mycursor.execute(sql, id)
    nb_addr = mycursor.fetchone()['nb_addr']
    print(nb_addr)
    if(nb_addr <= 1):
        print("Impossible de supprimer, il faut obligatoirement une adresse pour un client ")
        flash(u'Impossible de supprimer, il faut obligatoirement une adresse pour un client')
        return redirect(url_for('admin_client.admin_client_show'))
    else:
        sql = '''select user.username, user.id_user, adresse.id_adresse, adresse.libelle_adresse, adresse.region_id, region.libelle_region as region, type_adresse.libelle_type_adresse as type_adresse FROM adresse JOIN user on user.id_user = adresse.user_id join type_adresse on type_adresse.id_type_adresse = adresse.type_adresse_id join region on region.id_region = adresse.region_id where user_id = %s order by user.username, adresse.id_adresse'''
        mycursor.execute(sql, id)
        adresse = mycursor.fetchall()
        return render_template('/admin/client/delete_client.html', adresse=adresse)

@admin_client.route('/admin/client/delete_adresse', methods=['GET'])
def delete_client_adresse():
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    sql = '''SELECT COUNT(id_adresse) as nb_addr FROM adresse where user_id = %s'''
    mycursor.execute(sql, id)
    nb_addr = mycursor.fetchone()['nb_addr']
    print(nb_addr)
    if (nb_addr <= 1):
        sql = '''DELETE FROM adresse where id_adresse = %s'''
        mycursor.execute(sql, id)
        get_db().commit()
        return redirect(url_for('admin_client.admin_client_show'))
    else:
        sql = '''DELETE FROM adresse where id_adresse = %s'''
        mycursor.execute(sql, id)
        get_db().commit()
        return redirect(url_for('admin_client.delete_client_adresse'))
