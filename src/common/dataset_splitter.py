from glob import glob
import argparse
import random
import pandas as pd
import json

parser = argparse.ArgumentParser()
parser.add_argument("root_dir")
parser.add_argument(
    "-s, --separators", dest="separators", default=["/", "-"], type=str, nargs="+"
)
parser.add_argument("-f, --fields", dest="fields", default=[-1, 0], type=int, nargs="+")
parser.add_argument("--extension", default="wav")
parser.add_argument("--ratio", type=float, default=0.1)
parser.add_argument("--classes_stats", action="store_true")
parser.add_argument("--output_labels", action="store_true")
parser.add_argument("--no_output", action="store_true")
parser.add_argument("--no_remove_root", action="store_true")

parser.add_argument("--dataset_conf", default="datasets/config/librispeech.json")
parser.add_argument("--label", default="libri_speaker")
parser.add_argument("--samples_per_labels", action="store_true")
parser.add_argument("--train_size", type=int, default=10)
parser.add_argument("--valid_size", type=int, default=10)
parser.add_argument("--test_size", type=int, default=10)
parser.add_argument("--exclude_labels", default=None, type=str, nargs="+")
parser.add_argument("--num_labels", type=int, default=None)
parser.add_argument("--debugging_data", type=int, default=None)


args = parser.parse_args()

assert len(args.separators) == len(args.fields)

random.seed(30)

def label_tree(files):

    label_tree = {}
    for file in files:
        file_name = file if args.no_remove_root else file[len(args.root_dir) + 1 :]
        label_name = file_name
        for separator, field in zip(args.separators, args.fields):
            # import pdb; pdb.set_trace()
            label_name = label_name.split(separator)[field]
        if label_name not in label_tree:
            label_tree[label_name] = [file_name]
        else:
            label_tree[label_name].append(file_name)
    return label_tree


def train_test_valid_split(label_tree, ratio=args.ratio):
    valid = []
    test = []
    train = []
    for label_name in label_tree:
        random.shuffle(label_tree[label_name])
        label_size = len(label_tree[label_name])
        if args.classes_stats:
            print(label_name, label_size)
        
        valid += label_tree[label_name][: int(ratio * label_size)]
        test += label_tree[label_name][
            int(args.ratio * label_size) : int(2 * ratio * label_size)
        ]
        train += label_tree[label_name][int(2 * ratio * label_size) :]

    print("valid: {}, test: {}, train: {}".format(len(valid), len(test), len(train)))

    save_split(train, test, valid, label_tree)

    return train, test, valid


def samples_per_labels_split(label_tree, train_size=10, test_size=10, valid_size=10):
    valid = []
    test = []
    train = []
    for label_name in label_tree:
        random.shuffle(label_tree[label_name])
        label_size = len(label_tree[label_name])

        train += label_tree[label_name][:train_size]
        test += label_tree[label_name][train_size : train_size + test_size]
        valid += label_tree[label_name][
            train_size + test_size : train_size + test_size + valid_size
        ]

    print("valid: {}, test: {}, train: {}".format(len(valid), len(test), len(train)))

    save_split(train, test, valid, label_tree)

    return train, test, valid


def exclude_labels(label_tree, labels=None):
    if labels is not None:
        assert type(labels) == list, "'labels' not list"
        label_tree = {
            label: label_tree[label] for label in label_tree if label not in labels
        }
    return label_tree


def select_n_labels(label_tree, num_labels=None):
    if num_labels is not None:
        label_tree = {
            label: label_tree[label] for label in list(label_tree)[:num_labels]
        }
    return label_tree


def save_split(train, test, valid, label_tree, root_dir=args.root_dir):

    print("datasets saving to {}...".format(root_dir))

    if args.debugging_data is not None:
        with open(root_dir + "/test_debugging.csv", "w") as f:
            for file in test:
                f.write("{}\n".format(file))

        with open(root_dir + "/valid_debugging.csv", "w") as f:
            for file in valid:
                f.write("{}\n".format(file))

        with open(root_dir + "/train_debugging.csv", "w") as f:
            for file in train:
                f.write("{}\n".format(file))

        with open(root_dir + "/labels_debugging.csv", "w") as f:
            for label_name in label_tree:
                f.write("{}\n".format(label_name))
    else:
        with open(root_dir + "/test.csv", "w") as f:
            for file in test:
                f.write("{}\n".format(file))

        with open(root_dir + "/valid.csv", "w") as f:
            for file in valid:
                f.write("{}\n".format(file))

        with open(root_dir + "/train.csv", "w") as f:
            for file in train:
                f.write("{}\n".format(file))

        with open(root_dir + "/labels.csv", "w") as f:
            for label_name in label_tree:
                f.write("{}\n".format(label_name))


def update_config(jsonFile, nb_classes, train, test, valid):
    with open(jsonFile, "r+") as j:
        config = json.load(j)
        config["labels"][args.label]["nb_classes"] = nb_classes
        config["data"]["train"]["size"] = len(train)
        config["data"]["test"]["size"] = len(test)
        config["data"]["valid"]["size"] = len(valid)
        config["labels"][args.label]["map"] = args.root_dir + "/labels.csv"
        config["data"]["train"]["list"] = "train.csv"
        config["data"]["test"]["list"] = "test.csv"
        config["data"]["valid"]["list"] = "valid.csv"

        if args.debugging_data is not None:
            config["labels"][args.label]["map"] = (
                args.root_dir + "/labels_debugging.csv"
            )
            config["data"]["train"]["list"] = "train_debugging.csv"
            config["data"]["test"]["list"] = "test_debugging.csv"
            config["data"]["valid"]["list"] = "valid_debugging.csv"
        j.seek(0)
        json.dump(config, j, indent=4)
        j.truncate()


if __name__ == "__main__":
    files = glob("{}/**/*.{}".format(args.root_dir, args.extension), recursive=True)

    label_dict = label_tree(files)

    if args.exclude_labels is not None:
        label_dict = exclude_labels(label_dict, labels=args.exclude_labels)

    if args.num_labels is not None:
        label_dict = select_n_labels(label_dict, num_labels=args.num_labels)

    if args.debugging_data is not None:
        train, test, valid = samples_per_labels_split(
            label_dict,
            train_size=args.debugging_data,
            test_size=args.debugging_data,
            valid_size=args.debugging_data,
        )
    elif args.samples_per_labels:
        train, test, valid = samples_per_labels_split(
            label_dict,
            train_size=args.train_size,
            test_size=args.test_size,
            valid_size=args.valid_size,
        )
    else:
        train, test, valid = train_test_valid_split(label_dict)

    # update config file
    update_config(args.dataset_conf, len(label_dict.keys()), train, test, valid)
    print("done splitting.")
