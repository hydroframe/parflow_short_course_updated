# Setting up the workspace for the ParFlow short course

The recommended option is CodeSpaces. This will be the easiest to setup and follow along during the workshop. Docker should only be used as a fallback.

## Instructions for setting up the codespaces for the ParFlow short course:

**Note:** *The Codespace image might take a while to build, so make sure you do these steps ahead of the workshop.*

  1.  Follow the [GitHub documentation](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github) to create a personal GitHub account.
  2.  Browse to the [course repo](https://github.com/hydroframe/parflow_short_course_updated).
  3.  Click on the "Code" green button and then select "Create codespace on main". The codespace will launch in a new tab. This step can take up to 15-20 minutes when the codespace is building for the first time. When you subsequently launch the codespace, it will start up much faster. ![alt text](https://github.com/hydroframe/parflow_short_course_updated/blob/main/codespace1.png)
  4. Once the codespace completes building, navigate to the `gridding` folder and click on the `box_domain_setup_full.ipynb` notebook. ![alt text](https://github.com/hydroframe/parflow_short_course_updated/blob/main/codespace2.png)
  5. Run the notebook. When prompted to select a kernel for the Jupyter notebook, click on "Python Environments" and then select the Virtual Environment. ![alt text](https://github.com/hydroframe/parflow_short_course_updated/blob/main/codespace3.png)
  6. Make sure the notebook runs successfully without errors. ![alt text](https://github.com/hydroframe/parflow_short_course_updated/blob/main/codespace4.png)
  7. Congratulations, you're all setup!

## Instructions for setting up Docker for the ParFlow short course:

**Note:** *The Docker image might take a while to download, so make sure you do these steps ahead of the workshop.*

  1.  Follow the instructions [here](https://hydroframesubsettools.readthedocs.io/en/latest/getting_started.html#creating-a-hydrogen-hydroframe-hydrodata-account-and-registering-a-pin) to create a Hydrogen account.
  2.	Make sure you have the latest version of Docker Desktop. Go to [Docker](https://www.docker.com/products/docker-desktop/) and download Docker Desktop. Make sure you download the correct version based on your computer’s operating system and architecture. Follow the instructions to install Docker Desktop. ![alt text](https://github.com/hydroframe/parflow_short_course_updated/blob/main/Docker.png)
  3.	Launch Docker Desktop. The application should be running while you do the next steps. (You might need to create a Docker account and sign in if you don’t already have one.)
  4.	Start a new terminal session (outside Docker) to type the commands in the next two steps:
  5.	Pull the parflow/subsettools image from DockerHub. Choose the correct version based on your computer’s architecture.
**NOTE:** *If your Docker is running out of space, you might need to use [docker system prune](https://docs.docker.com/engine/reference/commandline/system_prune/) with the appropriate options to clear out old containers and make space for the new one.*
- For the x86_64/amd64 (Intel Chip for Mac or Windows) architecture:
```bash
docker pull george135/subsettools_amd64-june2025
```
- For the arm64 (M1/M2 chip for Mac) architecture:
```bash
docker pull george135/subsettools_arm64-june2025
```
  6. Once the image has finished downloading, you can run the container with:
- For the x86_64/amd64 architecture:
```bash
docker run -dp 8888:8888 george135/subsettools_amd64-june2025:latest start-notebook.sh --NotebookApp.token=''
```
- For the arm64 architecture:
```bash
docker run -dp 8888:8888 george135/subsettools_arm64-june2025:latest start-notebook.sh --NotebookApp.token=''
```
  7. Use a browser to navigate to your [JupyterLab container](http://localhost:8888/lab?) or use the link that will appear next to your container on the Docker Desktop application: ![alt text](https://github.com/hydroframe/parflow_short_course_updated/blob/main/Docker2.png)
  8. You should see a JupyterLab environment like this: ![alt text](https://github.com/hydroframe/parflow_short_course_updated/blob/main/Docker3.png)
  9. Click on the Terminal application to start a terminal session *inside* the container.
 10. Clone the ParFlow short course GitHub repository:
```bash
git clone https://github.com/hydroframe/parflow_short_course_updated.git
```
 11. Navigate to the `gridding` folder and click on the `box_domain_setup_full.ipynb` notebook.
 12. Make sure the notebook runs successfully without errors. ![alt text](https://github.com/hydroframe/parflow_short_course_updated/blob/main/Docker4.png)
 13. Congratulations, you're all setup!


## Instructions for setting up ParFlow locally with pre-built MacOS and Linux binaries

Please note that this feature is under development. Future ParFlow releases with include pre-built binaries as part of the release. More information will be provided in the [ParFlow Google Group](https://groups.google.com/g/parflow?pli=1).

### MacOS

1. Download the pre-built binaries from [here](https://github.com/parflow/parflow/actions/runs/26672439563/artifacts/7304739867).
2. Navigate to your `Downloads` folder, and double-click on the zip archive `parflow-macos-arm64.zip`. The resulting `install` directory is where ParFlow will be located on your system.
3. Open your terminal, and run the following command from the `Downloads` directory:
```bash
xattr -dr com.apple.quarantine install/
```
4. Set the `PARFLOW_DIR` environment variable to your install location. For example, in a Python script, add the line
```Python
os.environ['PARFLOW_DIR'] = '/Users/<your_username>/Downloads/install'
```

or in a shell script, add the line
```bash
export PARFLOW_DIR=/Users/<your_username>/Downloads/install
```
5. Note that in addition to these pre-built binaries, you will also need a Python environment containing `pftools`. This package can be installed with
```bash
pip install pftools
```

### Linux

1. Download the pre-built binaries from [here](https://github.com/parflow/parflow/actions/runs/26650477704/artifacts/7297049803). You will get a file like `parflow-pr-742-7f54d79e4655c3dd2abdfd5bb12759cfa43a3adb-linux-x86_64.tar.gz.zip`
2. Run the following commands:

```bash
unzip parflow-pr-742-7f54d79e4655c3dd2abdfd5bb12759cfa43a3adb-linux-x86_64.tar.gz.zip
tar -xvf parflow-pr-742-7f54d79e4655c3dd2abdfd5bb12759cfa43a3adb-linux-x86_64.tar.gz
```
You will end up with a directory called `release-install`. This is where your local ParFlow installation will be located.

3. Set the `PARFLOW_DIR` environment variable to your install location. For example, in a Python script, add the line
```Python
os.environ['PARFLOW_DIR'] = '/path/to/release-install'
```
or in a shell script, add the line
```bash
export PARFLOW_DIR=/path/to/release-install
```

Alternatively, you can source the `parflow-env.sh` script. This will set the PARFLOW_DIR variable in your shell.
```bash
source parflow-env.sh 
```

4. Note that in addition to these pre-built binaries, you will also need a Python environment containing `pftools`. This package can be installed with
```bash
pip install pftools
```