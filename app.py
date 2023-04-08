from flask import Flask, request, jsonify
from flask_cors import CORS
import test as ai
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return jsonify({'message': 'Hello, World!'})

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    # Nhận dữ liệu được gửi từ client
    data = request.get_json()

    # Xử lý dữ liệu, ví dụ lưu vào database
    data_dict = data
    answer_dict = data_dict['answers']
    result_list = []

    result_list.append(int(data_dict['mssv']))

    for key in answer_dict:
        result_list.append(int(answer_dict[key]))

    print(result_list)
    print(len(result_list))
    
    # Mở file JSON trong chế độ ghi
    with open("data.json", "w") as f:
    # Lưu dữ liệu vào file JSON
        json.dump(result_list, f)
    # Đóng file
    f.close()
    # Trả về phản hồi cho client
    return jsonify({'status': 'success'})

@app.route('/get_Learning_Path', methods=['GET'])
def get_Learning_Path():
    with open('data.json', 'r') as f:
        data = json.load(f)
    if not data:
        print("File data.json is empty.")
    else:
        result = ai.get_learning_path_knn(data)

        result_list = result.split("{")[1].split("}")[0].split(",")
        print(result_list)
        return jsonify(result_list)
if __name__ == '__main__':
    app.run()



