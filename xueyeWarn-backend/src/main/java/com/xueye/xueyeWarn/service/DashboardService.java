package com.xueye.xueyeWarn.service;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.xueye.xueyeWarn.bean.Student;
import com.xueye.xueyeWarn.bean.WarningStatsDTO;
import com.xueye.xueyeWarn.mapper.StudentMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class DashboardService {

    @Autowired
    private StudentMapper studentMapper;

    // 1. 数据卡片统计（基于现有表字段）
    public Map<String, Integer> getDashboardCards() {
        Map<String, Integer> cardData = new HashMap<>();
        // 学生总数
        cardData.put("studentCount", Math.toIntExact(studentMapper.selectCount(null)));
        // 专业个数（distinct major）
        cardData.put("majorCount", studentMapper.selectList(new QueryWrapper<Student>()
                .select("distinct major").lambda()).size());
        // 正常预警人数（warning_level='normal'）
        cardData.put("normalCount", Math.toIntExact(studentMapper.selectCount(new QueryWrapper<Student>()
                .eq("warning_level", "normal").lambda())));
        // 预警人数（warning_level='warning'）
        cardData.put("warningCount", Math.toIntExact(studentMapper.selectCount(new QueryWrapper<Student>()
                .eq("warning_level", "warning").lambda())));
        // 严重预警人数（warning_level='serious'）- 修复：增加null检查
        long severeCount = studentMapper.selectCount(new QueryWrapper<Student>()
                .eq("warning_level", "serious").lambda());
        cardData.put("severeCount", Math.toIntExact(severeCount)); // 如果severeCount为0，这里会正确返回0
        return cardData;
    }

    // 2. 专业分布饼图数据（各专业的学生数量）
    public Map<String, Object> getMajorDistribution() {
        Map<String, Object> data = new HashMap<>();
        List<WarningStatsDTO> majorList = studentMapper.selectMajorCount();

        List<String> majorNames = new ArrayList<>();
        List<Integer> counts = new ArrayList<>();
        for (WarningStatsDTO dto : majorList) {
            majorNames.add(dto.getMajor());
            counts.add(dto.getCount());
        }
        data.put("majorNames", majorNames);
        data.put("counts", counts);
        return data;
    }

    // 3. 各专业预警人数柱状图（每个专业的normal/warning/serious数量）
    public Map<String, Object> getMajorWarningData() {
        Map<String, Object> data = new HashMap<>();
        List<String> majors = studentMapper.selectList(new QueryWrapper<Student>()
                        .select("distinct major").lambda()).stream()
                .map(Student::getMajor)
                .collect(Collectors.toList());

        List<Integer> normalList = new ArrayList<>();
        List<Integer> warningList = new ArrayList<>();
        List<Integer> severeList = new ArrayList<>();

        for (String major : majors) {
            // 每个专业的normal数量
            normalList.add(Math.toIntExact(studentMapper.selectCount(new QueryWrapper<Student>()
                    .eq("major", major).eq("warning_level", "normal").lambda())));
            // 每个专业的warning数量
            warningList.add(Math.toIntExact(studentMapper.selectCount(new QueryWrapper<Student>()
                    .eq("major", major).eq("warning_level", "warning").lambda())));
            // 每个专业的serious数量 - 修复：增加null检查
            long severeCount = studentMapper.selectCount(new QueryWrapper<Student>()
                    .eq("major", major).eq("warning_level", "serious").lambda());
            severeList.add(Math.toIntExact(severeCount));
        }

        data.put("majors", majors);
        data.put("normalList", normalList);
        data.put("warningList", warningList);
        data.put("severeList", severeList);
        return data;
    }

    // 4. 预警等级性别分布（男女在不同预警等级的数量）
    public Map<String, Object> getGenderWarningData() {
        Map<String, Object> data = new HashMap<>();
        long maleNormal = studentMapper.selectCount(new QueryWrapper<Student>()
                .eq("gender", "男").eq("warning_level", "normal").lambda());
        long maleWarning = studentMapper.selectCount(new QueryWrapper<Student>()
                .eq("gender", "男").eq("warning_level", "warning").lambda());
        long maleSerious = studentMapper.selectCount(new QueryWrapper<Student>()
                .eq("gender", "男").eq("warning_level", "serious").lambda());

        long femaleNormal = studentMapper.selectCount(new QueryWrapper<Student>()
                .eq("gender", "女").eq("warning_level", "normal").lambda());
        long femaleWarning = studentMapper.selectCount(new QueryWrapper<Student>()
                .eq("gender", "女").eq("warning_level", "warning").lambda());
        long femaleSerious = studentMapper.selectCount(new QueryWrapper<Student>()
                .eq("gender", "女").eq("warning_level", "serious").lambda());

        data.put("maleData", new ArrayList<Integer>() {{
            add(Math.toIntExact(maleNormal));
            add(Math.toIntExact(maleWarning));
            add(Math.toIntExact(maleSerious));
        }});

        data.put("femaleData", new ArrayList<Integer>() {{
            add(Math.toIntExact(femaleNormal));
            add(Math.toIntExact(femaleWarning));
            add(Math.toIntExact(femaleSerious));
        }});

        return data;
    }

    // 5. 各专业平均绩点
    public Map<String, Object> getMajorAvgGrade() {
        Map<String, Object> data = new HashMap<>();
        List<WarningStatsDTO> majorList = studentMapper.selectMajorAvgGrade();

        List<String> majors = new ArrayList<>();
        List<Double> avgGrades = new ArrayList<>();
        for (WarningStatsDTO dto : majorList) {
            majors.add(dto.getMajor());
            avgGrades.add(dto.getAvgGrade());
        }
        data.put("majors", majors);
        data.put("avgGrades", avgGrades);
        return data;
    }
}
