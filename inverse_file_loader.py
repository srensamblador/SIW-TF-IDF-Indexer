from inverse_file import InverseFile
import serializer
import argparse


def main(args):
    inverse_file = serializer.load_inverse_file(args.file)
    print(inverse_file)  # Shows the inverse_file on console


def parse_args():
    parser = argparse.ArgumentParser(description="Loads inverse_file from disk")
    parser.add_argument("file", help="file contained the index")
    args = parser.parse_args()
    return args


main(parse_args())
