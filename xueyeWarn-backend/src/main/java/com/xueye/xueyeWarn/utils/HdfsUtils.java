package com.xueye.xueyeWarn.utils;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

public class HdfsUtils {
    // HDFS地址（虚拟机IP + RPC端口）
    private static final String HDFS_URI = "hdfs://192.168.10.100:8020";
    // HDFS用户名
    private static final String HDFS_USER = "root";

    static {
        try {
            String hadoopHome = System.getProperty("user.dir");
            System.out.println("Hadoop home: " + hadoopHome);
            System.setProperty("hadoop.home.dir", hadoopHome);
            String binPath = hadoopHome + File.separator + "bin";
            System.out.println("Bin path: " + binPath);
            
            System.out.println("Loading hadoop.dll from: " + binPath + File.separator + "hadoop.dll");
            System.load(binPath + File.separator + "hadoop.dll");
            System.out.println("Hadoop本地库加载成功");
            
            System.out.println("Setting java.library.path to: " + binPath);
            System.setProperty("java.library.path", binPath);
            
            System.out.println("重新加载本地库以确保java.library.path生效");
            try {
                System.loadLibrary("hadoop");
                System.out.println("通过System.loadLibrary重新加载hadoop库成功");
            } catch (UnsatisfiedLinkError e) {
                System.out.println("通过System.loadLibrary加载失败（这是正常的，因为已经加载过了）: " + e.getMessage());
            }
        } catch (UnsatisfiedLinkError e) {
            System.err.println("无法加载Hadoop本地库: " + e.getMessage());
            e.printStackTrace();
        }
    }

    // 获取HDFS文件系统
    public static FileSystem getFileSystem() throws URISyntaxException, IOException, InterruptedException {
        Configuration conf = new Configuration();
        return FileSystem.get(new URI(HDFS_URI), conf, HDFS_USER);
    }

    // 上传文件到HDFS
    public static void upload(String localPath, String hdfsPath) throws Exception {
        FileSystem fs = getFileSystem();
        fs.copyFromLocalFile(new Path(localPath), new Path(hdfsPath));
        fs.close();
    }

    // 从HDFS下载文件
    public static void download(String hdfsPath, String localPath) throws Exception {
        FileSystem fs = getFileSystem();
        fs.copyToLocalFile(new Path(hdfsPath), new Path(localPath));
        fs.close();
    }
}