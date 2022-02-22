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
    mycursor = get_db().cursor()
    sql = '''select panier.user_id, commande.id_commande, commande.date_achat, ligne_commande.quantite, SUM(ski.prix_ski * panier.quantite) as prix_total, etat.libelle from commande join ligne_commande on commande.id_commande = ligne_commande.commande_id join ski on ligne_commande.ski_id = ski.id_ski join panier on ski.id_ski = panier.ski_id join etat on commande.etat_id = etat.id_etat group by id_commande where user_id = %s'''
    mycursor.execute(sql, client_id)
    commandes = mycursor.fetchall()
    sql = '''select SUM(ski.prix_ski * panier.quantite), ligne_commande.* as prix_total from panier join ski on panier.ski_id = ski.id_ski join ligne_commande on  where user_id = %s'''
    mycursor.execute(sql, client_id)
    articles_commande = mycursor.fetchall()
    return render_template('client/commandes/show.html', commandes=commandes, articles_commande=articles_commande)

