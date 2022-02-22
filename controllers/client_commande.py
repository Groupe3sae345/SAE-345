#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    date = datetime.now().strftime('%Y-%m-%d')
    id_etat = 1
    id_user = session['user_id']
    tuple = (date, id_etat, id_user)

    sql = "insert into commande(date_achat, etat_id, user_id) values(%s,%s,%s);"
    mycursor.execute(sql, tuple)

    sql = "select last_insert_id() as last_insert_id from commande where user_id = %s;"
    mycursor.execute(sql, id_user)
    commande_last_id = mycursor.fetchone()

    sql = "select * from panier where user_id = %s;"
    mycursor.execute(sql, id_user)
    panier = mycursor.fetchall()

    for item in panier:
        sql = "select prix_ski from ski where id_ski = %s;"
        mycursor.execute(sql, item['ski_id'])
        prix = mycursor.fetchone()
        sql = '''insert into ligne_commande(ski_id, commande_id, prix_unit, quantite) values (%s,%s,%s,%s);'''
        mycursor.execute(sql, (item['ski_id'], commande_last_id['last_insert_id'], prix['prix_ski'], item['quantite']))

    sql = '''select * from ligne_commande;'''
    mycursor.execute(sql)
    result = mycursor.fetchall()
    print(result)

    sql = "delete from panier where user_id = %s;"
    mycursor.execute(sql, id_user)
    get_db().commit()
    flash(u'Commande ajoutée')
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))



@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    client_id = session['user_id']
    idCommande = request.form.get('idCommande')
    mycursor = get_db().cursor()
    sql = '''select commande.id_commande as id, commande.date_achat as date_achat, SUM(ligne_commande.quantite) as quantite, SUM(ski.prix_ski * ligne_commande.quantite) as prix_total, commande.etat_id, etat.libelle from commande join ligne_commande on ligne_commande.commande_id = commande.id_commande join ski on ski.id_ski = ligne_commande.ski_id join etat on etat.id_etat = commande.etat_id where commande.user_id = %s group by commande.id_commande'''
    mycursor.execute(sql, client_id)
    commandes = mycursor.fetchall()
    sql = '''select fabricant.nom_fabricant as nom, ski.prix_ski as prix, SUM(ligne_commande.quantite) as quantite, SUM(ski.prix_ski * ligne_commande.quantite) as prix_ligne from commande join ligne_commande on ligne_commande.commande_id = commande.id_commande join ski on ski.id_ski = ligne_commande.ski_id join fabricant on ski.fabricant_id = fabricant.id_fabricant where commande.id_commande = %s group by fabricant.nom_fabricant, ligne_commande.quantite, ski.prix_ski'''
    mycursor.execute(sql, idCommande)
    articles_commande = mycursor.fetchall()
    return render_template('client/commandes/show.html', commandes=commandes, articles_commande=articles_commande)

