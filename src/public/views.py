"""
Logic for dashboard related routes
"""

from flask import (Blueprint, escape, flash, render_template,
                   redirect, request, url_for)
from flask_login import current_user, login_required, login_user, logout_user

from .forms import  Formular
from ..data.database import db
from ..data.models import User, UserPasswordToken, Device_List
from ..data.util import generate_random_token
from ..decorators import reset_token_required
from ..emails import send_activation, send_password_reset
from ..extensions import login_manager
from flask_weasyprint import HTML, render_pdf
blueprint = Blueprint('public', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('public/index.tmpl')
@blueprint.route('/test', methods=['GET'])
def test():
    return 'Ok'




@blueprint.route('/graf', methods=['GET'])
def graf(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'Muj graf'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    return render_template('public/graf.tmpl', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)


import mimerender

mimerender.register_mime('pdf', ('application/pdf',))
mimerender = mimerender.FlaskMimeRender(global_charset='UTF-8')

def render_pdf(html):
    from xhtml2pdf import pisa
    from StringIO import StringIO
    pdf = StringIO()
    pisa.CreatePDF(StringIO(html.encode('utf-8')), pdf)
    resp = pdf.getvalue()
    pdf.close()
    return resp

@blueprint.route('/vystuppdf', methods=['GET'])
@mimerender(default='html', html=lambda html: html, pdf=render_pdf, override_input_key='format')
def vystuppdf():
    html = render_template('public/vystuppdf.tmpl')
    return { 'html': html } # mimerender requires a dict

from flask_weasyprint import HTML, render_pdf
@blueprint.route('/vystuppdf1', methods=['GET'])
def vystuppdf1():
    html = render_template('public/vystuppdf.tmpl')
    return render_pdf(HTML(string=html))

@blueprint.route('/formular', methods=['GET', 'POST'])
def formularhodnotanew1():
    data=[]
    form = Formular()
    if form.validate_on_submit():
        data['hodnota']=int(form.cislo1.data) * int(form.cislo2.data)
        return render_template('public/formularhodnota.tmpl',hodnota = data)
    return render_template("public/formular.tmpl", form=form, hodnota = data)

