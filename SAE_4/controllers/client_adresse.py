#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_adresse = Blueprint('client_adresse', __name__,
                        template_folder='templates')

@client_adresse.route('/client/coord/show')
def show_adresse_client():
    mycursor = get_db().cursor()
    id = session["user_id"]
    sql = '''select adresse.id_adresse, adresse.libelle_adresse, adresse.region_id, region.libelle_region as region, type_adresse.libelle_type_adresse as type_adresse FROM adresse join type_adresse on type_adresse.id_type_adresse = adresse.type_adresse_id join region on region.id_region = adresse.region_id where user_id = %s order by adresse.id_adresse'''
    mycursor.execute(sql, id)
    adresse = mycursor.fetchall()
    return render_template('client/coord/show_coord.html', adresse=adresse)

@client_adresse.route('/client/coord/add', methods=['GET'])
def add_adresse():
    mycursor = get_db().cursor()
    sql='''SELECT * FROM region'''
    mycursor.execute(sql)
    region = mycursor.fetchall()
    return render_template('client/coord/add_adresse.html', region=region)

@client_adresse.route('/client/coord/add', methods=['POST'])
def valid_add_adresse():
    mycursor = get_db().cursor()
    id = session["user_id"]
    adresse = request.form.get('adresse', '')
    region = request.form.get('region', '')
    tuple_insert = (adresse, region, id)
    sql = "INSERT INTO adresse(libelle_adresse, type_adresse_id, region_id, user_id) VALUES (%s, 2, %s, %s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/coord/show') #url_for('show_adresse')

@client_adresse.route('/client/coord/delete', methods=['GET'])
def delete_adresse():
    id_user = session["user_id"]
    id_addr = request.args.get('id', '')
    mycursor = get_db().cursor()
    sql = "SELECT COUNT(id_adresse) as nb_addr FROM adresse where adresse.user_id = %s "
    mycursor.execute(sql, id_user)
    nb = mycursor.fetchall()
    if (nb[0]['nb_addr'] > 1):
        sql = "DELETE FROM adresse WHERE id_adresse = %s;"
        mycursor.execute(sql, id_addr)
        get_db().commit()
        return redirect('/client/coord/show')
    else:
        flash(u'Impossible de supprimer, vous devez avoir au moins une adresse enregistrée sur le compte')
        return redirect('/client/coord/show')


@client_adresse.route('/client/coord/edit/<int:id>', methods=['GET'])
def edit_adresse(id):
    mycursor = get_db().cursor()
    sql = "SELECT id_adresse, libelle_adresse, region_id FROM adresse WHERE id_adresse = %s;"
    mycursor.execute(sql, (id))
    adresse = mycursor.fetchone()
    sql = '''SELECT * FROM region'''
    mycursor.execute(sql)
    region = mycursor.fetchall()
    return render_template('client/coord/edit_adresse.html', adresse=adresse, region=region)

@client_adresse.route('/client/coord/edit', methods=['POST'])
def valid_edit_adresse():
    libelle = request.form.get('adresse', '')
    region = request.form.get('region', '')
    id_adresse = request.form.get('id', '')
    tuple_update = (libelle, region, id_adresse)
    print(tuple_update)
    mycursor = get_db().cursor()
    sql = '''UPDATE adresse SET libelle_adresse = %s, region_id = %s WHERE id_adresse = %s; '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type article modifié, id: ' + id_adresse + " libelle : " + libelle)
    return redirect('/client/coord/show') #url_for('show_adresse')
