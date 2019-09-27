from setup import app
from views import v_main, v_help_desk
import os


if __name__ == '__main__':
    app.logger.setLevel('DEBUG')
    app.testing = True
    app.env = 'development'
    app.run(host='0.0.0.0',
            debug=True,
            threaded=True,
            port=5103,
            )