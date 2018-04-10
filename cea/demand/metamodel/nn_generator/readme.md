The following text is a guide for running the surrogate model.

Prerequisites:
To run the neural network you will need a minimum of 1GB of hard disk space per each building of your district.
The surrogate model creates samples of the entire district simultaneously, therefore, you should anticipate
the availability of hard disk space on your drive C (or what ever drive the case study is located).

The packages required for running the surrogate model is as follows, to install all packages, open the anaconda
terminal and follow these step one by one. Make sure that you don't skip any steps (even though they may be
optional), as it may tamper with the multi processing and the compatibility of the libraries.

(a) activate the cea environment, do:
    activate cea

(b) install scikit learn if not already installed, do:
    conda install scikit-learn

(c) install the requirements packages, if not already installed, do:
    conda install numpy scipy mkl-service libpython m2w64-toolchain nose sphinx pydot-ng git

(d) install theano and pygpu(for future implementation), do:
    conda install theano pygpu

(e) install keras, do:
    conda install -c conda-forge keras

NOTE:
The radiation file should be already generated, therefore, if not already done, navigate to the following folder:
    ...cea\resources\radiation_daysim
and run the following script:
    radiation_main.py

To run, do:
1. check the nn_settings.py file
2. run the scalar_sampler.py
3. run scaler_fit.py

4. Now there are two posibilities for starting the training:
    4.1. the first is to generate x number of samples (100 in this example)
    and then train the network (these samples will be constant in all epochs):
        - run nn_pretrainer_pipeline.py
    4.2. the second is to randomly generate a smaller number of samples (max 10)
    and train the NN (these 10 samples will be updated in each epoch):
        - run nn_random_pipeline.py

5. Now there are two possibilities for continuing the training from step 4:
    5.1. continue training similar to that of 4.1.:
        - run nn_pretrainer_continue.py
    5.2. continue training similar to that of 4.2.:
        - run nn_trainer_continue.py

6. Evaluate the network (test the perforamnce based on a random sample)
    6.1. you can evaluate based on a random sample:
        - run nn_trainer_evaluate.py
    6.2 you can estimate the outputs based on the current inputs of CEA:
        - run nn-trainer_estimate.py

