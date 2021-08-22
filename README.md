# 1. Intro

In this project, we are dealing with a multi-class classification problem where we are given a set of songs, their metadata ((check out `data/README` provided by the author OR my analytics notebook `notebook/exploratory_data_analysis.ipynb` for more information)) and their genres (target label).

A simple 4-Fold LightGBM model with selected & engineered features was trained (cross validation test accuracy of ~69.6%), and a simple web service with the following APIs was build:
1. [POST] classifier/predict-batch : Classify input data (in the form of .csv files) and persist the song's trackid, title and genre (prediction results) to the database.
2. [GET] genre/list : Returns a list of classified genres in the database.
3. [GET] genre/title-list : Returns a list of titles, given a genre.

Demo video of the web service:


https://user-images.githubusercontent.com/43180977/130363067-3ee13b7a-4f80-42a6-810a-789264d3848b.mov



# 2. Setups

## 2.1 Web Service & Database (Postgres)
1. Install docker.
2. Clone this repo, change directory to project root `cd <wherever-this-repo-is>`.
3. Build docker containers (web service and database) using `docker-compose build`.
4. Start docker containers `docker-compose up`.
5. By default, the database is empty, so you need to use the `predict-batch` API to upload the first batch of data. The simplest way to do this is via the FastAPI Swagger UI of the web service (one of the containers you started in `Step 4`), which can be accessed on http://0.0.0.0:5000/docs : 
    1. Go to the Swagger UI.
    2. Click on `[POST] /api/v1/predict-batch` -> `Try it out`.
    3. Input the `client-id`, `client-secret` (`test` for both, unless you made changes to `env/api-service.env`).
    4. Under `csv_file`, select either the training `data/features.csv` or test `data/test.csv` files
    5. Execute and you should see some data in your database now (use the other GET APIs to confirm this).

## 2.2 Analytics & Tuning Notebooks
1. Install [poetry](https://python-poetry.org/docs/#installation) and [jupyter notebook](https://jupyter.org/install) (or if you prefer to install this in the current environment only, do `poetry add notebook` after `Step 4`)
2. Clone this repo, change directory to project root `cd <wherever-this-repo-is>`.
3. Install project dependencies `poetry install`
4. Activate poetry environment `poetry shell`
5. Install Jupyter kernel `python ipykernel -m install --user --name "music-clf" --display-name "music-clf"`
6. Activate jupyter notebook `jupyter notebook`
7. Navigate to the notebook folder and select the notebook to run interactively (remember to change the kernel to `music-clf` created in `Step 5`)

### Additional : Getting the Transformer Files
If you intend to use the pretrained transformer to generate embeddings for the UMAP (in analytics notebook), you need to:
1. Create a new folder `model/paraphrase_tinybert`
2. Download the model files from [HuggingFace Model Hub](https://huggingface.co/sentence-transformers/paraphrase-TinyBERT-L6-v2)
3. Move the contents to the folder created in `Step 1`.

### 2.3 Tests
To confirm that the web services work (especially if you made changes to the logics in the future), we run unit tests on the codebase. This is how you can do it:
1. Make sure the database container is up (otherwise, repeat `Section 2.1`).
2. Make a new `.env` file in project root, and copy the contents from `env/api-service.env` to it, with the following changes:
    - IS_LOCAL=true
    - MODEL_PATH=/<your-full-home-path>/<this-project>/model/deployment/
3. Change directory to project root, run `pytest`.
4. Check if all tests passed, otherwise, figure out why.

# 3. Documentations

## 3.1 Analytics Findings
Check out the notebook `notebook/exploratory_data_analysis.ipynb`. Every section of the notebook is organised in the similar manner:
1. Observations
2. Insights/ Decisions
3. Bunchs of code & plots related to the section

In each section, I plotted the features, explored their characteristics across genres and made notes on these observations as well as the subsequent modelling & feature engineering decisions derived from them.

## 3.2 OpenAPI
In addition to the FastAPI Swagger UI, the OpenAPI documentation can be found in `openapi.json` too. This can be imported to Postman or [Swagger Editor](https://editor.swagger.io/) directly

# 4. Others Thoughts on Maintainability & Extensibility

## 4.1 Consistent Folder Structure
In this project, I attempted to modularize the code base, and as much as possible, use similar folder structure to organize the web service.

There are currently 3 resources (classifier, genre, healthcheck). Each resource:
- Is organised into a separate folder & added to the main app using `api_router`
- Has a `schema` folder which stores the Pydantic models for input & output validation (generated from sample responses, which are stored in `schema/response_json`)
- Has a `router.py` which stores the API logics

Something like this:

```
src/genre
├── __init__.py
├── router.py
└── schema
    ├── response_json
    │   └── genre_list.json  # Sample model of /genre/list API output
    ├── input_data.py        # Model for all /genre/ API input params
    └── genre_list.py        # Model for /genre/list API
```

## 4.2 Handling Environment Variables
These are handled using `env/*.env` files, so that we can easily switch between local/ staging/ production environment, just by changing & deploying the right `.env` files. These can also be modified into `configmap.yaml` / `secrets.yaml` easily, if a managed Kubernetes cluster is used in staging/ production.

## 4.3 Scaling the Service
With the `Dockerfile`, an image can be easily built and deployed on cloud services (e.g. AWS Elastic Beanstalk using image stored on AWS ECR), which then enables configurable automatic load-balancing & scaling.

In terms of database, we can also easily swap out the better-spec database (e.g. AWS RDS Postgres w mutli-AZ deployment for enhanced data durability & availability) with the existing one, by simply changing the `POSTGRES_URI` in `/env/api-service.env`.

Lastly, in terms of scaling the web service securely in production environment, the `client-id` and `client-secret` are the required authentication headers for all the APIs (except healthcheck). These can be set to rotate on a scheduled interval, using something like AWS Secrets Managers to better secure the APIs.