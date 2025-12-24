package com.xueye.xueyeWarn.bean;

import com.alibaba.excel.annotation.ExcelProperty;
import com.alibaba.excel.annotation.write.style.ColumnWidth;
import com.alibaba.excel.annotation.write.style.ContentRowHeight;
import com.alibaba.excel.annotation.write.style.HeadRowHeight;
import lombok.Data;

@Data
@HeadRowHeight(20)
@ContentRowHeight(18)
public class StudentExcel {
    @ExcelProperty(value = "学号", index = 0)
    @ColumnWidth(15)
    private String studentId;

    @ExcelProperty(value = "姓名", index = 1)
    @ColumnWidth(12)
    private String name;

    @ExcelProperty(value = "性别", index = 2)
    @ColumnWidth(8)
    private String gender;

    @ExcelProperty(value = "专业", index = 3)
    @ColumnWidth(20)
    private String major;

    @ExcelProperty(value = "平均绩点", index = 4)
    @ColumnWidth(12)
    private Double grade;

    @ExcelProperty(value = "预警等级", index = 5)
    @ColumnWidth(12)
    private String warningLevel;
}
