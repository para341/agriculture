package com.xueye.xueyeWarn.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.xueye.xueyeWarn.bean.Student;
import com.xueye.xueyeWarn.bean.WarningStatsDTO; // 导入你的DTO
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface StudentMapper extends BaseMapper<Student> {

    @Select("SELECT major, COUNT(*) AS count FROM student GROUP BY major")
    List<WarningStatsDTO> selectMajorCount();

    @Select("SELECT major, AVG(grade) AS avgGrade FROM student GROUP BY major")
    List<WarningStatsDTO> selectMajorAvgGrade();
}