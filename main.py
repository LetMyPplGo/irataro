# this file generates the main page with list of cards and allows adding new ones
import mammoth
from flask import Flask, render_template, request
import os
from xml.sax.saxutils import unescape
import sys


def show_description(path):
    with open(path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return unescape(result.value)


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    else:
        application_path = os.path.dirname(sys.argv[0])

    print(application_path)

    app = Flask(__name__, static_folder=os.path.join(application_path, 'static'))

    data_dir = 'static'
    main_jpg = 'main.jpg'

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('frameset.html')


    @app.route('/left.html')
    def left():
        folders = [
            'Старшие арканы',
            'Придворные карты',
            'Ситуационные посохов',
            'Ситуационные кубков',
            'Ситуационные мечей',
            'Ситуационные пентаклей',
        ]
        cards = []
        for upper_dir in folders:
            group = {'name': upper_dir, 'cards': []}
            for folder in os.listdir(os.path.join(data_dir, upper_dir)):
                if os.path.exists(os.path.join(data_dir, upper_dir, folder, main_jpg)):
                    group['cards'].append({
                        'title': folder,
                        'group': upper_dir,
                        'image': os.path.join(folder, main_jpg),
                    })
            cards.append(group)

        return render_template('left.html', cards=cards)


    @app.route('/right.html')
    def right():
        show = request.args.get('show')
        group = request.args.get('group')
        card = None
        if show is not None:
            card = {
                'title': show,
                # 'image': os.path.join(group, show, main_jpg),
                'image': f'{group}/{show}/{main_jpg}',
                'short': show_description(os.path.join('static', group, show, 'short.docx')),
                'long': show_description(os.path.join('static', group, show, 'long.docx')),
            }

        return render_template('right.html', show=card)

    app.run(debug=True)
