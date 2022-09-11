#!/usr/bin/env python3

import sys
from collections import OrderedDict
from threading import Thread
from copy import deepcopy
from typing import Optional, Union
import IPython
from traitlets.config import Config
from time import sleep
import yaml

import webui

par = "par"
use = "use"
euler_a = "Euler a"
euler = "Euler"
lms = "LMS"
heun = "Heun"
dpm2 = "DPM2"
dpm2_a = "DPM2 a"
ddim = "DDIM"
plms = "PLMS"

kwargs_txt2img = OrderedDict(
    prompt="",
    negative_prompt="",
    prompt_style="None",
    steps=50,
    sampler_index=1,
    restore_faces=False,
    tiling=False,
    n_iter=9,
    batch_size=1,
    cfg_scale=10.0,
    seed=42,
    subseed=0,
    subseed_strength=0.0,
    seed_resize_from_h=0,
    seed_resize_from_w=0,
    height=512,
    width=512,
)

try:
    with open("/var/tmp/stable-diffusion-ipython-shell-info", encoding="ascii") as f:
        progress_print_path = f.readline()[:-1]
except FileNotFoundError:
    progress_print_path = None
    print("\nWarning: no separate terminal set for progress prints.", file=sys.stderr)

if progress_print_path is not None:
    progress_print_out = open(progress_print_path, "w", encoding="utf8")
    webui.shared.progress_print_out = progress_print_out

job_queue = []
shell_exited = False


def _process_jobs():
    while not shell_exited:
        if job_queue:
            args = job_queue.pop(0)
            func = webui.wrap_gradio_gpu_call(webui.modules.txt2img.txt2img)
            func(*args)
        else:
            sleep(1)


processing_thread = Thread(target=_process_jobs)
processing_thread.start()


def _set_or_return(property_name: str, property_value: Union[str, int, float, bool, None]
                  ) -> Union[str, int, float, bool, None]:
    if property_value is None:
        return kwargs_txt2img[property_name]
    kwargs_txt2img[property_name] = property_value
    return None


def prompt(new_value: Optional[str] = None) -> Optional[str]:
    """Return the prompt or set by providing a value."""
    return _set_or_return("prompt", new_value)


def negative_prompt(new_value: Optional[str] = None) -> Optional[str]:
    """Return the negative prompt or set by providing a value."""
    return _set_or_return("negative_prompt", new_value)


def prompt_style(new_value: Optional[str] = None) -> Optional[str]:
    """Return the prompt style or set by providing a value."""
    if new_value is not None and new_value not in webui.modules.shared.prompt_styles:
        raise ValueError(
            f"Unknown prompt style: {new_value}. "
            f"Available: {list(webui.modules.shared.prompt_styles.keys())}"
        )
    return _set_or_return("prompt_style", new_value)


def steps(new_value: Optional[int] = None) -> Optional[int]:
    """Return the number of steps or set by providing a value."""
    if new_value is not None:
        new_value = int(new_value)
    return _set_or_return("steps", new_value)


def _sampler_index_to_name(sampler_index: Optional[int]) -> Optional[str]:
    if sampler_index is None:
        return None
    try:
        return webui.modules.sd_samplers.samplers[sampler_index].name
    except IndexError:
        raise ValueError(f"Sampler index must be in [0, {len(webui.modules.sd_samplers)}]"
                         f"but received {sampler_index}")


def _sampler_name_to_index(sampler_name: Optional[str]) -> Optional[int]:
    if sampler_name is None:
        return None
    available_samplers = [sd.name for sd in webui.modules.sd_samplers.samplers]
    try:
        return list(map(lambda s: s.lower(), available_samplers)).index(sampler_name.lower())
    except ValueError:
        raise ValueError(f"Unknown sampler: {sampler_name}. Available: {available_samplers}")


def sampler_index(new_value: Optional[int] = None) -> Optional[int]:
    """Return the sampler index or set by providing a value."""
    if new_value is not None:
        new_value = int(new_value)
    _sampler_index_to_name(new_value)
    return _set_or_return("sampler_index", new_value)


def sampler_name(new_value: Optional[str] = None) -> Optional[str]:
    """Return the sampler name or set by providing a value."""
    return sampler_index(_sampler_name_to_index(new_value))


def restore_faces(new_value: Optional[bool] = None) -> Optional[bool]:
    """Return whether faces are fixed in post processing or set by providing a value."""
    return _set_or_return("restore_faces", new_value)


def tiling(new_value: Optional[bool] = None) -> Optional[bool]:
    """Return whether tiling images are generated or set by providing a value."""
    return _set_or_return("tiling", new_value)


def n_iter(new_value: Optional[int] = None) -> Optional[int]:
    """Return the number of iterations or set by providing a value."""
    if new_value is not None:
        new_value = int(new_value)
    return _set_or_return("n_iter", new_value)


def batch_size(new_value: Optional[int] = None) -> Optional[int]:
    """Return the batch size or set by providing a value."""
    if new_value is not None:
        new_value = int(new_value)
    return _set_or_return("batch_size", new_value)


def cfg_scale(new_value: Optional[float] = None) -> Optional[float]:
    """Return the CFG scale or set by providing a value."""
    return _set_or_return("cfg_scale", new_value)


def seed(new_value: Optional[int] = None) -> Optional[int]:
    """Return the seed or set by providing a value."""
    if new_value is not None:
        new_value = int(new_value)
    return _set_or_return("seed", new_value)


def subseed(new_value: Optional[int] = None) -> Optional[int]:
    """Return the subseed used for variation or set by providing a value."""
    if new_value is not None:
        new_value = int(new_value)
    return _set_or_return("subseed", new_value)


def subseed_strength(new_value: Optional[float] = None) -> Optional[float]:
    """Return the subseed strength used for variation or set by providing a value."""
    if new_value is not None:
        new_value = int(new_value)
    return _set_or_return("subseed_strength", new_value)


def seed_resize_from_h(new_value: Optional[int] = None) -> Optional[int]:
    """Return the height used for generating initial noise or set by providing a value."""
    if new_value is not None:
        new_value = int(new_value)
    return _set_or_return("seed_resize_from_h", new_value)


def seed_resize_from_w(new_value: Optional[int] = None) -> Optional[int]:
    """Return the width used for generating initial noise or set by providing a value."""
    if new_value is not None:
        new_value = int(new_value)
    return _set_or_return("seed_resize_from_w", new_value)


def height(new_value: Optional[int] = None) -> Optional[int]:
    """Return the image height or set by providing a value."""
    if new_value is not None:
        new_value = int(new_value)
    return _set_or_return("height", new_value)


def width(new_value: Optional[int] = None) -> Optional[int]:
    """Return the image width or set by providing a value."""
    if new_value is not None:
        new_value = int(new_value)
    return _set_or_return("width", new_value)


def queue(**temporary_kwargs) -> None:
    """Queue a job with the current parameters. Provide kwargs to override current parameters for this job only."""
    kwargs_copy = deepcopy(kwargs_txt2img)
    kwargs_copy.update(temporary_kwargs)
    args = list(kwargs_copy.values())
    args.append(0)
    job_queue.append(args)


def queue_prompt(prompt: str) -> None:
    """Queue a job with this prompt."""
    queue(prompt=prompt)


def info(subject=par):
    """Print the current parameter values or usage instructions."""
    if subject == par:
        print("Parameter values:")
        for key, value in kwargs_txt2img.items():
            if key == "sampler_index":
                key = "sampler_name"
                value = _sampler_index_to_name(value)
            print(f"{key}: {value}")
    elif subject == use:
        print("Usable functions:")
        print(f"p, prompt: {prompt.__doc__}")
        print(f"np, negative_prompt: {negative_prompt.__doc__}")
        print(f"ps, prompt_style: {prompt_style.__doc__}")
        print(f"Available prompt styles: {list(webui.modules.shared.prompt_styles.keys())}")
        print(f"st, steps: {steps.__doc__}")
        print(f"sn, sampler_name: {sampler_name.__doc__}")
        print(f"rf, restore_faces: {restore_faces.__doc__}")
        print(f"ni, n_iter: {n_iter.__doc__}")
        print(f"bs, batch_size: {batch_size.__doc__}")
        print(f"cfg, cfg_scale: {cfg_scale.__doc__}")
        print(f"se, seed: {seed.__doc__}")
        print(f"ss, subseed: {subseed.__doc__}")
        print(f"sst, subseed_strength: {subseed_strength.__doc__}")
        print(f"srfh, seed_resize_from_h: {seed_resize_from_h.__doc__}")
        print(f"srfw, seed_resize_from_w: {seed_resize_from_w.__doc__}")
        print(f"h, height: {height.__doc__}")
        print(f"w, width: {width.__doc__}")
        print(f"q, queue: {queue.__doc__}")
        print(f"qp, queue_prompt: {queue_prompt.__doc__}")
        print("i, i par, info, info par: Print current parameter values.")
        print("i use, info use: Print usage instructions.")


p = prompt
ps = prompt_style
np = negative_prompt
st = steps
sn = sampler_name
rf = restore_faces
ni = n_iter
bs = batch_size
cfg = cfg_scale
se = seed
ss = subseed
sst = subseed_strength
srfh = seed_resize_from_h
srfw = seed_resize_from_w
h = height
w = width
q = queue
qp = queue_prompt
i = info

print()
info(use)
print()
ipython_config = Config()
ipython_config.InteractiveShell.autocall = 2
IPython.embed(config=ipython_config)

shell_exited = True
webui.shared.state.interrupt()
sys.exit(0)

