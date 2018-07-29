from flask import Flask, render_template, redirect, request, session, url_for, Blueprint
import base64

main = Blueprint('main', __name__, template_folder='templates/main')

@main.route('/view', methods=['GET'])
def view():
    image_url = base64.b64decode(request.args.get('id')).decode()
    return render_template('vrview/view.html', image_url=image_url)
