# syntax=docker/dockerfile:1
FROM ubuntu:22.04 AS base

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    zsh \
    mc \
    sudo \
    libgtk2.0-dev pkg-config \
    libgl1-mesa-glx ffmpeg libsm6 libxext6 \
    python3.10 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -G sudo --create-home --system --shell /bin/bash developer && \
    echo "developer ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/developer && \
    chown -R developer:developer /home/developer && \ 
    echo "export PATH=/home/developer/.local/bin:$PATH" >> /home/developer/.bashrc

RUN mkdir -p /app && chown developer:developer -R /app

# Bash
CMD ["$@"]

# ------------------------------------------------------------------------------
# Stage: Deploy
# ------------------------------------------------------------------------------
FROM base AS deploy

WORKDIR /app

# Copy the application
COPY --chown=developer:developer . .

USER developer

# Install Python dependencies
RUN /bin/bash -c \
    "python3 -m venv venv && \
    source venv/bin/activate && \
    python3 -m pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt && \
    deactivate"

# expose the port that the application will run on
EXPOSE 5000

# Run the application
ENTRYPOINT ["/app/venv/bin/python3"]
CMD ["/app/app.py"]
