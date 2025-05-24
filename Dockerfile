FROM devkitpro/devkita64:latest

# Setup workdir
WORKDIR /usr/src

# Update package cache and install deps
RUN apt update && \
    apt upgrade -y && \
    apt install -y gpg wget curl build-essential cmake

# Install Mise
# This is a toolchain manager, but I'm mainly using it here to install a specific verison of python
RUN install -dm 755 /etc/apt/keyrings && \
    wget -qO - https://mise.jdx.dev/gpg-key.pub | gpg --dearmor | tee /etc/apt/keyrings/mise-archive-keyring.gpg 1> /dev/null && \
    echo "deb [signed-by=/etc/apt/keyrings/mise-archive-keyring.gpg arch=amd64] https://mise.jdx.dev/deb stable main" | tee /etc/apt/sources.list.d/mise.list && \
    apt update && \
    apt install -y mise && \
    # this sets up non-interactive sessions
    echo 'eval "$(mise activate bash --shims)"' >> ~/.bash_profile && \
    # this sets up interactive sessions
    echo 'eval "$(mise activate bash)"' >> ~/.bashrc && \
    # source mise for the rest of this build
    . ~/.bash_profile

# Install Python
RUN mise install python@3.12 && mise use -g python@3.12

# Install rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain nightly -y && \
    # source rust env
    . $HOME/.cargo/env && \
    # We use nightly, since it's required for some of our compilation targets
    rustup default nightly && \
    # Add the aarch64 compile target since switch is an arm based cpu
    rustup target add aarch64-unknown-none
