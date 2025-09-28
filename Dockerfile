# Base image with Miniconda
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy environment file
COPY environment.yml .

# Create the conda environment
RUN conda env create -f environment.yml

# Copy project files
COPY . .

# Expose the port
EXPOSE 8000

# Use bash and activate conda environment at runtime
CMD ["bash", "-c", "source activate amulgpt && python -m app.gradio_app"]





