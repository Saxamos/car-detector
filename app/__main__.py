import logging
import os

import click
from keras.models import load_model

from app import ROOT_PATH
from app.parent_frame import ParentFrame


@click.command()
@click.argument('mode', click.Choice({'draw', 'camera'}))
@click.option('--model', '-m', type=click.Path(exists=True), default=os.path.join(ROOT_PATH, 'model', 'model.h5'),
              help='Model path')
@click.option('--saved', '-s', type=click.Path(exists=True), default=os.path.join(ROOT_PATH, 'data', 'picture'),
              help='Folder to save images')
@click.option('--viz_activation', '-v', type=click.BOOL, default=False)
def car_detector(mode, model, saved, viz_activation):
    logging.info(f'Loading {model} model')
    model_instance = load_model(model)
    app = ParentFrame(mode, model_instance, saved, viz_activation)
    app.mainloop()


car_detector()
