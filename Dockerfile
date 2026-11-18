# Stage 1: Base build stage
FROM python:3.14-slim AS builder

ARG INSTALL_DEV=false

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install pipenv
RUN pip install pipenv

# Copy the requirements file first (better caching)
COPY Pipfile Pipfile.lock ./

# Install dependencies, dev packages only for development
RUN if [ "$INSTALL_DEV" = "true" ]; then \
      pipenv install --deploy --system --dev; \
    else \
      pipenv install --deploy --system; \
    fi

# Stage 2: Production stage
FROM python:3.14-slim

RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.14/site-packages/ /usr/local/lib/python3.14/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
