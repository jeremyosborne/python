# machine learning notes

Chronological steps so far (as I remember to write them down). Not necessarily the order one should do them in.

* Watch videos on [3Blue1Brown Youtube Channel](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw):
    * [Neural Networks](https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)
    * [Essence of Linear Algebra](https://www.youtube.com/watch?v=kjBOesZCoqc&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)

* Update python (on mac, using [homebrew](https://brew.sh/))

```bash
brew doctor
brew update
brew install python ruby  # gets python3 and an updated ruby
```

* Discover [pipenv](https://docs.pipenv.org/) (and rejoice):

```bash
brew install pipenv

# very npm like, one command to manage pip and virtualenv, and seems to do the right thing
# most of the time. `pipenv install [packages]` + `pipenv shell`
```

* Update [atom](https://atom.io):

```bash
apm install platformio-ide-terminal
```

* Pick [scikit-learn](http://scikit-learn.org/) to start messing around with.
* [Figure out what I think I need to install from docs](http://scikit-learn.org/stable/install.html) and give it a try with `pipenv`:

```bash
# cd to my src dump directory
# I forget how soon after I installed the others beyond scikit-learn, but these were all installed
pipenv install numpy scipy scikit-learn matplotlib pandas jupyter

# Note: ran into a long dependency building issue that seems to be known with pipenv but doesn't happen to everyone.
# I let the first install run for awhile, and since then updating deps hasn't been a problem. It eventually
# did complete and didn't hang forever.
```

* [Copy, paste, talk to myself a lot, read out loud, and try out the quick start. Yep it works.](http://scikit-learn.org/stable/tutorial/basic/tutorial.html)

* Digression: Pandas DataFrames.
    * [Pandas Tutorial: DataFrames in Python](https://www.datacamp.com/community/tutorials/pandas-tutorial-dataframe-python)
    * [10 Minutes to pandas](https://pandas.pydata.org/pandas-docs/stable/10min.html)

* Digression: Jupyter + IPython:
    * [Jupyter Notebook Tutorial: The Definitive Guide](https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook)
    * [Jupyter + IPython docs](http://ipython.readthedocs.io/en/stable/interactive/index.html)
    * [Interactive Dashboards](https://blog.dominodatalab.com/interactive-dashboards-in-jupyter/)
    * [Jupyter widgets](http://ipywidgets.readthedocs.io/)


