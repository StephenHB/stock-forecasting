# STOC #

Run through steps following to setup local developing environment.

### Prerequisites ###

* Python version: 3.9.1
* Conda / MiniConda
### Verify Requisites ###
Open your terminal (MacOs) or PowerShell (Windows) and run following command
```console
python --version
```
You should see the output like:
```console
Python 3.9.1
```

### Setup Project (Only need to run once) ###

#### 1. Clone the repo and checkout to your feature branch (Run following command in your termibal)
```console
git clone <repo_remote_url>
cd stoc
git fetch
git checkout <feature_branch_name>
```
#### 2. Create a virtual environment
```console
conda env create -f environment.yml
```
#### 3. Activate virtual environment
```console
conda activate njenv
```
#### 4. Open your project in Jupyter Lab.
```console
jupyter lab
```
### Done! You are ready to go! ###
To deactivate virtual environment, just run following command in you terminal
```console
conda deactivate
```
### Sync Virtual Environment With Teamates ###
#### Export/Update environment.yml file (Should happens when you update the virtual environment. e.g. Install/Uninstall some packages)
```console
# For Windows users
conda env export --no-builds | findstr -v "prefix" > environment.yml

# For Mac users
conda env export --no-builds | grep -v "prefix" > environment.yml
```
#### Update local virtual environment (Should happens when others updated the environment.yml file)
```console
conda env update --file environment.yml  --prune
```
