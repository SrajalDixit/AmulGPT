FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Build Chroma DB on container start
RUN python backend/chroma_setup.py

# Expose port for Gradio
EXPOSE 7860

# Run the frontend
CMD ["python", "frontend/app.py"]
