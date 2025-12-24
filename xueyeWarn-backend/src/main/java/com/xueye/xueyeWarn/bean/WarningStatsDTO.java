package com.xueye.xueyeWarn.bean;

import lombok.Data;

// 封装预警等级统计数据
@Data
public class WarningStatsDTO {
    private String warningLevel;
    private Integer count;
    private String major;
    private Double avgGrade;
}