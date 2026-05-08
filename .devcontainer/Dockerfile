ARG BASE_IMAGE=ubuntu:24.04
FROM ${BASE_IMAGE}

SHELL ["/bin/bash", "+o", "pipefail", "-c"]

# Non interactive mode
ENV DEBIAN_FRONTEND=noninteractive

# Fetch the latest definitions of packages
RUN apt-get update && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    apt-get install -y tzdata && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    apt-get install -y \
        build-essential \
        curl \
        libcurl4 \
        git \
        vim \
        gfortran \
        libopenblas-dev \
        liblapack-dev \
        openssh-client \
        openssh-server \
        openmpi-bin \
        libopenmpi-dev \
        python3 \
        python3-pip \
        python3-venv \
        tcl-dev \
        tk-dev && \
    rm -rf /var/lib/apt/lists/*

RUN getent group ubuntu >/dev/null || groupadd -g 1000 ubuntu && \
    id -u ubuntu >/dev/null 2>&1 || useradd -u 1000 -g ubuntu -m -N -s /bin/bash ubuntu

USER ubuntu
WORKDIR /home/ubuntu/
ENV BASE_PATH=/home/ubuntu/

RUN mkdir -p                              \
    $BASE_PATH/parflow/build               \
    $BASE_PATH/parflow/dependencies/cmake   \
    $BASE_PATH/parflow/dependencies/silo-src \
    $BASE_PATH/parflow/dependencies/hdf5-src  \
    $BASE_PATH/parflow/dependencies/hypre-src  \
    $BASE_PATH/parflow/dependencies/netcdf-src

# -----------------------------------------------------------------------------
# Setup CMake
# -----------------------------------------------------------------------------

ARG CMAKE_URL=https://cmake.org/files/v3.29/cmake-3.29.0-linux-x86_64.tar.gz

RUN cd $BASE_PATH/parflow/dependencies/cmake && \
    curl -L $CMAKE_URL | tar --strip-components=1 -xzv

ENV CMAKE=$BASE_PATH/parflow/dependencies/cmake/bin/cmake
ENV CTEST=$BASE_PATH/parflow/dependencies/cmake/bin/ctest

# -----------------------------------------------------------------------------
# Install HDF5
# -----------------------------------------------------------------------------

ARG HDF5_URL=https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.0/src/hdf5-1.12.0.tar.gz

ENV HDF5_DIR=/opt/hdf5

WORKDIR $BASE_PATH/parflow/dependencies/hdf5-src
RUN curl -L $HDF5_URL | tar --strip-components=1 -xzv && \
    CC=mpicc ./configure \
      --prefix=$HDF5_DIR \
      --enable-parallel && \
    make

USER root
RUN make install
USER ubuntu

# -----------------------------------------------------------------------------
# Install NetCDF
# -----------------------------------------------------------------------------

ARG NETCDF_URL=https://github.com/Unidata/netcdf-c/archive/v4.7.4.tar.gz

ENV NETCDF_DIR=/opt/netcdf

WORKDIR $BASE_PATH/parflow/dependencies/netcdf-src
RUN curl -L $NETCDF_URL | tar --strip-components=1 -xzv && \
    CC=mpicc CPPFLAGS=-I$HDF5_DIR/include LDFLAGS=-L$HDF5_DIR/lib \
    ./configure --disable-shared --disable-dap --prefix=${NETCDF_DIR} && \
    make

USER root
RUN make install
USER ubuntu

# -----------------------------------------------------------------------------
# Install Hypre
# -----------------------------------------------------------------------------

ARG HYPRE_VERSION=v2.19.0

ENV HYPRE_DIR=/opt/hypre

WORKDIR $BASE_PATH/parflow/dependencies/hypre-src
RUN git clone https://github.com/hypre-space/hypre.git --single-branch --branch $HYPRE_VERSION

WORKDIR $BASE_PATH/parflow/dependencies/hypre-src/hypre/src
RUN ./configure --prefix=$HYPRE_DIR --with-MPI

USER root
RUN make install
USER ubuntu

# -----------------------------------------------------------------------------
# Install Parflow
# -----------------------------------------------------------------------------

RUN git clone -b master --depth 1 --single-branch \
    https://github.com/parflow/parflow.git \
    $BASE_PATH/parflow/src

RUN $CMAKE                     \
    -S $BASE_PATH/parflow/src   \
    -B $BASE_PATH/parflow/build  \
    -D CMAKE_BUILD_TYPE=Release   \
    -D HDF5_ROOT=$HDF5_DIR         \
    -D PARFLOW_ENABLE_HDF5=TRUE     \
    -D HYPRE_ROOT=$HYPRE_DIR         \
    -D PARFLOW_ENABLE_HYPRE=TRUE      \
    -D PARFLOW_HAVE_CLM=TRUE             \
    -D PARFLOW_ENABLE_TIMING=TRUE          \
    -D PARFLOW_AMPS_LAYER=mpi1              \
    -D PARFLOW_AMPS_SEQUENTIAL_IO=TRUE       \
    -D PARFLOW_ENABLE_NETCDF=TRUE             \
    -D NETCDF_DIR=$NETCDF_DIR                  \
    -D CMAKE_EXE_LINKER_FLAGS="-Wl,--no-as-needed -L$HDF5_DIR/lib -lhdf5_hl -lhdf5 -ldl -lz -lm -lmvec" \
    -D CURL_LIBRARY=/usr/lib/x86_64-linux-gnu/libcurl.so.4

USER root
ENV HOME=/root
RUN $CMAKE --build $BASE_PATH/parflow/build
RUN $CMAKE --install $BASE_PATH/parflow/build --prefix /opt/parflow
USER ubuntu
ENV HOME=/home/ubuntu

# -----------------------------------------------------------------------------
# Python virtual environment for notebooks/utilities
# -----------------------------------------------------------------------------

ENV VIRTUAL_ENV=/home/ubuntu/.venv
RUN python3 -m venv "$VIRTUAL_ENV" && \
    "$VIRTUAL_ENV/bin/pip" install --upgrade pip setuptools wheel && \
    "$VIRTUAL_ENV/bin/pip" install \
      "subsettools>=2.0.1" \
      "hf_hydrodata>=1.4.3" \
      "matplotlib>=3.7.2" \
      "bokeh>=3.3.0" \
      jupyter \
      ipykernel
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PARFLOW_DIR=/opt/parflow/
ENV LD_LIBRARY_PATH=/opt/hdf5/lib:/opt/netcdf/lib:/opt/parflow/lib:/opt/hypre/lib:/usr/include:$LD_LIBRARY_PATH
WORKDIR /home/ubuntu/