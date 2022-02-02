FROM centos:7

LABEL maintainer="MA <ma@email.com>"

SHELL [ "/bin/bash", "--login", "-c" ]

RUN yum update -y && \
    yum install -y wget bzip2 curl git && \
    yum clean -y all

# Create a non-root user
ARG username=ai4cop
ARG uid=1000
ARG gid=100
# ENV USER=$username
ENV UID=$uid
ENV GID=$gid
ENV HOME=/home/$username

RUN echo $username

RUN useradd \
    --uid $UID \
    --gid $GID \
    --home $HOME \
    $username

COPY environment.yml requirements.txt /tmp/
RUN chown $UID:$GID /tmp/environment.yml /tmp/requirements.txt

COPY postBuild /usr/local/bin/postBuild.sh
RUN chown $UID:$GID /usr/local/bin/postBuild.sh && \
    chmod u+x /usr/local/bin/postBuild.sh

COPY docker/entrypoint.sh /usr/local/bin/
RUN chown $UID:$GID /usr/local/bin/entrypoint.sh && \
    chmod u+x /usr/local/bin/entrypoint.sh

USER $username

# install miniconda
ENV MINICONDA_VERSION py38_4.10.3
ENV CONDA_DIR $HOME/miniconda3
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-$MINICONDA_VERSION-Linux-x86_64.sh -O ~/miniconda.sh && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh

# make non-activate conda commands available
ENV PATH=$CONDA_DIR/bin:$PATH

# make conda activate command available from /bin/bash --login shells
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile

# make conda activate command available from /bin/bash --interative shells
RUN conda init bash

# create a project directory inside user home
ENV PROJECT_DIR $HOME/app
RUN mkdir $PROJECT_DIR
WORKDIR $PROJECT_DIR

# copy source and notebook files
RUN mkdir $PROJECT_DIR/src
COPY src/* $PROJECT_DIR/src/

RUN mkdir $PROJECT_DIR/notebooks
COPY notebooks/*.ipynb $PROJECT_DIR/notebooks/

# build the conda environment
ENV ENV_PREFIX $PROJECT_DIR/env
RUN conda update --name base --channel defaults conda && \
    conda env create --prefix $ENV_PREFIX --file /tmp/environment.yml --force && \
    conda clean --all --yes && \
    rm /tmp/environment.yml

# run the postBuild script to install the JupyterLab extensions
RUN conda activate $ENV_PREFIX && \
    /usr/local/bin/postBuild.sh && \
    conda deactivate

# use an entrypoint script to insure conda environment is properly activated at runtime
ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

# default command will launch JupyterLab server for development with no password/token.
# --generate-config ensure jupyter config file is created before first launch
# CMD ["jupyter" "lab" "--generate-config"]
CMD [ "jupyter-lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
