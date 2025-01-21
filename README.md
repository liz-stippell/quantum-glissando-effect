# The Quantum Glissando Effect

To use the Notebook:
1. Download this repository to your computer. This can be achieved in two main ways:
  - Click the green "<>Code" button and click "Download ZIP"
  - <b>(Preferred Method) For more advanced users:</b> Click the green "<>Code" button and copy the URL to the clipboard. Then, navigate to your terminal. In the terminal, navigate to where you would like this code to live. Type: <code>git clone https://github.com/liz-stippell/quantum-glissando-effect.git [folder name]</code> (replace folder name with where you want these files to live, do not include the brackets)
      -  To update your copies of the code:
      -  In the terminal, navigate to where you have "cloned" the repository. Enter the file directory.
      -  `git status` will show you if your copy is up to date with the repository, if you have different files, etc. It should read something like: `Your branch is up to date with 'origin/main'.`
      -  If it says your copy is behind `origin/main`, run `git pull origin main`. This will pull any new files into your cloned repository from the main branch.
2. Download [Anaconda](https://www.anaconda.com/download?utm_source=anacondadocs&utm_medium=documentation&utm_campaign=download&utm_content=installwindows)
3. Open Anaconda and launch <b>Jupyter Notebook</b>
4. Navigate to where these files are saved in the Jupyter Notebook interface
5. Open the notebook corresponding to your version of Jupyter Notebook (version 7.X.X or version 6.X.X)

## Necessary Packages
Packages can be installed directly through the Jupyter Notebook interface. Directions for this installation technique is found within the Notebooks themselves.

To install the packages through the terminal:
1. `pip install matplotlib`
2. `pip install numpy`
3. `pip install scipy`

If you are using Jupyter Notebook v7.0+ you must also install:
1. `pip install ipympl`
