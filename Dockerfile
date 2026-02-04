FROM python:3.9-slim

WORKDIR /app

# Create a non-root user (Hugging Face Spaces requirement/recommendation)
RUN useradd -m -u 1000 user && \
    chown -R user:user /app

USER user
ENV PATH="/home/user/.local/bin:$PATH"

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . /app

# Expose port 7860
EXPOSE 7860

# Start the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
