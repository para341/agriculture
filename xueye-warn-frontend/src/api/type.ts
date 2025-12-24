// @/api/types.ts

/**
 * 后端统一响应格式（对应 Java 的 Result<T> 类）
 */
export interface ApiResponse<T> {
    code: number; // 状态码：200成功，500失败
    msg: string;  // 提示信息
    data: T;      // 业务数据
}

/**
 * 学生实体（对应 Java 的 Student 类）
 */
export interface Student {
    id?: number;         // 主键（新增时可不传，后端自增）
    studentId: string;   // 学号（对应数据库 student_id）
    name: string;        // 姓名
    gender: string;      // 性别
    major: string;       // 专业
    grade?: number;      // 平均绩点
    warningLevel: string; // 预警等级（normal/warning/serious）
}

/**
 * 用户实体（对应 Java 的 User 类）
 */
export interface User {
    id?: number;     // 主键ID
    username: string; // 用户名
    password: string; // 密码
    role: string;     // 角色（admin/student）
}

/**
 * 分页响应数据结构（用于分页查询）
 */
export interface PageResponse<T> {
    records: T[];   // 当前页数据列表
    total: number;  // 总条数
    size: number;   // 每页条数
    current: number; // 当前页码
}

/**
 * 预警统计DTO（对应 Java 的 WarningStatsDTO）
 */
export interface WarningStatsDTO {
    warningLevel?: string; // 预警等级
    count?: number;        // 统计数量
    major?: string;        // 专业（用于专业统计）
}
