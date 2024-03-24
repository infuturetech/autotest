# autotest
## 智能盒子自动化测试仓库
[1] 安装Python3.7.4
[2] pip3 install -r requirements.txt 安装依赖库
[3] 安装JDK + allure  根据操作系统自行完成
[4] 执行 case:
pytest -ra -v --alluredir=D:\projects\ats\log_report\001 D:\projects\ats\test_cases
注: test_cases目录按实际修改；

[5] 生成报告
allure generate -c -o   D:\projects\ats\log_report\allure   D:\projects\ats\log_report\001
注: 路径1为生成的报告目录  2为步骤4输出

[6] allure open  D:\projects\ats\log_report\allure 打开测试报告
