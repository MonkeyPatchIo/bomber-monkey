[![Bomber Monkey Trailer](http://img.youtube.com/vi/zaJuPzcj4a0/0.jpg)](https://youtu.be/zaJuPzcj4a0 "Bomber Monkey Trailer")

We like coding, we like playing, we like learning.

From a 3 days hackaton, 3 Monkeys with diverse expertises such as data engineering, devops and web backend,
figured out how to code a game from scratch.

## How to run the game

Install dependencies

    python3 -m venv venv
    . venv/bin/activate
    python3 -m pip install -r requirements.txt

Launch the game

    . venv/bin/activate
    export PYTHONPATH=$PWD
    cd bomber_monkey
    python3 app.py

## Controls

There are two keyboard mappings:
- one can use the arrows to move and the RETURN key to drop a bomb
- the other can move with the ZQSD keys and use the SPACE bar to drop a bomb

Joysticks are also supported. To drop a bomb, use the "first" button of the joystick.

Quit and/or pause can be triggered with the ESC key on the keyboard, or with the "second" button of the joystick.
