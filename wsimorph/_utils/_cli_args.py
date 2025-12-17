from argparse import ArgumentParser, Namespace
from pathlib import Path


def get_cli_args() -> Namespace:
    parser = ArgumentParser(description="Morphologically Profile a WSI")
    wsi_group = parser.add_argument_group("WSI Options")
    wsi_group.add_argument(
        "-i", "--input", required=True, help="Path to the input WSI file.", type=str
    )
    pipeline_group = parser.add_argument_group("Pipeline Options")
    pipeline_group.add_argument(
        "-c", "--config", required=True, help="Path to the config file.", type=str
    )
    args = parser.parse_args()
    if not Path(args.input).exists():
        raise FileNotFoundError(f"Input file does not exist.")
    if not Path(args.config).exists():
        raise FileNotFoundError(f"Config file does not exist.")
    return args
