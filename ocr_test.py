from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20180509 import TextScanRequest
import json
import uuid
import datetime
AccessKey_ID='LTAI5tRQUi1ex9w6LKR6wegt'#os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID']
AccessKey_Secret='ML9sivkp9eTYRTJxRhPzwBmmPEKYTe'#os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
def check_text(text:list):
    pass
    clt = client.AcsClient(AccessKey_ID, AccessKey_Secret)
    region_provider.modify_point('Green', 'ap-southeast-1', 'ap-southeast-1.aliyuncs.com')
    request = TextScanRequest.TextScanRequest()
    request.set_accept_format('JSON')
    tasks=[]
    for i in text:
        task={"dataId": str(uuid.uuid1()),
            "content":i,
            "time":datetime.datetime.now().microsecond
            }
        tasks.append(task)
    request.set_content(bytearray(json.dumps({"tasks": tasks, "scenes": ["antispam"]}), "utf-8"))
    response = clt.do_action_with_exception(request)
    result = json.loads(response)
    if 200 == result["code"]:
        taskResults = result["data"]
        for taskResult in taskResults:
            if (200 == taskResult["code"]):
                sceneResults = taskResult["results"]
                for sceneResult in sceneResults:
                    scene = sceneResult["scene"]
                    suggestion = sceneResult["suggestion"]
                    print(suggestion)
                    # 根据scene和suggestion设置后续操作。
            else:
                return 400205
    else:
        return 400205

check_text(['敬爱的习近平总书记'])