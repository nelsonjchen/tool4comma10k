import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from git import Repo


def fetch_reset_new_branch_upstream(repo_path: Path):
    repo = Repo(repo_path)
    # Force upstream to be comma10k repo
    if 'upstream' not in repo.remotes:
        repo.create_remote('upstream', 'https://github.com/commaai/comma10k')
    # Fetch it
    repo.remotes['upstream'].fetch()
    # Delete existing wip branch, if any
    if repo.active_branch.name == 'wip':
        # Set wip --hard to upstream/master
        repo.git.reset('--hard', 'upstream/master')
    else:
        head = repo.create_head('wip', 'upstream/master', force=True)
        head.checkout(force=True)


def create_push_pr_able_branch(repo_path: Path):
    repo = Repo(repo_path)
    # Generate a branch name, just use the date for now?
    time_string = datetime.now().strftime("%Y%m%d%H%M%S")
    branch_name = f"masks_{time_string}"
    mask_branch = repo.create_head(branch_name, force=True)
    mask_branch.checkout()
    origin_remote = repo.remotes['origin']
    repo.git.push("--set-upstream", origin_remote, repo.head.ref, force=True)
    github_user = urlparse(repo.remotes['origin'].url).path.split('/')[1]
    pull_request_url = \
        f"https://github.com/commaai/comma10k/compare/master...{github_user}:{branch_name}?expand=1"
    print(f"Create Pull Request URL: {pull_request_url}")
    return pull_request_url


def commit_with_message(repo_path: Path, img_name: str):
    repo = Repo(repo_path)
    masked_name = f"masks/{img_name}"
    changed_files = [item.a_path for item in repo.index.diff(None)]
    if masked_name not in changed_files:
        return
    mask_number = re.search(r'masks/(\d+)_', masked_name)[1]
    commit_message = f"{mask_number} - Update Mask"
    repo.git.commit('--all', '-m', commit_message)


# Test Only
if __name__ == "__main__":
    default_git_repo_location = Path.home() / "Documents" / "comma10k"
    if sys.argv[1] == "create_push":
        create_push_pr_able_branch(default_git_repo_location)
    elif sys.argv[1] == "fetch_reset":
        fetch_reset_new_branch_upstream(default_git_repo_location)
    elif sys.argv[1] == "commit_with_message":
        commit_with_message(default_git_repo_location,
                            '0012_76c3bc6da8109da7_2018-09-01--13-03-11_31_1101.png')
