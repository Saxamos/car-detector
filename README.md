[![Build Status](https://travis-ci.com/Saxamos/car-detector.svg?branch=master)](https://travis-ci.com/Saxamos/car-detector)

# car-detector

This is a drawing detection application for raspberry-pi. It detects if a drawing is a car or not. There are two modes of
running:
- take a picture of your drawing
- draw directly on the tactile screen of the raspberry


### Install the app

Create a python3 venv and all the required packages and the app in your virtual env.
At the root of the project, run:
```
python3 -m venv venv
pip install -r requirements
pip install -e .
```

### Run the tests
```
pytest
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

### Train a model

The modelisation notebook can be found at the root of the project. The data comes from the google quick draw application.
Usefull command for port forwarding (if you use ec2 instance):
```bash
ssh -L <local:port>:localhost:<distant:port> <user>@<ip-adress>
# example to forward tensorboard:
ssh -L 8881:localhost:6006 ubuntu@34.240.13.93

```

### Related article

[Article 1: train your model](https://blog.octo.com/ia-embarquee-deployer-du-deep-learning-sur-un-raspberry/)

[Article 2: deploy it on a raspberry](https://blog.octo.com/lia-embarquee-entrainer-deployer-et-utiliser-du-deep-learning-sur-un-raspberry-partie-2/)

[Article 3: use the model and enhance it](https://blog.octo.com/lia-embarquee-entrainer-deployer-et-utiliser-du-deep-learning-sur-un-raspberry-partie-3/)

### Schemes

#### Hardware issues on ARM

![ARMaggedon](assets/x86_vs_arm.png)

#### Use Ansible to configure Raspbian on QEMU

![Hans Ziebel](assets/ansible.png)

#### Pipeline overview

![Pipeline](assets/qemu_pipeline.png)
