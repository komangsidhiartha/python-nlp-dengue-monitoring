from flask import Flask, render_template
from flask_nav import Nav
from flask_nav.elements import *
# from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig


nav = Nav()

# registers the "top" menubar
nav.register_element('top', Navbar(
    View('Widgits, Inc.', 'index'),
    View('Our Mission', 'about'),
    Subgroup(
        'Products',
        View('Wg240-Series', 'products', product='wg240'),
        View('Wg250-Series', 'products', product='wg250'),
        Separator(),
        View('Wg10X', 'products', product='wg10x'),
    ),
))


def create_app(configfile=None):	
	app = Flask(__name__, template_folder="templates", static_folder="static")
	nav.init_app(app)
	AppConfig(app)
	# Bootstrap(app)
	app.config['BOOTSTRAP_SERVE_LOCAL'] = True

	@app.route('/')
	def index():
		return render_template('index.html')

	@app.route('/products/<product>/')
	def products(product):
		return render_template('index.html', msg='Buy our {}'.format(product))

	@app.route('/about-us/')
	def about():
		return render_template('index.html')

	return app

if __name__ == '__main__':
    create_app().run(debug=True)