package com.xueye.xueyeWarn.bean;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("student")
public class Student {
    @TableId(type = IdType.AUTO)
    private Integer id;
    private String studentId;  // 学号
    private String name;       // 姓名
    private String gender;     // 性别
    private String major;      // 专业
    private Double grade;      // 平均绩点
    private String warningLevel; // 预警等级（normal/warning/serious）

    @TableField(exist = false)
    private String warningReason;

    @TableField(exist = false)
    private String suggestedActions;


}
