# Tool for [Comma10k][comma10k]

![image](https://user-images.githubusercontent.com/5363/76159582-14b71780-60d7-11ea-86de-9c72bcc5951e.png)

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
* Majorly replaced path-drawing stuff with [PxBrush][pxbrush]. 
  This allows drawing without anti-aliasing which is needed.

## Usage

This is a bit Windows-centric for now.

### Annotation

1. Download a release ZIP from https://github.com/nelsonjchen/tool4comma10k/releases and extract.
2. Run `Tool4Comma10k.exe` in folder.
3. `git clone` your **fork** of the `comma10k` git repo to your Documents folder. 
    By default, the tool will assume you've cloned it to
    your Documents folder but this can be changed on every run, though not persistently.     
5. Workflow Loop
    1. Run `Reset Current To Upstream`
    2. Run `Run Editor Server`
        * This will run forever until stopped
    3. Visit http://localhost:5000     
    4. Work Work Work for each image number in question.    
        1. Press Save to Disk
        1. And then press Commit in the bottom right when mask is good.
    5. Stop Server in GUI
    6. Once ready to submit your batch of changes, Run `Create and Push Branch`
    7. Click the URL to fill out and make your pull request.

## Attribution

* https://github.com/nuwandavek/commapencil
    * Developed most of the tool. Assuming MIT license per pull request to Comma10k and GitHub TOS. 
* https://github.com/comma10k/comma10k
    * George tweaked it a bit.
* https://github.com/kozo002/px-brush
    * Wrote a guide on drawing on canvas without anti-aliasing. And the library. 

[comma10k]: https://github.com/commaai/comma10k
[pxbrush]: https://github.com/kozo002/px-brush
