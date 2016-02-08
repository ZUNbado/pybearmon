from flask import Flask, Blueprint,render_template, request, redirect, url_for
from app.common.sql import getdb
from app.contacts.controllers import Contacts
from telegram import Update
import urllib


app = Blueprint('telegram', __name__, url_prefix = '/integrations/telegram')
@app.route('/')
def telegram_start():
    update = Update.de_json(request.get_json(force=True))
    print update
    return ''
