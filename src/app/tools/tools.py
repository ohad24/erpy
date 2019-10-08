import os
import random
import string
import io
from setup import app

allowed_extensions = {'png', 'jpg', 'jpeg', 'pdf', 'xls', 'xlsx', 'doc', 'docx'}


def gen_rand_str(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_file(sub_dir, file):
    filename, ext = os.path.splitext(file.filename)
    mimetype = file.mimetype
    gen_file_name = gen_rand_str(15) + ext
    path = os.path.join(app.config['UPLOAD_FOLDER'], sub_dir)
    file.save(os.path.join(path, gen_file_name))
    file_length = os.stat(os.path.join(path, gen_file_name)).st_size
    return gen_file_name, file_length, mimetype
