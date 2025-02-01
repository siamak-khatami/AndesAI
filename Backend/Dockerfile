# if we do not specifify any version, it will always pull the latest
# it is not recommendad to do the latest since features can be chnaged over time
#FROM python:3.12.2
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel
# workdir is a directon in the docker container which is assumed your root directory to all your commands
# you will later copy your code base here as well
# this folder will be generated if there is no such a folder.
# When you make a workdir, it is similar to do a cd to the repo and run all commands there. So,
# in most applications you need to be presented in the workdir to run your code, thus it is a good practice
# to define the workdir
WORKDIR /usr/src/app

# ./ is WORKDIR
COPY Requirements.txt ./

# we run to install Requirements.txt
RUN pip install fastapi uvicorn
RUN python -m pip install --upgrade pip

RUN pip install --upgrade pip

RUN pip install -U bitsandbytes  ## The bitsandbytes installed is not sufficient and we need to install its latest version using this line

RUN pip install -r Requirements.txt


# this means copy all files from current directory to WORKDIR
# since it has a cache so it will skip adding Requirements again
COPY ./ ./


# Envoironemnt variables: can be managed here, in run command or composer.
# To define:
# ENV VARNAME
# To use ENV
# EXPOSE $VARNAME


# IF you need to give access to a specific system port, we need to expose the port to the container
# EXPOSE PORTNUMBER
# EXPOSE 80


# IF you want to attach a volume anonymously
# VOLUME ["/PATH"]


#CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# we do not want to have --reload in the production code, so, we keep it as a command in the docker-compose file.
# With no CMD, the base CMD of the image will be executed.

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
