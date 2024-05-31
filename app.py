from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import random
import json
import os

app = Flask(__name__)

word_dict = {}

def save_to_file():
    with open('words.json', 'w') as file:
        json.dump(word_dict, file)

def load_from_file():
    if os.path.exists('words.json'):
        with open('words.json', 'r') as file:
            return json.load(file)
    else:
        return {}

@app.route('/')
def index():
    return render_template('index.html', word_dict=word_dict)

@app.route('/add_word', methods=['POST'])
def add_word():
    word = request.form['word']
    translation = request.form['translation']

    if word in word_dict:
        # 单词已存在
        return jsonify({'message': f'单词 "{word}" 已存在。'})

    # 添加新单词
    word_dict[word] = translation
    save_to_file()
    return jsonify({'message': f'单词 "{word}" 已成功添加。'})


@app.route('/study')
def study():
    if word_dict:
        random_word = random.choice(list(word_dict.keys()))
    else:
        random_word = None
    return render_template('study.html', random_word=random_word, word_dict=word_dict)

if __name__ == '__main__':
    word_dict = load_from_file()
    app.run(debug=True)



@app.route('/delete_words', methods=['POST'])
def delete_words():
    words_to_delete = request.get_json()['words']
    for word in words_to_delete:
        if word in word_dict:
            word_dict.pop(word)
    save_to_file()
    return jsonify(success=True)
