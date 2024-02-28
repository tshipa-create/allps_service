from model.allps_service import AllpsService
from icecream import ic


if __name__ == "__main__":
    allps_service_instance = AllpsService()
    open_asi_auth_response_parser = allps_service_instance.authenticate()
    ic(open_asi_auth_response_parser.response_dict)
    promissory_id = "00004CDB46"
    get_instalment_response_parser = allps_service_instance.get_instalment(promissory_id, 1)
    ic(get_instalment_response_parser.response_dict)
    print("-------------------------------------------------")
    get_instalment_response_parser = allps_service_instance.get_instalment(promissory_id, 61)
    ic(get_instalment_response_parser.response_xml)
