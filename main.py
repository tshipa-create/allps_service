from model.allps_service import AllpsService
from icecream import ic
import util

if __name__ == "__main__":
    allps_service_instance = AllpsService()
    open_asi_auth_response_parser = allps_service_instance.authenticate()
    ic(open_asi_auth_response_parser.response_dict)
    promissory_id = "00004C40F2"
    """    
    get_instalment_response_parser = allps_service_instance.get_instalment(promissory_id=promissory_id, inst_num=1)
    ic(get_instalment_response_parser.response_dict)
    ic(get_instalment_response_parser.status)
    util.check_instalment_status(get_instalment_response_parser.status, "INCOMPLETE")
    """
    print("-------------------------------------------------")
    get_instalment_response_parser = allps_service_instance.get_instalment(promissory_id=promissory_id, inst_num=21)
    ic(get_instalment_response_parser.response_dict)
    ic(get_instalment_response_parser.status)
    util.check_instalment_status(get_instalment_response_parser.status, "INCOMPLETE")
    print("-------------------------------------------------")
    result = allps_service_instance.edit_instalment(promissory_id=promissory_id, inst_num=21, new_action_dt="2024032")
    ic(result.response_dict)
    
    