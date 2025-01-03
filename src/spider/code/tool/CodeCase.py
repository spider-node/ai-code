business_code = """
package cn.spider.stock.release.stock.component.spider.service;

import cn.spider.framework.annotation.NoticeScope;
import cn.spider.framework.annotation.TaskComponent;
import cn.spider.framework.annotation.TaskService;
import cn.spider.framework.annotation.enums.ScopeTypeEnum;
import cn.spider.stock.release.stock.component.spider.data.ReleaseStockParam;
import cn.spider.stock.release.stock.component.spider.data.ReleaseStockResult;
import cn.spider.spider.demo.stock.base.entity.Stock;
import cn.spider.spider.demo.stock.base.service.StockService;
import cn.spider.spider.demo.stock.lock.base.entity.StockLock;
import cn.spider.spider.demo.stock.lock.base.service.StockLockService;
import com.alibaba.fastjson.JSON;
import com.alipay.sofa.runtime.api.annotation.SofaService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;

@Slf4j
@TaskComponent(name = "stockService")
@SofaService
@Component
public class ReleaseStockComponent {

    @Autowired
    private StockService stockService;

    @Autowired
    private StockLockService stockLockService;

    /**
     * 释放库存
     *
     * @param param 锁code
     * @return 释放结果
     */
    @NoticeScope(scope = {ScopeTypeEnum.STABLE}, target = "stock")
    @TaskService(name = "releaseStock", functionName = "释放库存", desc = "根据锁code释放库存")
    public ReleaseStockResult releaseStock(ReleaseStockParam param) {
        log.info("releaseStock-param {}", JSON.toJSONString(param));

        // 根据锁code查询锁定库存记录
        StockLock stockLock = stockLockService.lambdaQuery()
                .eq(StockLock::getLockCode, param.getLockCode())
                .one();

        if (stockLock == null) {
            log.warn("No stock lock found with lock code: {}", param.getLockCode());
            return new ReleaseStockResult();
        }

        // 根据库存ID查询库存记录
        Stock stock = stockService.getById(stockLock.getStockId());

        if (stock == null) {
            log.warn("No stock found with ID: {}", stockLock.getStockId());
            return new ReleaseStockResult();
        }

        // 解锁库存数量
        BigDecimal lockedNumber = stockLock.getLockNumber();
        BigDecimal currentLockNumber = stock.getLockNumber();

        if (currentLockNumber.compareTo(lockedNumber) < 0) {
            log.warn("Locked number mismatch for stock ID: {}. Expected: {}, Actual: {}", stock.getId(), lockedNumber, currentLockNumber);
            return new ReleaseStockResult();
        }

        stock.setLockNumber(currentLockNumber.subtract(lockedNumber));
        stockService.updateById(stock);

        // 更新锁定库存记录状态为UNLOCK
        stockLock.setLockStatus("UNLOCK");
        stockLockService.updateById(stockLock);

        // 构建返回结果
        ReleaseStockResult result = new ReleaseStockResult();
        BeanUtils.copyProperties(stock, result);
        return result;
    }
}
"""
input_param_code = """
package cn.spider.stock.release.stock.component.spider.data;

import cn.spider.framework.annotation.StaTaskField;
import lombok.Data;

@Data
public class ReleaseStockParam {

    /**
     * 锁编号
     */
    @StaTaskField("stockLock.lockCode")
    private String lockCode;
}
"""

out_put_param_code = """
package cn.spider.stock.release.stock.component.spider.data;

import cn.spider.framework.annotation.NoticeSta;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
public class ReleaseStockResult {

    /**
     * 商品编号
     */
    @NoticeSta(target = "stock.goodCode")
    private String goodCode;

    /**
     * 商品名称
     */
    @NoticeSta(target = "stock.goodName")
    private String goodName;

    /**
     * 商品数量
     */
    @NoticeSta(target = "stock.goodNumber")
    private BigDecimal goodNumber;

    /**
     * 锁定数量
     */
    @NoticeSta(target = "stock.lockNumber")
    private BigDecimal lockNumber;

    /**
     * 创建时间
     */
    @NoticeSta(target = "stock.createTime")
    private LocalDateTime createTime;

    /**
     * 更新时间
     */
    @NoticeSta(target = "stock.updateTime")
    private LocalDateTime updateTime;
}
"""
