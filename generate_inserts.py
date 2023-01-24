from alive_progress import alive_bar
import requests
import shutil
import random
import json
import time
import os

ASSETS_PATH = './assets'
OUTPUT_PATH = './output'
INSERTS_PATH = f'{OUTPUT_PATH}/Inserts'
IMAGES_PATH = f'{OUTPUT_PATH}/Images'
CACHE_PATH = f'{ASSETS_PATH}/cache'
CUSTOM_PATH = f'{ASSETS_PATH}/custom'
INPUT_PATH = './inserts.json'
TEMPLATE_PATH = './template.xhtml'


def download_image(filename: str, url: str) -> None:
  with open(filename, 'wb') as f:
    r = requests.get(url)
    if r.status_code == 200:
      f.write(r.content)

opf_items_inserts = []
opf_items_images = []
opf_items_itemrefs = []

inserts = []
with open(INPUT_PATH, 'rb') as f:
  inserts = [e for e in json.load(f)["inserts"] if e["chapter"] is not None]
  inserts.sort(key=lambda e: e["chapter"])

xhtmlTemplate = ''
with open(TEMPLATE_PATH, 'r') as f:
  xhtmlTemplate = f.readlines()
  xhtmlTemplate = ''.join(xhtmlTemplate)

with alive_bar(len(inserts), dual_line=True, title='Generating Inserts') as bar:
  shutil.rmtree(f'{OUTPUT_PATH}')
  os.makedirs(f'{INSERTS_PATH}', exist_ok=True)
  os.makedirs(f'{IMAGES_PATH}', exist_ok=True)
  os.makedirs(f'{CACHE_PATH}', exist_ok=True)
  os.makedirs(f'{CUSTOM_PATH}', exist_ok=True)

  for insert in inserts:
    bar.text = f'-> Getting data for next insert...'
    chapter = '{:0>4}'.format(insert["chapter"])
    key = insert["key"]
    title = insert["title"]
    sub = insert["sub"]
    vert = insert["vert"]
    url = insert["url"]

    bar.text = f'-> Getting image for: `{key}` insert...'
    # get image from url
    if 'http' in url:
      # check cache first
      if os.path.exists(f'{CACHE_PATH}/{key}.jpg'):
        bar.text = f'-> Copying cached asset `{key}.jpg` to `{IMAGES_PATH}`...'
        os.system(f'cp {CACHE_PATH}/{key}.jpg {IMAGES_PATH}/{key}.jpg')
      else:
        # if not in cache, download it
        bar.text = f'-> Waiting before downloading `{key}.jpg`'
        # wait a bit to not trigger rate limit
        time.sleep(1+.5*random.random())
        bar.text = f'-> Downloading `{key}.jpg` from `{url}`...'
        download_image(f'{CACHE_PATH}/{key}.jpg', url)
        bar.text = f'-> Copying asset `{key}.jpg` to `{IMAGES_PATH}`...'
        os.system(f'cp {CACHE_PATH}/{key}.jpg {IMAGES_PATH}/{key}.jpg')
    else:
      # url is a local file
      if os.path.exists(f'{CUSTOM_PATH}/{key}.jpg'):
        bar.text = f'-> Copying custom asset `{key}.jpg` to `{IMAGES_PATH}`...'
        os.system(f'cp {CUSTOM_PATH}/{key}.jpg {IMAGES_PATH}/{key}.jpg')
      else:
        # raise error
        raise Exception(f'ERROR: key `{key}` specified a local file but it does not exist in `{CUSTOM_PATH}`.')

    # generate xhtml file
    bar.text = f'-> Generating `i-{chapter}-{key}.xhtml file`'
    with open(f'{INSERTS_PATH}/i-{chapter}-{key}.xhtml', 'w+', encoding='utf8') as f:
      content = ''
      if title is not None:
        content += f'<div class="title">{title}</div>'
      if sub is not None:
        content += f'\n    <div class="sub">{sub}</div>'
      if vert is not None:
        content += f'\n    <div class="vert">{vert}</div>'
      f.write(xhtmlTemplate.format(title=title, key=key, content=content))

    # add to opf
    opf_items_inserts += f'    <item id="i-{chapter}-{key}.xhtml" href="Inserts/i-{chapter}-{key}.xhtml" media-type="application/xhtml+xml"/>\n'
    opf_items_images += f'    <item id="{key}.jpg" href="Images/{key}.jpg" media-type="image/jpeg"/>\n'
    opf_items_itemrefs += f'<itemref idref="i-{chapter}-{key}.xhtml"/>\n'

    # bump progress bar
    bar()

  # dump opf items
  with open(f'{OUTPUT_PATH}/opf_items.txt', 'w+') as f:
    for item in opf_items_inserts:
      f.write(item)
    f.write('\n')
    for item in opf_items_images:
      f.write(item)
    f.write('\n')
    for item in opf_items_itemrefs:
      f.write(item)
