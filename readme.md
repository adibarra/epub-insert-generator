# EPUB Insert Generator

## About

This is a simple script to generate EPUB3 xhtml files.
It was designed to be used to generate image inserts.

The script takes a JSON file as input and generates a folder with the xhtml files.
Insert.css is used to style the xhtml files and should be added to the EPUB3 container.

## Installation

```bash
# Clone the repository
$ git clone https://github.com/adibarra/epub-insert-generator
$ cd epub-insert-generator

# Create a virtual environment and install the requirements
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install -r requirements.txt
```

## Usage

```bash
# rename example_inserts.json to inserts.json
$ mv example_inserts.json inserts.json

# edit inserts.json
$ nano inserts.json
```

## Format

| Field | Description |
| --- | --- |
| `chapter` | Used in the file name so that the files are ordered correctly. |
| `key` | Used to generate the name of the xhtml and image files. It should be unique. |
| `title` | Used to generate the main text xhtml file. |
| `sub` | Used to generate the subtitle the xhtml file. |
| `vert` | Used to generate the vertical text in the xhtml file. |
| `url` | Used to download the image used in the xhtml file. |

The `inserts.json` file should have the following format:

```json
{
  "inserts": [
    {
      "chapter": 0,                                // Chapter number
      "key": "cool",                               // Unique key
      "title": "Cool image",                       // Main text
      "sub": "This is an image from a url",        // Sub text
      "vert": "Stored in the assets/cache folder", // Vertical text
      "url": "https://example.com/image.jpg"       // Url or path to image
    },
    {
      "chapter": 1,
      "key": "custom",
      "title": "Custom Image",
      "sub": "This is a custom image",
      "vert": "Stored in the assets/custom folder",
      "url": "./assets/custom/custom-image.jpg"
    }
  ]
}

```
