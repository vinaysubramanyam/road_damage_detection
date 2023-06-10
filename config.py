import torch
BATCH_SIZE = 8 # increase / decrease according to GPU memeory
RESIZE_TO = 416 # resize the image for training and transforms
NUM_EPOCHS = 10 # number of epochs to train for
NUM_WORKERS = 4
DEVICE = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
# training images and XML files directory
TRAIN_DIR = '/home/vinay/cs229/road_images_rcnn/train'
# validation images and XML files directory
VALID_DIR = '/home/vinay/cs229/road_images_rcnn/valid'
# classes: 0 index is reserved for background
CLASSES = ['__background__', 'D00', 'D01', 'D10', 'D11', 'D20', 'D40', 'D43', 'D44', 'D50', 'Repair', 'D0w0']

NUM_CLASSES = len(CLASSES)
# whether to visualize images after crearing the data loaders
VISUALIZE_TRANSFORMED_IMAGES = False
# location to save model and plots
OUT_DIR = 'outputs'