# Astro Tonight?

## Why

I keep missing opportunities for astrophotography so I made a script that can take data from the clearoutside.com image

Mostly as a learning exercise

## How to use

1. Pull the repository
    
    `git pull https://github.com/doghousedean/astro-tonight.git`
2. Create the virtual environment

    `python -m venv venv`

3. Activate your environment (This is the linux/macos version, windows is weird)

    `source venv/bin/activate`
4. Install requirements

    `pip install -r requirements.txt`

5. Create a `.env` file with your Lattitude and Longitude, you can edit and save `.env-sample` if you want

```bash
LAT=53.0
LON=-2.4
```

6. Run the tool

    `python astro-tonight.py`

## Example output

### When we should stay on the sofa

```bash
$ python astro-tonight.py                        
No luck, best get browsing firstlightoptics.com
$
```

### When the universe is being nice

```bash
$ python astro-tonight.py
Good conditions for astronomy this evening!
$
```
