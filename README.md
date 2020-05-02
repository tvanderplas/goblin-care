# Goblin Care

A game about goblins and cars

### Prerequisites

This game depends on Python 3.7, although it may also work with some older versions. Currently only works on Windows. 

### Installing

Clone the repository

```
git clone https://github.com/tvanderplas/goblin-care.git
```

Create a Python 3.7 virtual environment

```
cd goblin-care
python -m venv env
```

Activate the environment

```
env\Scripts\activate
```

Install dependencies

```
pip install -r requirements.txt
```

Run `goblin care.py`

## Built With

* [pyinstaller](https://pypi.org/project/PyInstaller/) - Bundles the game and all its dependencies into a single package
* [pygame](https://www.pygame.org) - For OpenGL context, event handling and game loop
* [PyOpenGL](https://pypi.org/project/PyOpenGL/) - OpenGL bindings for Python

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see [releases](https://github.com/tvanderplas/goblin-care/releases). 

## Authors

* **Tim Vanderplas** - *Initial work* - [tvanderplas](https://github.com/tvanderplas)
