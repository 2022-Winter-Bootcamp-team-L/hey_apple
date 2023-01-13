import os, json
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from environ import ImproperlyConfigured #예외처리용2

BASE_DIR = Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, 'secrets.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

#sys.version 3.10 이상 부터 가능하다고 하는데 왜 안되는지 알 수 없음 ;;
'''
def error_check_mailAPI_reason(agrument):
    match agrument:
        case 0:
            return "send_email_api check - unknown error : code check"
        case 1:
            return "success - 여기 들어오면 안되는데?"
        case 2:
            return "mail setting check - maybe parsing error"
        case 3:
            return "dbcon check - maybe Tuple not in database"
        case 4:
            return "mail check - maybe send error"
        case default:
            return "error - unknown error"
        
#print(error_check_mailAPI_reason(2))
'''
# 버전 실패로 안될 경우

def error_check_mailAPI_sub(arg):
    error_check = {0:"send_email_api check - unknown error : code check", 
                   1: "success - 여기 들어오면 안되는데?",
               2: "mail setting check - maybe parsing error", 
               3: "dbcon check - maybe 투플이 없는 경우", 
               4: "mail check - maybe send error"}
    
    return error_check[arg]
    #print(error_check[arg])
    #for k, v in error_check.items():
        #print("key: {}, value: {}".format(k, v))
    #return result
