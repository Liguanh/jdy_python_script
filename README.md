### 功能简介
> 本功能是用户九斗鱼非存管平台的脚本，用于将给定的execl文件的内容导入核心库core_user,core_auth_card,core_bank_card表中，
导入的内容的为平台的借款人信息：［姓名、身份证号、手机号、银行卡号］

> 相关配置

- config 配置区分生产环境和开发环境 [APP_ENV]
- config 配置了数据库的信息core,module
- config 配置了cardbin信息，用来获取bank_id信息
- config 配置获取bank_id的方法 1、Db[数据库读取 module_bank_cardbin]  Url[请求九斗鱼接口获取返回数据] ，经测试100条数据，Db比后者快近20倍

> 录入失败的数据会导入到storage的execl文件中，并记录失败的原因

> 本地测试录入信息[读取bank_id信息为Db方式]所需时长大概为512秒左右，录入数据成功大概为34152条，失败大概3014条

> 添加查询用户先锋充值记录并更新用户订单的脚本[2018年04月23号]

### 环境要求
*python版本及用到的模块库*
- python3
- xlrd,xlwt
- argparse
- urllib
- pymysql
- yaml
- hashlib
- json


### 命令行简介

- 帮助命令

```
python app.py --help
```

- 执行脚本的命令

```
python app.py --user import_loan_user --file filename  
#import_loan_user 要执行的文件的属性方法参数
#filename 上要解析的文件的名字参数，文件存放在storage目录下 
```

- 执行处理先锋充值订单命令

```
python app.py --order record_ucf_recharge
处理先锋充值最新订单，更新用户充值卡表的记录
```
