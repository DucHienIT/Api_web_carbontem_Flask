from flask import Flask, request, jsonify
from flask_cors import CORS
import test as ai
import json
import pyodbc 
# s = 'DUCTHINHPC' #Your server name 
# d = 'Hackathon' #Your database name
# str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';Trusted_Connection=yes'
str = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:hackathon-server-carbon.database.windows.net,1433;Database=hackathon-db-new;Uid=ducthinh-carbon;Pwd=th@nCarbo;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
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

    #them du lieu vua submit vao bang quiz
    # print(result_list)
    # print(len(result_list))
    conn = pyodbc.connect(str)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dbo.SinhVien(MSSV) VALUES (?)", result_list[0])
    cursor.execute("INSERT INTO dbo.Quiz(MSSV, Cau1, Cau2, Cau3, Cau4, Cau5, Cau6, Cau7, Cau8, Cau9, Cau10, Cau11, Cau12, Cau13, Cau14, Cau15, Cau16, Cau17, Cau18, Cau19, Cau20, Cau21, Cau22, Cau23, Cau24, Cau25, Cau26, Cau27, Cau28, Cau29, Cau30, Cau31, Cau32, Cau33, Cau34, Cau35) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", result_list[0], result_list[1], result_list[2], result_list[3], result_list[4], result_list[5], result_list[6], result_list[7], result_list[8], result_list[9], result_list[10], result_list[11], result_list[12], result_list[13], result_list[14], result_list[15], result_list[16], result_list[17], result_list[18], result_list[19], result_list[20], result_list[21], result_list[22], result_list[23], result_list[24], result_list[25], result_list[26], result_list[27], result_list[28], result_list[29], result_list[30], result_list[31], result_list[32], result_list[33], result_list[34], result_list[35])
    conn.commit()
    conn.close()
    
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
