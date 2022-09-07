#!/usr/bin/env python3

from collections import OrderedDict
from threading import Thread
from copy import deepcopy
from typing import Optional, Union
import IPython
from traitlets.config import Config
from time import sleep

import webui

kwargs_txt2img = OrderedDict(
    prompt="",
    negative_prompt="",
    steps=20,
    sampler_index=0,
    use_GFPGAN=False,
    tiling=False,
    n_iter=9,
    batch_size=1,
    cfg_scale=10.0,
    seed=42,
    height=512,
    width=512,
)

job_queue = []


def process_jobs():
    while True:
        if job_queue:
            args = job_queue.pop(0)
            webui.modules.txt2img.txt2img(*args)
        else:
            sleep(1)


processing_thread = Thread(target=process_jobs)
processing_thread.start()


def set_or_return(property_name: str, property_value: Union[str, int, float, bool, None]
                  ) -> Union[str, int, float, bool, None]:
    if property_value is None:
        return kwargs_txt2img[property_name]
    kwargs_txt2img[property_name] = property_value
    return None


def prompt(new_value: Optional[str] = None) -> Optional[str]:
    return set_or_return("prompt", new_value)


def negative_prompt(new_value: Optional[str] = None) -> Optional[str]:
    return set_or_return("negative_prompt", new_value)


def steps(new_value: Optional[str] = None) -> Optional[str]:
    return set_or_return("steps", new_value)


def sampler_index(new_value: Optional[int] = None) -> Optional[str]:
    return set_or_return("sampler_index", new_value)


def use_GFPGAN(new_value: Optional[bool] = None) -> Optional[str]:
    return set_or_return("use_GFPGAN", new_value)


def tiling(new_value: Optional[bool] = None) -> Optional[str]:
    return set_or_return("tiling", new_value)


def n_iter(new_value: Optional[int] = None) -> Optional[int]:
    return set_or_return("n_iter", new_value)


def batch_size(new_value: Optional[int] = None) -> Optional[int]:
    return set_or_return("batch_size", new_value)


def cfg_scale(new_value: Optional[float] = None) -> Optional[float]:
    return set_or_return("cfg_scale", new_value)


def seed(new_value: Optional[int] = None) -> Optional[int]:
    return set_or_return("seed", new_value)


def height(new_value: Optional[int] = None) -> Optional[int]:
    return set_or_return("height", new_value)


def width(new_value: Optional[int] = None) -> Optional[int]:
    return set_or_return("width", new_value)


def queue(**temporary_kwargs) -> None:
    kwargs_copy = deepcopy(kwargs_txt2img)
    kwargs_copy.update(temporary_kwargs)
    args = list(kwargs_copy.values())
    args.append(0)
    job_queue.append(args)


def queue_prompt(prompt: str) -> None:
    queue(prompt=prompt)


p = prompt
q = queue
qp = queue_prompt
np = negative_prompt
st = steps
si = sampler_index
gfpgan = use_GFPGAN
ni = n_iter
bs = batch_size
cfg = cfg_scale
se = seed
h = height
w = width


ipython_config = Config()
ipython_config.InteractiveShell.autocall = 2
IPython.embed(config=ipython_config)
