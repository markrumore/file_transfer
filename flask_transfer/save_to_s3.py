import argparse
import spacy

from scripts import utils

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='script to save a spacy model to s3'
    )

    parser.add_argument(
        '-p', '--model_path',
        help='local path to model to be saved',
    )

    parser.add_argument(
        '-n', '--model_name',
        help='name of model to be used as key in s3',
    )

    parser.add_argument(
        '-d', '--model_dir',
        help='S3 directory to save model in',
        default=utils.DEFAULT_S3_PROD_MODEL_DIR
    )

    args = parser.parse_args()

    nlp = spacy.load(args.model_path)

    output = utils.save_to_s3(nlp, args.model_name, s3_model_dir=args.model_dir)

    print(output)
