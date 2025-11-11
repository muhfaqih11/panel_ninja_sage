from utils import download_resource

def download_all_resources():
    resources_list = ["mission","enemy","weapon-effect","back_item-effect","accessory-effect","gamedata"]
    for resource in resources_list:
        download_resource(resource)

if __name__ == "__main__":
    download_all_resources()