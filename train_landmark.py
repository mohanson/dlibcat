import dlib

options = dlib.shape_predictor_training_options()
options.oversampling_amount = 300
options.nu = 0.05
options.tree_depth = 2
options.be_verbose = True

dlib.train_shape_predictor('train_landmark.xml', 'predictor.dat', options)

print("\nTraining accuracy: {}".format(dlib.test_shape_predictor('train_landmark.xml', 'predictor.dat')))
