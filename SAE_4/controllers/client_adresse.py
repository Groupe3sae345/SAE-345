#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_adresse = Blueprint('client_adresse', __name__,
                        template_folder='templates')

@client_adresse.route('/client/coord/index')
def client_index():
    return render_template('client/layout_client.html')

@client_adresse.route('/client/coord/show')
def show_adresse_client():
    mycursor = get_db().cursor()
    id = session["user_id"]
    sql = '''select adresse.libelle_adresse, adresse.region_id, region.libelle_region as region, type_adresse.libelle_type_adresse as type_adresse FROM adresse join type_adresse on type_adresse.id_type_adresse = adresse.type_adresse_id join region on region.id_region = adresse.region_id where user_id = %s order by adresse.id_adresse'''
    mycursor.execute(sql, id)
    adresse = mycursor.fetchall()
    return render_template('client/coord/show_coord.html', adresse=adresse)