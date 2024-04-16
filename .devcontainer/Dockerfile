FROM mcr.microsoft.com/devcontainers/miniconda:0-3

# Install a different version of Python than the default
RUN conda install -y python=3.10.13 \
    && pip install --no-cache-dir pipx 

# Copy environment.yml (if found) to a temp location so we update the environment. 
COPY .devcontainer/environment.yml /tmp/conda-tmp/
RUN conda env create -f /tmp/conda-tmp/environment.yml \ 
    && rm -rf /tmp/conda-tmp

# Copy the template to the share template folder
RUN mkdir -p /usr/local/share/omp-templates/
COPY .devcontainer/almeida.omp.json /usr/local/share/omp-templates/