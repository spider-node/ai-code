goods_info_config = """
@Getter
@Setter
@TableName("spider_area")
public class SpiderArea implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * id
     */
    @TableId("id")
    private String id;

    /**
     * 领域名称
     */
    @TableField("area_name")
    private String areaName;

    /**
     * 领域描述
     */
    @TableField("desc")
    private String desc;

    /**
     * 领域sdk
     */
    @TableField("sdk_url")
    private String sdkUrl;

    /**
     * 扫描类路径
     */
    @TableField("scan_class_path")
    private String scanClassPath;

    /**
     * sdk的名称
     */
    @TableField("sdk_name")
    private String sdkName;

    /**
     * sdk状态
     */
    @TableField("sdk_status")
    private String sdkStatus;

    /**
     * 创建时间
     */
    @TableField("create_time")
    private LocalDateTime createTime;
}
"""

domain_object_package = "package cn.spider.spider.spider.area.base.entity"

domain_object_entity_name = "SpiderArea"

domain_object_service_name = "SpiderAreaService"

domain_object_service_package = "package cn.spider.spider.spider.area.base.service"

domain_object_service_impl_name = "SpiderAreaServiceImpl"

domain_object_service_impl_package = "package cn.spider.spider.spider.area.base.service.impl"

domain_info = {"domain_info": {"domain_object": goods_info_config, "domain_object_package": domain_object_package,
                               "domain_object_entity_name": domain_object_entity_name,
                               "domain_object_service_name": domain_object_service_name,
                               "domain_object_service_package": domain_object_service_package,
                               "domain_object_service_impl_name": domain_object_service_impl_name,
                               "domain_object_service_impl_package": domain_object_service_impl_package,
                               "groupId": "cn.spider",
                               "tableName": "spider_area",
                               "datasource": "spider"
                               }}
