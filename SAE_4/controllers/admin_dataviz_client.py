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
    sql = '''select region.libelle_region FROM region'''
    mycursor.execute(sql)
    labels = mycursor.fetchall()
    sql = '''select COUNT(region.libelle_region) FROM region'''
    mycursor.execute(sql)
    values = mycursor.fetchall()
    return render_template('admin/client/dataviz_client.html', labels=labels, values=values)
