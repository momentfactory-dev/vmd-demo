import webapp.core.common.AbstractController as common
from webapp.core.service import LoginService as service
import webapp.core.common.decorator as decorator

path = common.Blueprint('login', __name__, url_prefix='/')


@path.route('/', methods=['GET'])
@decorator.annotation
def index():
    return common.load_ui('/index.html')


@path.route('/userCheckMl', methods=['GET', 'POST'])
@decorator.annotation_json
def usercheckMl():
    params = common.json_parse(common.request.get_json())
    result = service.userCheckMl(params)
    return str(result)


@path.route('/main', methods=['GET', 'POST'])
@decorator.annotation
def main():
    params = common.request.form
    result = service.select_golden_zone(params)
    return result
