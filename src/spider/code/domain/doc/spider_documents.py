import json

from llama_index.core import Document

from src.spider.code.tool.CodeTool import query_area


def init_area_info() -> list[Document]:
    """
    通过跟spider-node交互,获取到子域，子域base，子域的功能，三个数组信息 进行组合返回
    :return:
    """
    area_all = query_area()
    return json_convert_doc(area_all)


def json_convert_doc(json_data: json) -> list[Document]:
    area_function_info_docs = area_function_info_doc(safe_get(json_data, 'areaPluginInfos'))
    base_area_info_docs = base_area_info_doc(safe_get(json_data, 'sonAreaCodeBases'))
    son_area_info_docs = son_area_info_doc(safe_get(json_data, 'sonAreaInfos'))
    area_info_docs = area_info_doc(safe_get(json_data, 'areaInfos'))
    datasource_info_docs = datasource_doc(safe_get(json_data, 'datasourceInfos'))
    return merge_lists(area_function_info_docs, base_area_info_docs, son_area_info_docs,
                       area_info_docs,
                       datasource_info_docs)


def area_info_doc(area_infos: list) -> list[Document]:
    if area_infos is not None:
        return [Document(
            doc_id=f"area_{area_info['id']}",
            text=f"area_id 主领域id: {area_info['id']} - area name 主领域名称: {area_info['areaName']}"
                 f"- area desc 主领域描述: {area_info['desc']} ",
            metadata={"source": "area", "area_id": area_info['id'], "area_name": area_info['areaName']}
        ) for area_info in area_infos]


def datasource_doc(datasource_info: list) -> list[Document]:
    if datasource_info is not None:
        return [Document(
            doc_id=f"datasource_{datasource['id']}",
            text=f"datasource id 数据源id: {datasource['id']} -datasource name 数据源用户: {datasource['name']}"
                 f" -datasource url 数据源连接地址: {datasource['url']} -datasource password 数据源密码: {datasource['password']} -datasource 数据源名称: {datasource['datasource']}",
            metadata={"source": "datasource", "datasource_id": datasource['id'], "datasource_name": datasource['name']}
        ) for datasource in datasource_info]


def area_function_info_doc(area_function_infos: list) -> list[Document]:
    if area_function_infos is not None:
        return [Document(
            doc_id=f"area_function_id{area_function_info['id']}",
            text=f"area_function_id 领域功能id: {area_function_info['id']} - area id 主领域id: {area_function_info['areaId']}"
                 f" - table name 表名称: {area_function_info['tableName']} - datasource name 数据源名称: {area_function_info['datasourceName']} "
                 f"- datasource id 数据源id: {area_function_info['datasourceId']} - areaFunction Class 领域功能的class: {area_function_info['areaFunctionClass']} "
                 f"- areaFunctionParam class 领域功能的入参class: {area_function_info['areaFunctionParamClass']} - areaFunctionResult class 领域功能的返回参数class: {area_function_info['areaFunctionResultClass']} "
                 f"- base_area_pom version 子域的版本: {area_function_info['baseVersion']} - area_function status 领域功能状态: {area_function_info['status']} "
                 f"- area_function version 领域功能版本: {area_function_info['version']} - function name 功能名称: {area_function_info['functionName']} "
                 f"- function desc 功能描述: {area_function_info['functionDesc']} - function_pom groupId 领域功能更的groupId: {area_function_info['groupId']} "
                 f"- function_pom artifactId 领域功能的artifactId: {area_function_info['artifactId']} ",

            metadata={"source": "area_function", "area_function_id": area_function_info['areaFunctionId'],
                      "datasource_name": area_function_info['datasourceName'],
                      "table_name": area_function_info['tableName'],
                      "datasource_id": area_function_info['datasourceId']}
        ) for area_function_info in area_function_infos
        ]


def base_area_info_doc(base_infos: list) -> list[Document]:
    if base_infos is not None:
        return [
            Document(
                doc_id=f"base_area_info_{base_info['id']}",
                text=f"base_area id 子域基础信息id: {base_info['id']} - datasource id 数据源id: {base_info['datasourceId']} - datasource name 数据源名称: {base_info['datasourceName']} "
                     f"- table name 表名称: {base_info['tableName']} - sonArea_name 子域名称: {base_info['sonAreaName']} - domain_object_entity_filed 子域对象实体类的字段: {base_info['domainObject']} "
                     f"- domainObject package 子域基础对象的包: {base_info['domainObjectPackage']} - domainObjectEntity name 子域基础对象类名: {base_info['domainObjectEntityName']} "
                     f"- domainObjectService name 子域基础对象的service名称: {base_info['domainObjectServiceName']} - domainObjectService package 子域基础对象的service的包名: {base_info['domainObjectServicePackage']} "
                     f"- domainObjectServiceImpl name 子域基础对象的service实现类名称: {base_info['domainObjectServiceImplName']} - domainObjectServiceImpl package 子域基础对象的service实现类包名: {base_info['domainObjectServiceImplPackage']} "
                     f" - base_area_pom version : {base_info['version']}  - base_area_pom groupId : {base_info['groupId']} - base_area_pom artifactId : {base_info['artifactId']} - area_id 领域id: {base_info['areaId']} - area_name 领域名称: {base_info['areaName']}",
                metadata={"source": "base_area_info", "table_name": base_info['tableName'],
                          "sonArea_name": base_info['sonAreaName']}
            )
            for base_info in base_infos
        ]


def son_area_info_doc(son_areas: list) -> list[Document]:
    if son_areas is not None:
        return [Document(
            doc_id=f"son_area_{son_area['id']}",
            text=f"son_area_id 子域id: {son_area['id']} - area id 领域id: {son_area['areaId']} - area name 领域名称: {son_area['areaName']} - sonArea name 子域名称: {son_area['sonAreaName']}"
                 f" - table name 表名称: {son_area['tableName']} - datasource name 数据源名称: {son_area['datasource']} ",

            metadata={"source": "son_area", "table_name": son_area['tableName'], "son_area_id": son_area['id'],
                      "son_area_name": son_area['sonAreaName'], "datasource_name": son_area['datasource']}
        )
            for son_area in son_areas
        ]


def init_local_doc() -> list[Document]:
    return [Document(
        doc_id=f"spider_test_{1}",
        text=f"spider_test ID: {1}",

        metadata={"source": "spider_test"}
    )]


def merge_lists(*lists):
    result = []
    for lst in lists:
        if lst is not None and len(lst) > 0:
            result.extend(lst)
    return result


def safe_get(data, key):
    return data.get(key, []) if isinstance(data, dict) else None
