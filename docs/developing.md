# Developing SSHDR (Running from Source)

If you want to contribute, develop or otherwise run SSHDR from source, you'll need to meet a few pre-requisites.


<hr />

## Contents

- [Pre-requisites](#️-pre-requisites)
- [Python Setup](#python-setup)
- [ASM Setup](#asm-setup)
  - [Rust Setup](#rust-setup)
- [Troubleshooting](#troubleshooting)

<hr />


## ❗️ Pre-Requisites

Necessary:
- `python 3.12`

For [ASM development](#asm-setup):
- `rust`
- `devkitA64`

### Python Setup

#### 1. Clone

```sh
git clone git@github.com:mint-choc-chip-skyblade/sshd-rando.git && cd sshd-rando
```

#### 2a. Setup Virtual Env

```sh
py -m venv .venv
# or
python -m venv .venv
# or
python3 -m venv .venv

source .venv/bin/activate
```

#### 2b. Install Dependencies

How you install dependencies and run depends on how you installed python 3.

```sh
py -m pip install -r requirements.txt
# or
python -m pip install -r requirements.txt
# or
python3 -m pip install -r requirements.txt
```

#### 3. Add Extract

Add your `romfs` and `exefs` to `./sshd_extract`.

You won't be able to test randomization without it, so you'll need it during development as well. Our `.gitignore` will prevent you from accidentally committing those files, so it's safe to put there.

#### 4. Tests

```sh
# Run tests one after another
pytest

# Run tests in parallel
pytest -n auto
```

#### 5. Run

```sh
py ./sshdrando.py
# or
python ./sshdrando.py
# or
python3 ./sshdrando.py
```

### ASM Setup

Compiling ASM **requires** `devkitpro` to be installed. See [ASM Readme](../asm/README.md) for full instructions.


#### Rust Setup

Setting up rust requires installing [rustup](https://rustup.rs/), which will bring `cargo` and `rustc` with it, among other essential rust tools.

All rust source can be found within `./asm/additions/rust-additions`.

Rather than compiling these with rust ourselves, these are compiled alongside all other assembly with a python script. You can use:

```sh
cd ./asm # must be in asm directory

py ./assemble.py
# or 
python ./assemble.py
# or
python3 ./assemble.py
```


### Compiling from Source

For the most part, it's recommended to just compile from GitHub Actions. They're consistent and build for all platforms.


### Troubleshooting

> #### nlzss11 failed to install

Occasionally, `cmake` causes issues when trying to install `nlzss11`. The error is never very clear, but when `nlzss11` fails with a pip install, it is often `cmake`.

We specifically care about the `cmake` installed via the pip toolchain in order to run from source and develop locally.

One thing that can help resolve this is installing cmake directly via pip.

```sh
pip install cmake
```
