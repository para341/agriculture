package com.xueye.xueyeWarn.service;

import com.xueye.xueyeWarn.bean.Student;
import com.xueye.xueyeWarn.bean.WarningStatsDTO;

import java.util.List;

public interface StudentService {

    List<Student> getAllStudents();

    Student getStudentById(Integer id);

    // 新增方法声明
    Student getStudentByNumber(String studentId);

    Student getStudentByName(String name);

    Student getStudentByNumberOrName(String studentId, String name);

    Student getStudentWarningStatus(String studentId);

    int addStudent(Student student);

    int updateStudent(Student student);

    int deleteStudent(Integer id);

    List<WarningStatsDTO> getWarningStats();
}
