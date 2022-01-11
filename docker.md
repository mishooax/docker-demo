## Docker

0. **BUILD** an image (using the `Dockerfile`):

```shell
docker build -t <IMAGE-NAME:IMAGE-TAG> PATH-TO-DOCKERFILE | URL | -
```

1. **START / STOP / DELETE**

```shell
docker run --name <CONTAINER-NAME> -p <HOST-PORT>:<CONTAINER-PORT> <IMAGE-NAME:IMAGE-TAG> -w <WORKDIR>
```

Other interesting options:
- `[-e | --env]`: set environment variables
- `[-m | --memory]`: memory limit (in bytes)
- `[--d | --detach]`: run container in background (prints container ID)
- `[--gpus all]`: add all GPU devices to the container
- `[-P | --publish-all]`: publish _all_ exposed ports to _random_ ports (to avoid conflicts)
- `--pull 'always | missing | never'`: pull image before running (default == `missing`)
- `--rm`: automatically remove container when it exits
- `[-v | --volume list]`: bind mount a volume (can also mount volumes from another container with `--volume-driver`)

Stop the containe. This sends a termination signal for graceful shutdown; if the process doesn't respond or shut down in <SECONDS> seconds then Docker kills it.

```shell
docker stop [--time <SECONDS>] <CONTAINER-IDs>
```

Delete a container:

```shell
docker rm <CONTAINER-NAME>
```

Delete an image:

```shell
docker rmi <IMAGE-NAME:IMAGE:TAG>
```

2. **LIST**

List all images:

```shell
docker images
```

List all containers:

```shell
docker ps [--all]  [--latest] [--last <NUMBER>] [--size]
```

3. **LOGS / INFO**, etc.

```shell
# display the logs of a container
docker logs <CONTAINER-NAME>
# inspect produces lots of information in JSON-format: state (env vars, run-cmd, status, ...), config, network settings, etc.
docker inspect <CONTAINER-NAME>
```

4. **LAYERS**

```shell
# shows all the layers of an image - these were produced by docker build
docker history <IMAGE-NAME:IMAGE:TAG>
```

Example:

```shell
$ docker history eccr.ecmwf.int/ai4copernicus/ai4copernicus:v2
IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
99a5ffa956ba   4 days ago     /bin/bash --login -c #(nop)  CMD ["jupyter-l…   0B
bc860824f1c1   4 days ago     /bin/bash --login -c #(nop)  CMD ["/bin/bash…   0B
c08e0ca3d11b   5 days ago     /bin/bash --login -c #(nop)  ENTRYPOINT ["/u…   0B
b73b8c7711ca   5 days ago     |3 gid=100 uid=1000 username=ai4cop /bin/bas…   640MB
5de3f73a8798   5 days ago     |3 gid=100 uid=1000 username=ai4cop /bin/bas…   5.8GB
6809b7044072   5 days ago     /bin/bash --login -c #(nop)  ENV ENV_PREFIX=…   0B
eed316dd908c   5 days ago     /bin/bash --login -c #(nop) WORKDIR /home/ai…   0B
6b92d6a38094   5 days ago     |3 gid=100 uid=1000 username=ai4cop /bin/bas…   0B
039ac8977abb   5 days ago     /bin/bash --login -c #(nop)  ENV PROJECT_DIR…   0B
dc11262dca17   5 days ago     |3 gid=100 uid=1000 username=ai4cop /bin/bas…   714B
1a548591f860   5 days ago     |3 gid=100 uid=1000 username=ai4cop /bin/bas…   49B
47d598b9ef8e   5 days ago     /bin/bash --login -c #(nop)  ENV PATH=/home/…   0B
053296d783dc   5 days ago     |3 gid=100 uid=1000 username=ai4cop /bin/bas…   342MB
8cb0d0919950   5 days ago     /bin/bash --login -c #(nop)  ENV CONDA_DIR=/…   0B
ffd9f3916386   5 days ago     /bin/bash --login -c #(nop)  ENV MINICONDA_V…   0B
b7377a22d036   5 days ago     /bin/bash --login -c #(nop)  USER ai4cop        0B
3f066cc07e63   5 days ago     |3 gid=100 uid=1000 username=ai4cop /bin/bas…   67B
88692b69cc73   5 days ago     /bin/bash --login -c #(nop) COPY file:c08142…   67B
86c628b4bd0f   5 days ago     |3 gid=100 uid=1000 username=ai4cop /bin/bas…   184B
d154d6d199f3   5 days ago     /bin/bash --login -c #(nop) COPY file:ac2b48…   184B
f92e179c00d0   5 days ago     |3 gid=100 uid=1000 username=ai4cop /bin/bas…   596B
c0a01349c583   5 days ago     /bin/bash --login -c #(nop) COPY multi:59e93…   596B
3f43d03af77f   5 days ago     |3 gid=100 uid=1000 username=ai4cop /bin/bas…   360kB
3262d13f9ae8   5 days ago     |3 gid=100 uid=1000 username=ai4cop /bin/bas…   0B
fccd65c06c1f   5 days ago     /bin/bash --login -c #(nop)  ENV HOME=/home/…   0B
626a194fd7ba   5 days ago     /bin/bash --login -c #(nop)  ENV GID=100        0B
8aaf973bef6d   5 days ago     /bin/bash --login -c #(nop)  ENV UID=1000       0B
3932f272753a   5 days ago     /bin/bash --login -c #(nop)  ARG gid=100        0B
24a11b60e94a   5 days ago     /bin/bash --login -c #(nop)  ARG uid=1000       0B
f328a20f3d5a   5 days ago     /bin/bash --login -c #(nop)  ARG username=ai…   0B
0dc8be95f058   5 days ago     /bin/bash --login -c yum update -y &&     yu…   213MB
b655ee6f3067   5 days ago     /bin/bash --login -c #(nop)  SHELL [/bin/bas…   0B
50f2a99ec78c   5 days ago     /bin/sh -c #(nop)  LABEL maintainer=MA <ma@e…   0B
eeb6ee3f44bd   3 months ago   /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>      3 months ago   /bin/sh -c #(nop)  LABEL org.label-schema.sc…   0B
<missing>      3 months ago   /bin/sh -c #(nop) ADD file:b3ebbe8bd304723d4…   204MB
```

5. **DISTRIBUTE** an image to a hub

Add an image **tag** that includes the Docker Hub ID:

```shell
docker tag demo:v1 eccr.ecmwf.int/ai4copernicus/demo:v1
```

Login and push the image to the Hub:

```shell
# login
docker login -u <USER-ID> -p <SECRET> eccr.ecmwf.int
# push to hub
docker push eccr.ecmwf.int/ai4copernicus/demo:v1
```

### Connecting to a Docker container

```shell
# -i: run in interactive mode
# -t: allocates a pseudo-terminal (TTY) so i can use the shell properly
# NB: this is running under the ai4cop account (as set up in the Dockerfile)

$ docker exec -i -t ai4cop-v2-test2 bash
[ai4cop@1701c0ef633d app]$ ll
total 4
drwxr-xr-x. 1 ai4cop users 4096 Jan  6 08:22 env
[ai4cop@1701c0ef633d app]$ ps auxc
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
ai4cop         1  0.0  0.0  88636 61848 ?        Ss   08:56   0:00 jupyter-lab
ai4cop        49  0.1  0.0  11804  1924 pts/0    Ss   10:14   0:00 bash
ai4cop        81  0.0  0.0  51732  1716 pts/0    R+   10:14   0:00 ps
```

The container uses its own Process ID _namespace_ so it has its own process tree wth its own ID number sequence. Said tree is a subtree of the hosts's full process tree. The container also has an isolated filesystem:

```shell
[ai4cop@1701c0ef633d app]$ ls /
anaconda-post.log  bin  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```