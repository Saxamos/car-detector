import logging
import os

import click
from keras.models import load_model

from app import ROOT_PATH
from app.parent_frame import ParentFrame

logging.getLogger('tensorflow').setLevel(logging.ERROR)

logging.basicConfig(level=logging.INFO)


@click.command()
@click.argument('mode', click.Choice({'draw', 'camera'}))
@click.option('--model', '-m', type=click.Path(exists=True), default=os.path.join(ROOT_PATH, 'model', 'model.h5'),
              help='Model path')
@click.option('--saved', '-s', type=click.Path(exists=True), default=os.path.join(ROOT_PATH, 'data', 'picture'),
              help='Folder to save images')
@click.option('--viz-activation', '-va', is_flag=True, type=click.BOOL, default=False)
@click.option('--viz-entropy', '-ve', is_flag=True, type=click.BOOL, default=False)
def car_detector(mode, model, saved, viz_activation, viz_entropy):
    logging.info(f'Loading {model} model')
    model_instance = load_model(model)
    app = ParentFrame(mode, model_instance, saved, viz_activation, viz_entropy)
    app.mainloop()


car_detector()
