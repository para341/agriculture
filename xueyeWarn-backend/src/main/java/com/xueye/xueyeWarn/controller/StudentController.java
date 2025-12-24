package com.xueye.xueyeWarn.controller;
import com.xueye.xueyeWarn.bean.Result;
import com.xueye.xueyeWarn.bean.Student;
import com.xueye.xueyeWarn.bean.StudentExcel;
import com.xueye.xueyeWarn.bean.WarningStatsDTO;
import com.xueye.xueyeWarn.service.StudentService;
import com.xueye.xueyeWarn.util.ExcelUtil;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.servlet.http.HttpServletResponse;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/student")
public class StudentController {

    private static final Logger log = LoggerFactory.getLogger(StudentController.class);

    @Autowired
    private StudentService studentService;

    // 查询所有学生（修复版）
    @GetMapping("/list")
    public Result<List<Student>> getAllStudents() {
        try {
            log.info("收到获取所有学生的请求");
            List<Student> students = studentService.getAllStudents();
            log.info("返回学生数据，数量: {}", students.size());
            return Result.success(students);
        } catch (Exception e) {
            log.error("获取学生列表失败", e);
            return Result.fail("获取学生列表失败: " + e.getMessage());
        }
    }

    // 根据ID查询学生
    @GetMapping("/{id}")
    public Result<Student> getStudentById(@PathVariable Integer id) {
        try {
            Student student = studentService.getStudentById(id);
            return Result.success(student);
        } catch (Exception e) {
            log.error("根据ID查询学生失败", e);
            return Result.fail("查询学生失败: " + e.getMessage());
        }
    }

    // 添加学生
    @PostMapping("/add")
    public Result<Integer> addStudent(@RequestBody Student student) {
        try {
            int rows = studentService.addStudent(student);
            return Result.success(rows);
        } catch (Exception e) {
            log.error("添加学生失败", e);
            return Result.fail("添加学生失败: " + e.getMessage());
        }
    }

    // 修改学生
    @PutMapping("/update")
    public Result<Integer> updateStudent(@RequestBody Student student) {
        try {
            int rows = studentService.updateStudent(student);
            return Result.success(rows);
        } catch (Exception e) {
            log.error("修改学生失败", e);
            return Result.fail("修改学生失败: " + e.getMessage());
        }
    }


    // 删除学生
    @DeleteMapping("/delete/{id}")
    public Result<Integer> deleteStudent(@PathVariable Integer id) {
        try {
            int rows = studentService.deleteStudent(id);
            return Result.success(rows);
        } catch (Exception e) {
            log.error("删除学生失败", e);
            return Result.fail("删除学生失败: " + e.getMessage());
        }
    }

    // 预警统计
    @GetMapping("/stats")
    public Result<List<WarningStatsDTO>> getWarningStats() {
        try {
            List<WarningStatsDTO> stats = studentService.getWarningStats();
            return Result.success(stats);
        } catch (Exception e) {
            log.error("获取预警统计失败", e);
            return Result.fail("获取预警统计失败: " + e.getMessage());
        }
    }


    // 查询学生预警状态
    @GetMapping("/warning-status")
    public Result<Student> getStudentWarningStatus(
            @RequestParam(required = false) String studentId,
            @RequestParam(required = false) String name) {
        Student student = studentService.getStudentByNumberOrName(studentId, name);
        return Result.success(student);
    }

    @GetMapping("/export")
    public void exportStudentExcel(HttpServletResponse response) {
        try {
            List<Student> students = studentService.getAllStudents();
            List<StudentExcel> excelList = students.stream().map(student -> {
                StudentExcel excel = new StudentExcel();
                BeanUtils.copyProperties(student, excel);
                return excel;
            }).collect(Collectors.toList());
            ExcelUtil.export(response, "学生信息", StudentExcel.class, excelList);
        } catch (Exception e) {
            log.error("导出学生信息Excel失败", e);
            throw new RuntimeException("导出学生信息Excel失败: " + e.getMessage());
        }
    }
}
