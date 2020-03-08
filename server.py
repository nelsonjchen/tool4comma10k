#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from urllib.request import urlopen

from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
from gooey import GooeyParser, Gooey

from repo_operations import commit_with_message, fetch_reset_new_branch_upstream, create_push_pr_able_branch

# noinspection PyBroadException
try:
    import _version

    software_version = _version.software
except Exception:
    software_version = 'develop'

if getattr(sys, 'frozen', False):
    APPLICATION_PATH = Path(sys.executable).parent
else:
    APPLICATION_PATH = Path(__file__).parent

app = Flask(__name__, static_url_path='', template_folder=APPLICATION_PATH / 'templates')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

REPO_URL = 'https://github.com/commaai/comma10k/'

CONFIG = json.load(open(APPLICATION_PATH / 'config.json', 'r'))


@dataclass
class ToolPaths:
    local_repo_path: Path = None
    image_paths: List[Path] = field(default_factory=list)


tool_paths = ToolPaths()


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(Path(APPLICATION_PATH) / 'static', path)


@app.route('/imgs/<path:path>')
def send_img(path):
    return send_from_directory(tool_paths.local_repo_path / 'imgs', path)


@app.route('/masks/<path:path>', methods=['GET', 'POST'])
def send_mask(path):
    if request.method == 'POST':
        with urlopen(request.form['image']) as response:
            data = response.read()
            with open(tool_paths.local_repo_path / 'masks' / path, 'wb') as f:
                f.write(data)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    elif request.method == 'GET':
        return send_from_directory(tool_paths.local_repo_path / 'masks', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(Path(APPLICATION_PATH) / 'static', path)


@app.route('/')
def base():
    return redirect("/pencil")


# index
@app.route('/pencil/')
def index():
    img_id = int(request.args.get('id', 0))
    if img_id < 0:
        return redirect("/pencil?id=0")
    elif img_id >= len(tool_paths.image_paths):
        return redirect("/pencil?id=" + str(len(tool_paths.image_paths) - 1))
    img_name = tool_paths.image_paths[img_id].parts[-1]
    data = {
        'software_version': software_version,
        'total_images': len(tool_paths.image_paths),
        'img_id': img_id,
        'img_name': img_name,
        'config': CONFIG
    }
    return render_template("pencil.html", data=data)


@app.route('/hub-action/')
def hub():
    img_name = request.args.get('imgfile', '')
    # print(img_name)
    if img_name == '':
        return jsonify({"out": "no-file", "err": ""})
    else:
        commit_with_message(tool_paths.local_repo_path, img_name)

        return jsonify('\n\n', {"out": 'OK', "err": ''})


@Gooey(
    program_name="Tool for Comma10k",
    optional_cols=2,
)
def main():
    parser = GooeyParser(
        description="Utilities and Servers for contributing to the Comma10k dataset. Please read the README!",
    )

    # Assume this is likely to be checked out in a user's Document folder.
    default_git_repo_location = Path.home() / "Documents" / "comma10k"

    subparsers = parser.add_subparsers(help='commands', dest='command', required=True)

    server_parser = subparsers.add_parser(
        'server',
        prog="Run Editor Server",
    )

    server_parser.add_argument(
        '--comma10k_dir',
        default=str(default_git_repo_location),
        metavar="Local Clone of your Comma10k Fork Git Repository Path",
        widget="DirChooser",
        help="The Editor Server will operate on this repository",
        required=False,
    )

    fetch_reset_parser = subparsers.add_parser(
        'fetch_reset',
        prog='Reset Current to Upstream',
    )

    fetch_reset_parser.add_argument(
        '--comma10k_dir',
        default=str(default_git_repo_location),
        metavar="Local Clone of your Comma10k Fork Git Repository Path",
        widget="DirChooser",
        help="The tool will create (and overwrite if needed) and checkout a branch called 'wip' that has the latest "
             "changes from comma.ai's comma10k repo.",
        required=False,
    )

    create_push_parser = subparsers.add_parser(
        'create_push',
        prog="Create and Push Branch"
    )

    create_push_parser.add_argument(
        '--comma10k_dir',
        default=str(default_git_repo_location),
        metavar="Local Clone of your Comma10k Fork Git Repository Path",
        widget="DirChooser",
        help="The tool will create a new branch from the current branch with a unique name and push it to your GitHub "
             "fork. It will then give you a link to submit a pull request to comma.ai to the new branch.",
        required=False,
    )

    args = parser.parse_args()

    tool_paths.local_repo_path = Path(args.comma10k_dir)
    tool_paths.image_paths = sorted(tool_paths.local_repo_path.glob('imgs/*.png'))

    if args.command == 'server':
        # Debug true causes Gooey to popup. Oh well.
        app.run(debug=False)
    elif args.command == 'fetch_reset':
        fetch_reset_new_branch_upstream(tool_paths.local_repo_path)
    elif args.command == 'create_push':
        create_push_pr_able_branch(tool_paths.local_repo_path)


if __name__ == "__main__":
    main()
