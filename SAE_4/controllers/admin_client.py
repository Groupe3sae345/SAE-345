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
    sql='''select user.username, adresse.id_adresse, adresse.libelle_adresse, adresse.region, adresse.type_adresse FROM adresse JOIN user on user.id_user = adresse.user_id'''
    mycursor.execute(sql)
    adresse =mycursor.fetchall()
    return render_template('admin/client/show_client.html', adresse=adresse)
