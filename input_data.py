from fastai.vision.all import download_url
from pathlib import Path
import os
import numpy as np
import gzip
import torch
import argparse


# Parse input arguments
def get_input() -> argparse.Namespace:

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", type=str,
                        help="Path to download data to", 
                        required=True)
    parser.add_argument("--learning_rates", "-lr", 
                        nargs="+",
                        type=float,
                        help="An arbitrary number of learning rates to use in model training",
                        required=True)
    parser.add_argument("--gamma", "-g", 
                        nargs="+",
                        type=float,
                        help="An arbitrary number of gammas (learning rate decay) to use in model training. Defaults to 0.1. Add 1 for no gamma at all.",
                        required=False)
    parser.add_argument("--batch_size", "-bs", 
                        nargs="+",
                        type=int,
                        help="An arbitrary number of batch sizes to use in model training. Defaults to 64.",
                        required=False)
    parser.add_argument("--epochs", "-e", 
                        nargs="+",
                        type=int,
                        help="An arbitrary number of epoch limits to train for for each hyperparameter combination.",
                        required=True)
    parser.add_argument("--shuffle", "-s", 
                        nargs="+",
                        type=bool,
                        help="Add one of three options: True, False or True False. Specifies whether the dataset will be shuffled during training. Defaults to True",
                        required=False)
    parser.add_argument("--find_lr", "-f",
                        type=bool,
                        help="True/False - whether to use fastai's learning rate finder to find optimal learning rate. If True, you shouldn't pass your own learning rates.",
                        required=False
                        )
    args = parser.parse_args()
    print(args.learning_rates)
    return args

# Download mnist data from url to dir_name
def download_mnist(dir_name:str) -> None:
    train_imgs_url = "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-images-idx3-ubyte.gz"
    train_labels_url = "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-labels-idx1-ubyte.gz"
    test_imgs_url = "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-images-idx3-ubyte.gz"
    test_labels_url = "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-labels-idx1-ubyte.gz"
    
    dir_name = Path(dir_name)
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    for (url, name) in [(train_imgs_url, "train_images.gz"),
                    (train_labels_url, "train_labels.gz"),
                    (test_imgs_url, "test_images.gz"),
                    (test_labels_url, "test_labels.gz")]:
        download_url(url, dir_name/name)

# Load mnist data from path
def load_mnist(path:str, kind:str="train") -> (torch.Tensor, torch.Tensor):
    
    labels_path = os.path.join(path,
                               "%s_labels.gz"
                               % kind)
    images_path = os.path.join(path,
                               "%s_images.gz"
                               % kind)

    with gzip.open(labels_path, "rb") as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8,
                               offset=8)

    with gzip.open(images_path, "rb") as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8,
                               offset=16).reshape(len(labels), 1, 28, 28)

    return (torch.from_numpy(images).float(), torch.from_numpy(labels).long())

get_input()