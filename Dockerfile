FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get upgrade -y

RUN apt install -y python3

RUN apt install -y wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y \
        apt-utils lsb-core cmake git \
        libopencv-dev \
        protobuf-compiler \
        libprotobuf-dev \
        libgoogle-glog-dev \
        libboost-all-dev \
        hdf5-tools \
        libhdf5-dev \
        libatlas-base-dev
        

RUN git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git

WORKDIR openpose

# Latest commit as of 18 Jan 22.
# Change if you need to, but be aware that dependencies may have changed.
RUN git checkout 6f0b8868bc4833b4a6156f020dd6d486dcf8a976

WORKDIR scripts/ubuntu

RUN sed -i 's/\<sudo -H\>//g' install_deps.sh; \
    sed -i 's/\<sudo\>//g' install_deps.sh; \
    sync; sleep 1;

WORKDIR /openpose/build

# Downloads all available models. You can reduce image size by being more selective.
RUN cmake -DGPU_MODE:String=CPU_ONLY \
          -BUILD_PYTHON:Bool=ON \
          -DOWNLOAD_BODY_25_MODEL:Bool=ON \
          -DDOWNLOAD_BODY_MPI_MODEL:Bool=OFF \
          -DDOWNLOAD_BODY_COCO_MODEL:Bool=OFF \
          -DDOWNLOAD_FACE_MODEL:Bool=OFF \
          -DDOWNLOAD_HAND_MODEL:Bool=OFF \
          -DUSE_MKL:Bool=OFF \
          ..

# you may find that you need to adjust this.
RUN make -j$((`nproc`+1))

RUN apt-get remove wget unzip cmake git build-essential -y && apt-get autoremove -y

WORKDIR /openpose

