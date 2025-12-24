package com.xueye.xueyeWarn.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.xueye.xueyeWarn.bean.User;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface UserMapper extends BaseMapper<User> {
    User getUserByUsername(String username);
}