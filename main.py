# this file generates the main page with list of cards and allows adding new ones
import mammoth
from flask import Flask, render_template, request
import os
from xml.sax.saxutils import unescape


def show_description(path):
    with open(path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value


if __name__ == '__main__':
    app = Flask(__name__)

    data_dir = 'static'
    main_jpg = 'main.jpg'

    @app.route('/')
    @app.route('/index')
    def hello():
        show = request.args.get('show')
        cards = []
        i = 0
        for folder in os.listdir(data_dir):
            if os.path.exists(os.path.join(data_dir, folder, main_jpg)):
                i += 1
                cards.append({
                    'title': folder,
                    'image': os.path.join(folder, main_jpg),
                    'r': i % 3
                })

        card = None
        if show is not None:
            card = {
                'title': show,
                'image': os.path.join(show, main_jpg),
                'short': unescape(show_description(os.path.join('static', show, 'short.docx'))),
                'long': unescape(show_description(os.path.join('static', show, 'long.docx'))),
            }

        return render_template('index.html', title='Welcome', cards=cards, show=card)

    app.run(debug=True)
