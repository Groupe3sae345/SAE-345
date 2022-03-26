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
    sql='''select user.username, adresse.id_adresse, adresse.libelle_adresse, adresse.region, type_adresse.libelle_type_adresse as type_adresse FROM adresse JOIN user on user.id_user = adresse.user_id join type_adresse on type_adresse.id_type_adresse = adresse.type_adresse_id'''
    mycursor.execute(sql)
    adresse =mycursor.fetchall()
    return render_template('admin/client/show_client.html', adresse=adresse)

@admin_client.route('/admin/client/edit/<int:id>', methods=['GET'])
def admin_client_edit(id):
    mycursor = get_db().cursor()
    sql = "SELECT * FROM region"
    mycursor.execute(sql)
    region = mycursor.fetchall()
    sql = "SELECT id_user, username FROM user WHERE id_user = %s"
    mycursor.execute(sql, id)
    user = mycursor.fetchall()
    sql = "SELECT * FROM adresse where user_id = %s"
    mycursor.execute(sql, id)
    adresse = mycursor.fetchall()
    sql = "SELECT * FROM type_adresse"
    mycursor.execute(sql)
    type_adresse = mycursor.fetchall()
    return render_template('admin/client/edit_client.html', region=region, user=user, adresse=adresse, type=type_adresse)

@admin_client.route('/admin/client/edit', methods=['POST'])
def valid_edit_client():
    id = request.args.get('id', '')
    adresse = request.form.get('adresse', '')
    region = request.form.get('region', '')
    type = request.form.get('type', '')
    tuple_update = (adresse, type, region, id)
    print(tuple_update)
    mycursor = get_db().cursor()
    sql = '''UPDATE adresse SET libelle_adresse = %s, type_adresse_id = %s, region = %s WHERE user_id = %s;'''
    debug = mycursor.execute(sql, tuple_update)
    print(debug)
    get_db().commit()
    return redirect(url_for('admin_client.admin_client_show'))