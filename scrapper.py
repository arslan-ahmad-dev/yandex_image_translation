import os
import cv2
import random
import requests
import numpy as np
import pytesseract
from flask_cors import CORS
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw
from flask import Flask, request, jsonify, send_file
from flask_uploads import configure_uploads, UploadSet, DOCUMENTS
from helpers_method.get_fonts import get_box_size, create_font, get_text_color
from helpers_method.utils import initialize_ocr, get_translate_headers, clean_text

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class OCRTranslator:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.config['UPLOADED_DOCUMENTS_DEST'] = "downloaded_images"
        self.app.config['UPLOADED_DOCUMENTS_ALLOW'] = ['gif', 'png', 'jpg', 'jpeg', 'bmp']
        self.app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

        self.docs = UploadSet('documents', DOCUMENTS)
        configure_uploads(self.app, self.docs)

        self.project_dir = os.path.abspath(os.path.dirname(__file__))
        self.ocr_configs, self.fonts = initialize_ocr()
        
        self.translate_url = "https://translate.yandex.net/api/v1/tr.json/translate"
        self.translate_headers = get_translate_headers()
        self.user_agents = self._get_user_agents()

        self.app.route('/')(self._index)
        self.app.route('/yandex_scrapper', methods=['POST'])(self._translate_image_text)

    def _get_user_agents(self):
        user_agents_filename = 'user_agents.txt'
        user_agents_path = os.path.join(self.project_dir, 'helpers_method', user_agents_filename)
        with open(user_agents_path, 'r') as f:
            data = f.read()
            user_agents = data.split('\n')
            return user_agents

    def _get_ocr(self, lang):
        ocr_config = self.ocr_configs.get(lang)
        if ocr_config:
            return PaddleOCR(**ocr_config)
        else:
            return None

    def validation_required1(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    def _extract_text_from_image(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        extracted_text = pytesseract.image_to_string(gray_image)
        return extracted_text
    
    @validation_required1
    def _index(self):
        return "OCR Translator API"

    def _translate_image_text(self):
        if 'input_image' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        input_file = request.files['input_image']
        if input_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        file_content = input_file.read()
        if not file_content:
            return jsonify({'error': 'File is empty'}), 400
        
        image_array = np.frombuffer(file_content, np.uint8)
        decoded_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        extracted_text = self._extract_text_from_image(decoded_image)

        source_language = request.form.get('source_language', 'en')
        target_language = request.form.get('target_language', 'no')

        form_data = {
            "text": [extracted_text],
            "options": "0"
        }

        random_user_agent = random.choice(self.user_agents)
        self.translate_headers['User-Agent'] = random_user_agent
        
        translate_params = {
            "id": "58cb3738.668a5bfd.2c43d02a.74722d696d616765-0-0",
            "srv": "tr-image",
            "source_lang": source_language,
            "target_lang": target_language,
            "reason": "ocr",
            "format": "html",
            "strategy": "0",
            "disable_cache": "false",
        }

        response = requests.post(self.translate_url, headers=self.translate_headers, params=translate_params, data=form_data)

        if response.status_code != 200:
            return jsonify({'error': 'Failed to translate text'}), response.status_code
        
        translated_text = clean_text(response.json()['text'][0])

        random_number = random.randint(0, 99999999)
        unique_filename = f"{random_number}_{input_file.filename.lower()}"

        input_file.seek(0)

        image_url = self.docs.save(input_file, folder='image', name=unique_filename.replace(" ", ""))
        img_path = os.path.join(self.app.config['UPLOADED_DOCUMENTS_DEST'], image_url)

        if not os.path.exists(img_path):
            return jsonify({'error': 'File was not saved correctly'}), 500
        
        with open(img_path, 'rb') as f:
            saved_file_content = f.read()
        if not saved_file_content:
            return jsonify({'error': 'Saved file is empty'}), 500
        
        ocr_processor = self._get_ocr(source_language)
        if not ocr_processor:
            return jsonify({'error': 'Unsupported source language'}), 400
        
        ocr_results = ocr_processor.ocr(img_path, cls=True)[0]
        image_path = Image.open(img_path)
        text_boxes = [line[0] for line in ocr_results]

        draw_image = ImageDraw.Draw(image_path)

        translated_text = translated_text.strip()
        api_response_text = [segment.strip() for segment in clean_text(translated_text.strip()).split('\n')]
        
        if len(api_response_text) != len(ocr_results) and len(api_response_text) > len(ocr_results):
            api_response_text = [segment for segment in api_response_text if segment.strip() and '@' not in segment and not ('(' in segment and len(segment) < 3)]
        
        if len(ocr_results) != len(api_response_text):
            min_length_index = min(range(len(api_response_text)), key=lambda i: len(api_response_text[i]))
            api_response_text.pop(min_length_index)

        for ocr_result in range(len(ocr_results)):
            box_size = get_box_size(text_boxes[ocr_result])
            rgb_color = image_path.getpixel(((text_boxes[ocr_result][0][0]), (text_boxes[ocr_result][0][1])))

            try:
                recognized_text = api_response_text[ocr_result]
            except Exception as e:
                pass
                # return f"Exception Due To : {str(e)}"

            font_style = self.fonts.get(target_language, os.path.join(self.project_dir, "fonts/arial.ttf"))
            generated_font = create_font(recognized_text, box_size, font_style)
            text_position = (((text_boxes[ocr_result][0][0])), ((text_boxes[ocr_result][0][1])))

            background_color = rgb_color
            values_box = tuple(map(tuple, text_boxes[ocr_result]))
            draw_image.polygon(values_box, fill=background_color)
            
            if str(type(rgb_color)) == "<class 'int'>":
                background_color = tuple([rgb_color, rgb_color, rgb_color])

            text_color = get_text_color(background_color)
            draw_image.text(text_position, recognized_text, font=generated_font, fill=text_color)
        
        real_path = f'{self.project_dir}/downloaded_images/output/{random_number}.png'
        image_path.save(real_path)

        output_dir = os.path.join(self.project_dir, 'downloaded_images/output')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f'{random_number}.png')
        image_path.save(output_path)

        return send_file(output_path, mimetype='image/png')

    def run(self):
        self.app.run(debug=True)
if __name__ == '__main__':
    ocr_translator = OCRTranslator()
    ocr_translator.run()
