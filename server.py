#!/usr/bin/env python3
import glob
import json
import os
import subprocess
import sys
from pathlib import Path

from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
from gooey import GooeyParser, Gooey

app = Flask(__name__, static_url_path='')

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    APPLICATION_PATH = Path(sys.executable).parent
elif __file__:
    APPLICATION_PATH = Path(__file__).parent

REPO_URL = 'https://github.com/commaai/comma10k/'

CONFIG = json.load(open('config.json', 'r'))

LOCAL_REPO_PATH = None
# IMAGES = sorted(glob.glob('../imgs/*.png'))
IMAGES = []


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/imgs/<path:path>')
def send_img(path):
    return send_from_directory('../imgs', path)


@app.route('/masks/<path:path>')
def send_mask(path):
    return send_from_directory('../masks', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static', path)


@app.route('/')
def base():
    return redirect("/pencil")


# index
@app.route('/pencil/')
def index():
    img_id = int(request.args.get('id', 0))
    if img_id < 0:
        return redirect("/pencil?id=0")
    elif img_id >= len(IMAGES):
        return redirect("/pencil?id=" + str(len(IMAGES) - 1))
    img_name = Path(IMAGES[img_id]).parts[-1]
    data = {'total_images': len(IMAGES), 'img_id': img_id, 'img_name': img_name, 'config': CONFIG}
    return render_template("pencil.html", data=data)


@app.route('/hub-action/')
def hub():
    img_name = request.args.get('imgfile', '')
    # print(img_name)
    if img_name == '':
        return jsonify({"out": "no-file", "err": ""})
    else:
        file_location = 'masks/' + img_name
        print(file_location, os.path.exists(file_location))
        process = subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if img_name in out.decode("utf-8"):
            process = subprocess.Popen(['git', 'add', file_location], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print('\n\n', {"out": str(out.decode("utf-8")), "err": str(err.decode("utf-8"))})

            process = subprocess.Popen(
                ['git', 'commit', '-m', '" add mask : ' + REPO_URL + 'blob/master/imgs/' + img_name + '"'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print('\n\n', {"out": str(out.decode("utf-8")), "err": str(err.decode("utf-8"))})

            process = subprocess.Popen(['git', 'push'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print('\n\n', {"out": str(out.decode("utf-8")), "err": str(err.decode("utf-8"))})

            process = subprocess.Popen(
                ['hub', 'pull-request', '-m', '" add mask : ' + REPO_URL + 'blob/master/imgs/' + img_name + '"'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print({"out": str(out.decode("utf-8")), "err": str(err.decode("utf-8"))})
        # print({"out":str(out.decode("utf-8")), "err": str(err.decode("utf-8") )})
        return jsonify('\n\n', {"out": str(out.decode("utf-8")), "err": str(err.decode("utf-8"))})


@Gooey
def main():
    parser = GooeyParser(description="Tool for Comma10k")
    parser.add_argument('comma10k_dir', widget="DirChooser")
    parser.parse_args()

    app.run(debug=False)


if __name__ == "__main__":
    main()
