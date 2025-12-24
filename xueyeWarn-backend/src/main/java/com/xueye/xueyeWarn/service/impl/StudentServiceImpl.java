package com.xueye.xueyeWarn.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.xueye.xueyeWarn.bean.Student;
import com.xueye.xueyeWarn.bean.WarningStatsDTO;
import com.xueye.xueyeWarn.mapper.StudentMapper;
import com.xueye.xueyeWarn.service.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class StudentServiceImpl implements StudentService {

    private static final Logger log = LoggerFactory.getLogger(StudentServiceImpl.class);

    @Autowired
    private StudentMapper studentMapper;

    // 简化缓存机制
    private List<Student> cachedStudentList = null;
    private long lastUpdateTime = 0;
    private static final long CACHE_DURATION = 5 * 60 * 1000; // 5分钟缓存

    // 查询所有学生（修复版）
    @Override
    public List<Student> getAllStudents() {
        try {
            long currentTime = System.currentTimeMillis();

            // 如果缓存存在且未过期，直接返回
            if (cachedStudentList != null && (currentTime - lastUpdateTime) < CACHE_DURATION) {
                log.info("使用缓存数据，数量: {}", cachedStudentList.size());
                return cachedStudentList;
            }

            // 否则查询数据库并更新缓存
            log.info("从数据库查询学生数据...");
            cachedStudentList = studentMapper.selectList(null);
            lastUpdateTime = currentTime;

            if (cachedStudentList == null) {
                cachedStudentList = new ArrayList<>();
            }

            // 遍历学生列表，动态设置预警信息
            cachedStudentList.forEach(this::setStudentWarningInfo);

            log.info("数据库查询完成，数据量: {}", cachedStudentList.size());
            return cachedStudentList;
        } catch (Exception e) {
            log.error("查询学生数据失败", e);
            return new ArrayList<>();
        }
    }

    @Override
    public Student getStudentById(Integer id) {
        Student student = studentMapper.selectById(id);
        if (student != null) {
            setStudentWarningInfo(student);
        }
        return student;
    }

    // 新增：根据学号查询学生
    @Override
    public Student getStudentByNumber(String studentId) {
        LambdaQueryWrapper<Student> queryWrapper = new LambdaQueryWrapper<>();
        queryWrapper.eq(Student::getStudentId, studentId);
        Student student = studentMapper.selectOne(queryWrapper);
        if (student != null) {
            setStudentWarningInfo(student);
        }
        return student;
    }

    // 新增：根据姓名查询学生
    @Override
    public Student getStudentByName(String name) {
        LambdaQueryWrapper<Student> queryWrapper = new LambdaQueryWrapper<>();
        queryWrapper.eq(Student::getName, name);
        Student student = studentMapper.selectOne(queryWrapper);
        if (student != null) {
            setStudentWarningInfo(student);
        }
        return student;
    }

    // 新增：根据学号或姓名查询学生（主要查询方法）
    @Override
    public Student getStudentByNumberOrName(String studentId, String name) {
        if (studentId != null && !studentId.isEmpty()) {
            return getStudentByNumber(studentId);
        } else if (name != null && !name.isEmpty()) {
            return getStudentByName(name);
        }
        return null;
    }

    // 新增：获取学生预警状态（包含详细信息和建议）
    @Override
    public Student getStudentWarningStatus(String studentId) {
        Student student = getStudentByNumber(studentId);
        if (student != null) {
            setStudentWarningInfo(student);
        }
        return student;
    }

    // 添加学生（清除缓存）
    @Override
    public int addStudent(Student student) {
        try {
            int result = studentMapper.insert(student);
            clearCache();
            log.info("添加学生成功，ID: {}", student.getId());
            return result;
        } catch (Exception e) {
            log.error("添加学生失败", e);
            return 0;
        }
    }

    // 修改学生（清除缓存）
    @Override
    public int updateStudent(Student student) {
        try {
            int result = studentMapper.updateById(student);
            clearCache();
            log.info("修改学生成功，ID: {}", student.getId());
            return result;
        } catch (Exception e) {
            log.error("修改学生失败", e);
            return 0;
        }
    }

    // 删除学生（清除缓存）
    @Override
    public int deleteStudent(Integer id) {
        try {
            int result = studentMapper.deleteById(id);
            clearCache();
            log.info("删除学生成功，ID: {}", id);
            return result;
        } catch (Exception e) {
            log.error("删除学生失败", e);
            return 0;
        }
    }

    // 清除缓存方法
    private void clearCache() {
        cachedStudentList = null;
        log.info("缓存已清除");
    }

    // 辅助方法：根据预警等级设置详细信息和建议
    private void setStudentWarningInfo(Student student) {
        switch (student.getWarningLevel()) {
            case "serious":
                student.setWarningReason("学业成绩严重不达标，可能影响毕业");
                student.setSuggestedActions("立即联系辅导员，制定学习计划");
                break;
            case "warning":
                student.setWarningReason("学业成绩接近预警线，需要关注");
                student.setSuggestedActions("调整学习方法，加强课程学习");
                break;
            default:
                student.setWarningReason("学业状态正常");
                student.setSuggestedActions("继续保持良好学习状态");
        }
    }

    @Override
    public List<WarningStatsDTO> getWarningStats() {
        try {
            List<Student> studentList = getAllStudents();

            Map<String, Long> levelCountMap = studentList.stream()
                    .collect(Collectors.groupingBy(
                            Student::getWarningLevel,
                            Collectors.counting()
                    ));

            List<WarningStatsDTO> statsList = new ArrayList<>();
            String[] levels = {"normal", "warning", "serious"};
            for (String level : levels) {
                WarningStatsDTO dto = new WarningStatsDTO();
                dto.setWarningLevel(level);
                dto.setCount(levelCountMap.getOrDefault(level, 0L).intValue());
                statsList.add(dto);
            }

            return statsList;
        } catch (Exception e) {
            log.error("获取预警统计失败", e);
            return new ArrayList<>();
        }
    }
}
