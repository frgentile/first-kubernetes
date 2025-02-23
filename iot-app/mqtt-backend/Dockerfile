# syntax=docker/dockerfile:1
FROM ubuntu:22.04 AS base

LABEL author="Francisco GENTILE <ingentile@gmail.com>"
LABEL description="Bridge between a MQTT broker and a MongoDB database"

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc git sudo \
    python3.10 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -G sudo --create-home --system --shell /bin/bash developer && \
    echo "developer ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/developer && \
    # chown -R developer:developer /home/developer && \ 
    echo "export PATH=/home/developer/.local/bin:$PATH" >> /home/developer/.bashrc

# Create app folder and own it to the developer user
RUN mkdir -p /app && chown developer:developer -R /app

CMD ["$@"]

# ------------------------------------------------------------------------------
# Stage: Deploy
# ------------------------------------------------------------------------------
FROM base AS deploy

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY --chown=developer:developer . /app

# Switch to the developer user
USER developer

# # Install any needed packages specified in requirements.txt
# RUN --mount=type=cache,target=/home/developer/.cache/pip pip install --no-cache-dir -r requirements.txt
RUN /bin/bash -c \
    "python3 -m venv venv && \
    source venv/bin/activate && \
    python3 -m pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt && \
    deactivate"

# Run app.py when the container launches
ENTRYPOINT [ "/app/venv/bin/python3" ]
CMD ["main.py"]
