# TruCol Market Analysis [![Build Status](https://travis-ci.com/a-t-0/Code-LatexReportTemplate.svg?branch=main)](https://travis-ci.com/a-t-0/Code-LatexReportTemplate)

Hi, this is a our preliminary parameterised market analysis for the TruCol company. By sharing our model we hope to be able to provide more insight in our analysis and to improve its accuracy based on the provided feedback. This repository enables you to automatically updates your pdf report every time you run your code. It also syncs with Overleaf so you can do your typing there if you wish.

Our latest presentation of our market analysis (pdf) is visible [here](https://github.com/TruCol/Market_analysis/blob/main/latex/project1/main.pdf) (refresh page once).

## Usage: do once

Download/clone this repository.

0. If you don't have pip: open Anaconda prompt and browse to the directory of this readme:

```
cd /home/<your path to the repository folder>/
```

1. To use this package, first make a new conda environment and activate (it this automatically installs everything you need)

```
conda env create --file environment.yml
```

## Usage: do every time you start Anaconda:

3. Activate the conda environment you created:

```
conda activate market_analysis
```

## Usage: do every run:

3. Performe a run for assignment 1 (named project1) of main code (in `main.py`, called from `__main__.py`)

```
python -m code.project1.src
```

## Testing

4. Testing is as simple as running the following command in the root directory of this repository in Anaconda prompt:

```
python -m pytest
```

from the root directory of this project.

<!-- Un-wrapped URL's below (Mostly for Badges) -->
