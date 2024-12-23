# Image Processor Script

This project provides a Python script for organizing photos and images from a temporary folder (`~/FOTOS_TEMP/`) into a structured folder hierarchy (`~/FOTOS/`). The structure is based on the year, month, and day extracted from the photos' EXIF metadata. The script supports both JPEG and RAW formats and avoids duplicating files that already exist in the destination folder.

## **Features**

- Organizes photos into `YEAR/MONTH/DAY` folders based on EXIF metadata.
- Supports both JPEG (`.jpg`, `.jpeg`) and RAW formats (`.arw`, `.dng`, `.mrw`).
- Uses `ExifTool` for robust metadata extraction, ensuring compatibility with various file types.
- Skips files that are already present in the destination directory.
- Provides a summary of copied/moves and skipped files after execution.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/jrborras/image_processor.git
cd image_processor
```

## Docker Setup

### Dockerfile

The `Dockerfile` builds a minimal Python container that runs the `process_images.py`.

```dockerfile
# Base image Python 3.12 (Debian)
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app/process_images.py /app/
COPY ./app/requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN apt-get update
RUN apt-get install -y libimage-exiftool-perl

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script when the container launches
CMD ["python", "process_images.py"]

# Run this commnad to do tests only, comment prevous CMD command
# CMD ["tail", "-f", "/dev/null"]
```

### docker-compose.yml

The `docker-compose.yml` file defines the `image-processor` service, which runs the `process_images.py` in a container. 

```yaml
version: "3.9"

services:

  image-processor:
    container_name: image-processor
    build: ./
    volumes:
      - ${ORIGIN_PHOTOS_TEMP}:${DEST_PHOTOS_TEMP}
      - ${ORIGIN_PHOTOS}:${DEST_PHOTOS}
    environment:
      - SOURCE_DIR=${DEST_PHOTOS_TEMP}
      - DEST_DIR=${DEST_PHOTOS}
    command: ["python", "process_images.py"]
```
## **Usage**

### **Run with Docker**
To use the script with Docker, follow these steps:

1. **Build the Docker Image**
   ```bash
   docker-compose build
   ```

2. **Run the Script in a Container**
   ```bash
   docker-compose up
   ```

---

## **Customization**

You can modify the supported file extensions or the folder paths in the script:
- Supported extensions: `.jpg`, `.jpeg`, `.raw`, `.dng`, `.nef`, `.crw`, `.cr2`, `.arw`, `.mrw`, `.heic`, `.mp4`.
- Folder paths can be adjusted using `SOURCE_DIR` and `DEST_DIR` environment variables.


## **License**

This project is licensed under the MIT License. See the [`LICENSE`](LICENSE) file for details.

---

## **Acknowledgements**

- [ExifTool](https://exiftool.org/) by Phil Harvey for robust metadata extraction.
