
import json
import os.path
from argparse import ArgumentParser, _ArgumentGroup
from typing import Sequence, Union
from gooey_tools import add_hybrid_arg

CFG_FILE = "config.cfg"
UPDIR = os.path.dirname(os.getcwd())

def _open_cfg_safe(cfg_file):
    try:
        with open(cfg_file) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def init_config_parser(
        config_parser: ArgumentParser,
        cfg_file: str = CFG_FILE,
        defaults: dict = dict(),
    ) -> None:

    cfg = _open_cfg_safe(cfg_file)

    lang = defaults.get("LANGUAGE", cfg_file.split('.')[0])
    config_parser.add_argument(
        "--LANGUAGE",
        metavar="Language configuration:",
        default=lang
    )

    add_hybrid_arg(
        config_parser,
        "--CFG_FILE",
        metavar="Path to save config to:",
        default=cfg_file,
        type='filepath'
    )

    init_eafl_parser(config_parser, cfg)
    init_csv_parser(config_parser, cfg)
    init_html_parser(config_parser, cfg)

def init_html_parser(config_parser, cfg):
    if type(cfg) is str:
        cfg = _open_cfg_safe(cfg)
    html = config_parser.add_argument_group(
        'HTML',
        'Args for building HTML file for website.'
    )
    html_cfg = cfg.get('HTML', dict())
    init_meta = html_cfg.get("META", os.path.join(UPDIR, "metadata.csv"))
    init_wav = html_cfg.get("WAV", os.path.join(UPDIR, "wav"))
    init_www = html_cfg.get("WWW", os.path.join(UPDIR, "www"))

    nav_bar = """<div align="right">
        <a href="index.html">Corpus</a>
        - <a href="dict.xhtml">Dictionary</a>
        </div>"""
    nav_bar = html_cfg.get("NAV_BAR", nav_bar)

    add_hybrid_arg(
        config_parser,
        "--META",
        group=html,
        metavar="WAV Session Metadata (optional):",
        type='filepath',
        default=init_meta,
    )
    add_hybrid_arg(
        config_parser,
        "--WAV",
        group=html,
        metavar="WAV Input Directory:",
        type='dirpath',
        default=init_wav,
    )
    add_hybrid_arg(
        config_parser,
        "--WWW",
        group=html,
        metavar="Web Files Output Directory:",
        type='dirpath',
        default=init_www,
    )
    # init_clips = self.cfg.get("CLIPS", os.path.join(UPDIR, "audio", "www", "clips"))
    # self.mk_choice_row("CLIPS", init_clips, "WAV Clips Output Directory:", isdir=True)

    #self.mk_text_row("PG_TITLE", "Kwaras Corpus", "HTML Page Title:")
    html.add_argument(
        "--NAV_BAR",
        metavar="HTML div for Navigation",
        default=nav_bar,
    )

def init_eafl_parser(config_parser: ArgumentParser, cfg: Union[dict, str]) -> _ArgumentGroup:
    if type(cfg) is str:
        cfg = _open_cfg_safe(cfg)
    eafl = config_parser.add_argument_group(
        'EAFL',
        'Args for making EAFL file from LIFT file.'
        )
    eafl_cfg = cfg.get('EAFL', dict())
    add_hybrid_arg(
        config_parser,
        "--LIFT",
        group=eafl,
        metavar="Input LIFT file:",
        type='filepath',
        default=eafl_cfg.get("LIFT", os.path.join(UPDIR, "FLEx.lift")),
    )
    add_hybrid_arg(
        config_parser,
        "--EAFL_DIR",
        group=eafl,
        metavar="Output EAFL Directory:",
        type='dirpath',
        default=eafl_cfg.get("EAFL_DIR", UPDIR),
    )

def init_csv_parser(config_parser: ArgumentParser, cfg: Union[dict, str]) -> _ArgumentGroup:
    if type(cfg) is str:
        cfg = _open_cfg_safe(cfg)
    csv = config_parser.add_argument_group(
        'CSV',
        'Args for making datafile metadata.csv from ELAN annotations.'
    )
    old_eafs = os.path.join(UPDIR, "corpus-data-versions")
    out_dir = os.path.join(old_eafs, "auto")
    
    csv_cfg = cfg.get('CSV', dict())
    init_dir = csv_cfg.get("FILE_DIR", UPDIR)
    init_eafs = csv_cfg.get("OLD_EAFS", old_eafs)

    add_hybrid_arg(
        config_parser,
        "--FILE_DIR",
        group=csv,
        metavar="Working File Directory:",
        type='dirpath',
        default=init_dir,
    )
    if not os.path.exists(out_dir):
        out_dir = init_dir
    # init_csv = self.csv_cfg.get("CSV", os.path.join(out_dir, "data.csv"))
    # self.mk_choice_row("CSV", init_csv, "Output CSV File:", issave=True)

    exp_fields = csv_cfg.get("EXP_FIELDS",  # List of fields to include
                                ", ".join(["Phonetic", "Spanish", "English", "Note"]))
    csv.add_argument(
        "--EXP_FIELDS",
        default=exp_fields,
        help="List of Fields to Export",
        nargs='+'
    )

    add_hybrid_arg(
        config_parser,
        "--OLD_EAFS",
        group=csv,
        metavar="Directory of Input EAFs:",
        type='dirpath',
        default=init_eafs,
    )
    # self.mk_choice_row("NEW_EAFS", os.path.join(init_eafs, "auto"), "Directory for Output EAFs:", isdir=True)
    return csv