[![Build Status](https://travis-ci.com/Saxamos/car-detector.svg?branch=master)](https://travis-ci.com/Saxamos/car-detector)

# car-detector

This is a drawing detection application for raspberry-pi. It detects if a drawing is a car or not. There are two modes of
running:
- take a picture of your drawing
- draw directly on the tactile screen of the raspberry


### Install the app

Install the app in your virtual env. At the root of the project, run:
```
pip install -e .
```

### Run the tests
```
TODO
```

### Launch the app

Run the folllowing command to load the app with camera:
```
car_detector camera
```

With clicking mouse drawing and optionnal arguments:
```
car_detector draw --model <path/to/model> --saved <path/to/save/image>
```

### Related article

[Article 1: train your model](https://blog.octo.com/ia-embarquee-deployer-du-deep-learning-sur-un-raspberry/)

[Article 2: deploy it on a raspberry](https://blog.octo.com/lia-embarquee-entrainer-deployer-et-utiliser-du-deep-learning-sur-un-raspberry-partie-2/)

[Article 3: use the model and enhance it](https://blog.octo.com/lia-embarquee-entrainer-deployer-et-utiliser-du-deep-learning-sur-un-raspberry-partie-3/)
