package com.xueye.xueyeWarn.controller;

import com.xueye.xueyeWarn.bean.Result;
import com.xueye.xueyeWarn.utils.HdfsUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletResponse;
import java.io.File;
import java.io.FileInputStream;
import java.io.OutputStream;
import java.net.URLEncoder;
import java.io.IOException;

@RestController
@RequestMapping("/hadoop")
public class HadoopController {

    private static final String TEMP_DIR = System.getProperty("user.dir") + File.separator + "temp";

    // 文件上传到HDFS
    @PostMapping("/upload")
    public Result<String> upload(@RequestParam("file") MultipartFile file) {
        try {
            // 1. 临时保存文件到本地
            File tempDir = new File(TEMP_DIR);
            if (!tempDir.exists()) {
                tempDir.mkdirs();
            }
            String localPath = TEMP_DIR + File.separator + file.getOriginalFilename();
            File tempFile = new File(localPath);
            file.transferTo(tempFile);

            // 2. 上传到HDFS
            String hdfsPath = "/xueye_warn/" + file.getOriginalFilename();
            HdfsUtils.upload(localPath, hdfsPath);

            // 3. 删除本地临时文件
            tempFile.delete();

            return Result.success("文件上传到HDFS成功：" + hdfsPath);
        } catch (Exception e) {
            e.printStackTrace();
            return Result.fail("上传失败：" + e.getMessage());
        }
    }

    // 从HDFS下载文件
    @GetMapping("/download")
    public void download(@RequestParam String fileName, HttpServletResponse response) {
        try {
            // 1. HDFS文件路径
            String hdfsPath = "/xueye_warn/" + fileName;
            // 2. 本地临时路径
            File tempDir = new File(TEMP_DIR);
            if (!tempDir.exists()) {
                tempDir.mkdirs();
            }
            String localPath = TEMP_DIR + File.separator + fileName;
            // 3. 从HDFS下载到本地
            HdfsUtils.download(hdfsPath, localPath);

            // 4. 响应给前端
            File file = new File(localPath);
            response.setContentType("application/octet-stream");
            response.setHeader("Content-Disposition", "attachment; filename=" + URLEncoder.encode(fileName, "UTF-8"));
            OutputStream os = response.getOutputStream();
            FileInputStream fis = new FileInputStream(file);
            byte[] buffer = new byte[1024];
            int len;
            while ((len = fis.read(buffer)) != -1) {
                os.write(buffer, 0, len);
            }
            fis.close();
            os.close();

            // 5. 删除本地临时文件
            file.delete();
        } catch (IOException e) {
            try {
                response.setStatus(500);
                response.setContentType("application/json;charset=UTF-8");
                response.getWriter().write("{\"code\":500,\"msg\":\"下载失败：" + e.getMessage() + "\"}");
            } catch (IOException ex) {
                ex.printStackTrace();
            }
            e.printStackTrace();
        } catch (Exception e) {
            try {
                response.setStatus(500);
                response.setContentType("application/json;charset=UTF-8");
                response.getWriter().write("{\"code\":500,\"msg\":\"下载失败：" + e.getMessage() + "\"}");
            } catch (IOException ex) {
                ex.printStackTrace();
            }
            e.printStackTrace();
        }
    }
}