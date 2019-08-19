# bomber monkey

A Bomberman clone featuring monkeys and banana.

This was developped during a 3 days hackaton by the following Monkeys :
- Florent Le Gac
- Nicolas Lalevée
- Logan Mauzaize 

## run

    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
    export PYTHONPATH=$PWD
    cd bomber_monkey
    python3 app.py


### MacOS


PyGame 1 is relying on the lib SDL1, which runs very slow on retina screens.

Two workarounds available:

- install PyGame2 which uses SDL2: `pip install pygame==2.0.0.dev3`
- follow the instructions there: https://stackoverflow.com/a/47585242/974474
