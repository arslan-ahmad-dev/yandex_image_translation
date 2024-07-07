**Image Translation Tool**
This project translates an image with text from one language to another while keeping the same background.
The project uses a Flask API to handle the translation request.

**Create a Virtual Environment**
python -m venv myenv
myenv\Scripts\activate

**Install Requirements**
pip install -r requirements.txt

**Example Request using Postman**
**Set the request method to POST.**
**Enter the URL** : http://127.0.0.1:5000/yandex_scrapper

**Go to the Body tab and Select form-data and Add the following fields**
**input_image**: Choose the image file.
**source_language**: Enter the source language code (e.g., "fr").
**target_language**: Enter the target language code (e.g., "en").

**Click Send.**
