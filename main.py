from flask import Flask, render_template, redirect, request, session, url_for, Blueprint
import base64

main = Blueprint('main', __name__, template_folder='templates/main')

@main.route('/view/<image_id>')
def view(image_id):
    image_id = base64.b64decode(image_id).decode()
    title = 'Petra'
    article = 'Petra, originally known to its inhabitants as Raqmu, is a historical and archaeological city in southern Jordan.'
    tags = ['cool', 'wow', 'beautiful']
    return render_template(
        'vrview/view.html', 
        image_url=image_id, 
        current_url=request.base_url,
        title=title,
        article=article, 
        tags=tags
    )

@main.route('/upload')
def upload():
    return 'unavailable at the moment'

@main.route('/search')
def search():
    return 'unavailable at the moment'
