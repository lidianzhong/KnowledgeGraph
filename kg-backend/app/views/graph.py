import json

from django.views.decorators.csrf import csrf_exempt
from app.utils.jsonResponse import json_response
from app.models import User
# from app.models import Graph

# 处理三元组数据
graph_path = 'app/utils/testData/graph.json'
graph_path_entity_map = 'app/utils/testData/entityId_map.txt'
graph_path_relation_map = 'app/utils/testData/relationId_map.txt'
@csrf_exempt
def get_graph(request):
    if request.method == 'GET':

        import json

        # 读取txt文件，将序号与对应字符串存储在字典中
        entity_dict = {}
        relation_dict = {}

        with open(graph_path_entity_map, "r", encoding="utf-8") as txt_file:
            for line in txt_file:
                index, entity_type = line.strip().split("\t")
                entity_dict[int(index)] = entity_type

        with open(graph_path_relation_map, "r", encoding="utf-8") as txt_file:
            for line in txt_file:
                index, relation_type = line.strip().split("\t")
                relation_dict[int(index)] = relation_type

        # 读取JSON文件并更改"entity_type"的值
        with open(graph_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

            # 统计出现次数的entity_type
            entity_type_count = {}

            for vertex in data["Vertices"]:
                entity_type = vertex["entity_type"]

                # 查找txt文件对应的 entity_type 并更改
                if entity_type in entity_dict:
                    vertex["entity_type"] = entity_dict[entity_type]

                if entity_dict[entity_type] in entity_type_count:
                    entity_type_count[entity_dict[entity_type]] += 1
                else:
                    entity_type_count[entity_dict[entity_type]] = 1

            for edge in data["Edges"]:
                relation_type = edge["relationship_type"]
                # 查找txt文件对应的 relation_type 并更改
                if relation_type in relation_dict:
                    edge["relationship_type"] = relation_dict[relation_type]

        # 对entity_type出现次数进行排序并取前四名
        sorted_entity_types = sorted(entity_type_count.items(), key=lambda x: x[1], reverse=True)[:4]

        return json_response(200, '请求成功', {'graph': data, 'mostCalledType': sorted_entity_types})
    else:
        return json_response(203, '请求方式错误')

