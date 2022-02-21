from flask import Blueprint,render_template,abort,request
from ProjectPackage import parameter
from linebot.exceptions import LineBotApiError,InvalidSignatureError
from ProjectPackage.linebot_control import echo,f #一定要匯入被綁定的函式才能讓裝飾器發揮作用
from ProjectPackage.forms import SettingsForm

app_route=Blueprint("app_basic",__name__,static_folder='static',template_folder='templates')
@app_route.route('/')
def home():
    return render_template('base.html')

@app_route.route('/delay/')
def delay():
    return render_template('delay.html')

@app_route.route('/settings/customer_data')
def settings_user():
    return render_template('settings-user.html',user=parameter.settings)

@app_route.route('/settings/',methods=['GET','POST'])
def settings():
    form=SettingsForm()
    if form.validate_on_submit():
        for each in form:
            print(each.data)
    print(parameter.settings)
    return render_template('settings.html',settings=parameter.settings,form=form)

@app_route.route('/finish/')
def finish():
    return render_template('finish.html')

@app_route.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    # app_route.logger.info("Request body: " + body)
    try:
        parameter.handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@app_route.route('/settings/reload')
def load_settings():
    return parameter.load_settings()