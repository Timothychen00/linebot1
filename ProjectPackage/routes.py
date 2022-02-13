from flask import Blueprint,render_template
app_route=Blueprint("app_basic",__name__,static_folder='static',template_folder='templates')
@app_route.route('/')
def home():
    return render_template('base.html')

@app_route.route('/delay/')
def delay():
    return render_template('delay.html')

@app_route.route('/settings/customer_data')
def settings_user():
    return render_template('settings-user.html')

@app_route.route('/settings/')
def settings():
    return render_template('settings.html')

@app_route.route('/finish/')
def finish():
    return render_template('finish.html')
