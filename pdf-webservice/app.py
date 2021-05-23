from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, send_file
import utils
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['pdf', 'PDF'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 访问分割页面
@app.route('/')
def upload_test():
    return render_template('upload.html')


# 分割文档
@app.route('/api/splitpdf', methods=['POST'], strict_slashes=False)
def api_splitpdf():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    if 'myfile' not in request.files:
        return "No file part"
    file = request.files['myfile']
    interval = int(request.form.get("quantity"))  # id是前端调格式的，name是后端获取表单数据的

    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 创建工作文件夹，并将上传的pdf保存在该文件夹下
        randomName = str(uuid.uuid4()).split("-")[-1]
        curFileFolder = os.path.join(basedir, "upload", randomName)
        utils.makeCurWorkspace(curFileFolder)
        file.save(os.path.join(file_dir, randomName, filename + ".pdf"))
        # pdf文件分割业业务代码，将输出目录打包并返回
        input_dirPath = os.path.join(file_dir, randomName, filename + ".pdf")
        output_dirPath = os.path.join(file_dir, randomName, "output")
        utils.splitPDF(input_dirPath, output_dirPath, interval)
        utils.makeZip(curFileFolder)
        file_path = os.path.join(file_dir, randomName + ".zip")
        return send_file(file_path, as_attachment=True)
    return jsonify({"errno": 1001, "errmsg": "上传失败"})


@app.route('/api/deletepage', methods=['POST'], strict_slashes=False)
def api_deletepage():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    if 'myfile2' not in request.files:
        return "No file part"
    file = request.files['myfile2']
    deletePages = request.form.get("deletepages")

    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 创建工作文件夹，并将上传的pdf保存在该文件夹下
        randomName = str(uuid.uuid4()).split("-")[-1]
        curFileFolder = os.path.join(basedir, "upload", randomName)
        utils.makeCurWorkspace(curFileFolder)
        file.save(os.path.join(file_dir, randomName, filename + ".pdf"))
        # pdf文件分割业业务代码，将输出目录打包并返回
        input_dirPath = os.path.join(file_dir, randomName, filename + ".pdf")
        output_dirPath = os.path.join(file_dir, randomName, "output",
                                      filename + "_new.pdf")
        utils.deletePDF(input_dirPath, output_dirPath, deletePages)
        utils.makeZip(curFileFolder)
        file_path = os.path.join(file_dir, randomName + ".zip")
        return send_file(file_path, as_attachment=True)
    return jsonify({"errno": 1001, "errmsg": "上传失败"})


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)