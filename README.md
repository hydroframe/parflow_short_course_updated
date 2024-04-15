# Instructions for getting setup for the IDEAS-watersheds subsettools workshop 

**Note:** *The Docker image might take a while to download, so make sure you do these steps ahead of the workshop.*

  1.  Follow the instructions [here](https://hydroframesubsettools.readthedocs.io/en/latest/getting_started.html#creating-a-hydrogen-hydroframe-hydrodata-account-and-registering-a-pin) to create a Hydrogen account.
  2.	Go to [Docker](https://www.docker.com/products/docker-desktop/) and download Docker Desktop. Make sure you download the correct version based on your computer’s operating system and architecture. Follow the instructions to install Docker Desktop. ![alt text](https://github.com/gartavanis/IDEAS-watersheds/blob/main/Docker.png)
  3.	Launch Docker Desktop. The application should be running while you do the next steps. (You might need to create a Docker account and sign in if you don’t already have one.)
  4.	Start a new terminal session (outside Docker) to type the commands in the next two steps:
  5.	Pull the parflow/subsettools image from DockerHub. Choose the correct version based on your computer’s architecture.
**NOTE:** *If your Docker is running out of space, you might need to use [docker system prune](https://docs.docker.com/engine/reference/commandline/system_prune/) with the appropriate options to clear out old containers and make space for the new one.*
- For the x86_64/amd64 (Intel Chip for Mac or Windows) architecture:
```bash
docker pull george135/subsettools_amd64
```
- For the arm64 (M1/M2 chip for Mac) architecture:
```bash
docker pull george135/subsettools_arm64
```
  6. Once the image has finished downloading, you can run the container with:
- For the x86_64/amd64 architecture:
```bash
docker run -dp 8888:8888 george135/subsettools_amd64:latest start-notebook.sh --NotebookApp.token=''
```
- For the arm64 architecture:
```bash
docker run -dp 8888:8888 george135/subsettools_arm64:latest start-notebook.sh --NotebookApp.token=''
```
  7. Use a browser to navigate to your [JupyterLab container](http://localhost:8888/lab?) or use the link that will appear next to your container on the Docker Desktop application: ![alt text](https://github.com/gartavanis/IDEAS-watersheds/blob/main/Docker2.png)
  8. You should see a JupyterLab environment like this: ![alt text](https://github.com/gartavanis/IDEAS-watersheds/blob/main/Docker3.png)
  9. Click on the Terminal application to start a terminal session *inside* the container.
 10. Clone the GitHub repository that contains the example workflows for `subsettools` and `hf_hydrodata`:
```bash
git clone https://github.com/hydroframe/subsettools-binder.git
```
 11. Navigate to `subsettools-binder` -> `subsettools` folder and click on the `definte_subset.ipynb` notebook. ![alt text](https://github.com/gartavanis/IDEAS-watersheds/blob/main/Docker4.png)
 12. Make sure the notebook runs successfully without errors. **You will need to provide your Hydrogen email and pin in the first code cell of the notebook.**
 13. Congratulations, you're all setup for Sunday!
 14. The documentation for [subsettools](https://hydroframesubsettools.readthedocs.io/en/latest/index.html) and [hf_hydrodata](https://hf-hydrodata.readthedocs.io/en/latest/) is hosted at Read The Docs
