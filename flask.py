__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "2019-09-18"
__app__ = "mp_donntu_spark_hdfs"
__status__ = "Development"


from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run("0.0.0.0")