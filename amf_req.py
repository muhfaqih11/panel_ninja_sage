from utils import send_amf_request
import config
from utils import Crypt, get_random_n_seed

def check_version():
    result = send_amf_request('SystemLogin.checkVersion',[config.BUILD_NUM])
    return result

def get_all_characters():
    account_id = config.login_data['uid']
    session_key = config.login_data['sessionkey']

    parameters = [account_id, session_key]
    result = send_amf_request("SystemLogin.getAllCharacters", parameters)
    # save_to_json(result,"all_chars")
    config.all_char = result
    char_list = []
    for i in range(result["total_characters"]):
        print(i+1,". Character ID: ",result["account_data"][i]["char_id"],"Character Name: ",result["account_data"][i]["character_name"],"Character Level: ",result["account_data"][i]["character_level"])
        char_list.append(result["account_data"][i]["char_id"])
    return char_list

def get_character_data(char_id):

    parameters = [char_id, config.login_data['sessionkey']]
    result = send_amf_request("SystemLogin.getCharacterData", parameters)
    # save_to_json(result,"char_data")
    config.char_data = result
    return result
                
def login(username, password, char_dot__, char_dot__underscore):

    # encryption stub – you'll need to fill in the actual routine
    encrypted = Crypt.encrypt(password, char_dot__, char_dot__underscore)
    specific_item = char_dot__underscore+"40367c3cc999a9f9e951a1d33211545b84b2d5a63933b0020433000c3bb410fb"+char_dot__underscore+char_dot__underscore+char_dot__underscore+char_dot__underscore
    random_seed = get_random_n_seed(int(char_dot__underscore), config.BYTES_LOADED)

    params = [
        username,
        encrypted,
        float(char_dot__underscore),  
        config.BYTES_LOADED,
        config.BYTES_TOTAL,
        char_dot__,            
        specific_item,
        random_seed,          
        len(password)
    ]
    result = send_amf_request('SystemLogin.loginUser',params)
    #encode request
    
    # save_to_json(result,"login_data")
    return result