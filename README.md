# Tool for [Comma10k][comma10k]

This is the annotation tool extracted out of the [comma10k][comma10k] repository for annotating images.

The following major changes have been added:

* Wrapped in a Gooey Wrapper. This can be disabled by adding the `--ignore-gooey` argument.
* Parameterized the comma10k Git repo location. This is by default "Documents/comma10k" 
  and can be changed in the GUI/Arguments.
* Compiled with PyInstaller for Windows so users don't have to setup a Python development 
  environment to run the tool.
* "Save to Disk" button to save the mask changes right to the file location of the local comma10k repo.
* Added functionality in launcher to create and reset a `wip` branch to the latest `master` branch on Comma.ai's repo.
* Added functionality in launcher to generate a branch, push, and be linked a URL to submit a pull request on the current branch.

## Usage

This is a bit Windows-centric for now.

### Annotation

1. Download a release ZIP from https://github.com/nelsonjchen/tool4comma10k/releases and extract.
2. Run `Tool4Comma10k.exe` in folder.
3. Choose a locally cloned `comma10k` Git Repo.
4. Visit http://localhost:5000 .
5. LOOP
    1. TODO: fetch upstream and reset to upstream/master 
    2. Load existing mask image.
    3. Fix annotation
    4. Press Save to Disk
    5. TODO: Press Checkout new Branch and Commit and Push
    6. TODO: Automate? Visit GitHub to make Pull request to comma repo

## Attribution

* https://github.com/nuwandavek/commapencil
    * Developed most of the tool. Assuming MIT license per pull request to Comma10k and GitHub TOS. 
* https://github.com/comma10k/comma10k
    * George tweaked it a bit.

[comma10k]: https://github.com/commaai/comma10k

