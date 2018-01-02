import dlib

options = dlib.simple_object_detector_training_options()
options.add_left_right_image_flips = True
options.C = 5
options.num_threads = 4
options.be_verbose = True

dlib.train_simple_object_detector('train.xml', "detector.svm", options)

print("\nTraining accuracy: {}".format(dlib.test_simple_object_detector('train.xml', 'detector.svm')))
