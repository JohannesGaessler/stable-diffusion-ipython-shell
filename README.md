# stable-diffusion-ipython-shell
IPython shell frontend for generating images with Stable Diffusion.

## Features

* txt2img
* Full IPython functionality during use.
* Prompt queuing.
* Negative prompts.
* Separate terminals for IPython and progress prints.

## Example Use
```
p "E=mc2"  # set prompt to E=mc2
q  # queue txt2img job
i  # print current parameter values
ni 50  # set number of iterations to 5
sn lms  # set sampler name to LMS
se 42  # set seed to 42
qp "r/aww"  # queue txt2img job with prompt "r/aww"
qp "bronze statue"  # queue txt2img job with prompt "bronze statue"
```

## Installation Instructions

1. Install Linux.
2. Install the [AUTOMATIC1111 "Voldemort" webui fork](https://github.com/AUTOMATIC1111/stable-diffusion-webui).
3. Copy the file `shell.py` to the root of your webui installation.

## Usage instructions

1. Open two terminals: a control terminal and a print terminal.
2. Execute the file `set_progress_print_out.sh` from this repository in the print terminal.
3. Navigate to the root directory of the webui installation with the control terminal.
4. Execute the `shell.py` script with the control terminal, e.g. via `python shell.py`. Any command line arguments are passed on to webui. If you get an ImportError at this stage please let me know (I have a non-standard webui installation).
