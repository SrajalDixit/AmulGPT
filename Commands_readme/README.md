# Project Environment Setup Guide

## Package Management

### Installing a package
```bash
pip install <package-name>
```

### Uninstalling a package
```bash
pip uninstall <package-name>
```

### Upgrading a package
```bash
pip install --upgrade <package-name>
```

### Listing installed packages
```bash
pip list
```

### To run a python file

```bash
python file_name.py
```

## Conda Environment Setup

### Create an environment
```bash
conda create -n <env-name> python=3.10
```

### Activate an env

```bash
conda activate <env-name>
```

### To save env in a file
```bash
conda activate amulgpt
conda env export > environment.yml
```

### Remove an env
```bash
conda env remove -n myenv
```

### list all envs
```bash 
conda env list
```

## Docker setup

### Installing Docker

```bash
# In your WSL terminal
sudo apt update
sudo apt install docker.io -y
```

### Start docker

```bash
sudo service docker start
sudo usermod -aG docker $USER
```

## To check ubuntu version

```bash
lsb_release -a
```

## Ollama setup

### To install ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### To pull a model

```bash
ollama pull llama3.2:1b
```

### To run the model

```bash
ollama run llama3.2:1b
```
