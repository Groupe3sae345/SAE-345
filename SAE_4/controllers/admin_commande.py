#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    idCommande = request.form.get('idCommande')
    mycursor = get_db().cursor()
    if idCommande is None:
        articles_commande = None
    else:
        sql = '''select fabricant.nom_fabricant as nom, ski.prix_ski as prix, SUM(ligne_commande.quantite) as quantite, SUM(ski.prix_ski * ligne_commande.quantite) as prix_ligne from commande join ligne_commande on ligne_commande.commande_id = commande.id_commande join ski on ski.id_ski = ligne_commande.ski_id join fabricant on ski.fabricant_id = fabricant.id_fabricant where commande.id_commande = %s group by fabricant.nom_fabricant, ligne_commande.quantite, ski.prix_ski'''
        mycursor.execute(sql, idCommande)
        articles_commande = mycursor.fetchall()

    sql = '''select commande.id_commande as id, commande.date_achat as date_achat, SUM(ligne_commande.quantite) as quantite, SUM(ski.prix_ski * ligne_commande.quantite) as prix_total, commande.etat_id, etat.libelle from commande join ligne_commande on ligne_commande.commande_id = commande.id_commande join ski on ski.id_ski = ligne_commande.ski_id join etat on etat.id_etat = commande.etat_id group by commande.id_commande order by commande.etat_id ASC, commande.id_commande, commande.date_achat'''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    return render_template('admin/commandes/show.html', commandes=commandes, articles_commande=articles_commande)


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    idCommande = request.form.get('idCommande')
    mycursor = get_db().cursor()
    sql = '''update commande set commande.etat_id = 2 where commande.id_commande = %s'''
    mycursor.execute(sql, idCommande)
    get_db().commit()
    return redirect('/admin/commande/show')
