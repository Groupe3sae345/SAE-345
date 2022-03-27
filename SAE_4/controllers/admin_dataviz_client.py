#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_dataviz_client = Blueprint('admin_dataviz_client', __name__,
                         template_folder='templates')

@admin_dataviz_client.route('/admin/client/dataviz')
def admin_client_show():
    mycursor = get_db().cursor()
    sql = '''SELECT libelle_region,COUNT(region_id) as count from adresse join region r on r.id_region = adresse.region_id group by region_id;'''
    mycursor.execute(sql)
    values = mycursor.fetchall()
    value = []
    label = []
    for k in values:
        value.append(k['count'])
        label.append(k['libelle_region'])
    return render_template('admin/client/dataviz_client.html', labels=label, values=value)
