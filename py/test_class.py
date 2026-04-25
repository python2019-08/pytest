"""
这段代码清晰地展示了 类属性（Class Attributes） 的三种操作方式：通过 self.__class__、通过 @classmethod 以及通过类名直接访问。

以下是代码运行逻辑的详细拆解：
## 1. 核心行为分析
在你的代码中，完全没有定义实例属性（因为 self.name = n 等行被注释掉了）。所有的读写都在操作“类”这一层级。

* 初始化阶段 (__init__)：
    当你创建 p1 时，self.__class__.name = "class name" 强制修改了类的公共属性。此时，类层面的 name 从 '' 变成了 "class name"。
* 方法修改阶段 (changeClsVars)：
    这是修改类属性的标准做法。使用 cls.name 再次覆盖了之前的修改，将其变更为 "class name33"。
* 读取阶段 (speak)：
    由于实例 p1 内部没有 name 和 age（p1.__dict__ 是空的），Python 会向上查找，去类里寻找这些变量。

## 2. 运行结果解析

CPeople.age= 100 .....CPeople.name= class name    # 由 p1 的 __init__ 修改
changeClsVars                                     # 执行了类方法
class name33 说: 我 300 岁。                      # p1 读取的是类最新的值
CPeople.age= 300 .....CPeople.name= class name33  # 类属性已被永久改变
class name33 说: 我 300 岁。                      # 再次读取

## 3. 关于 __weight 的特殊陷阱
这里有一个非常隐蔽的 Bug：

* 在 __init__ 中，你写的是 self.__class__.__weight = "..."。由于是在方法内部写的，Python 不会对这里的双下划线进行名称修饰。它真的在类里创建了一个名为 __weight 的新变量。
* 而在类定义开头定义的 __weight = "ddd"，被 Python 自动改名成了 _CPeople__weight。
* 结果：你的类里现在同时存在 _CPeople__weight（原始的）和 __weight（你手动创建的）。

## 4. 总结与建议

| 方式 | 评价 | 影响范围 |
|---|---|---|
| self.__class__.xxx | 不推荐 | 修改类属性，影响所有实例。容易让代码逻辑变混乱。 |
| @classmethod | 推荐 | 修改类属性的标准姿势，语义清晰。 |
| CPeople.xxx | 可用 | 在类外部修改类属性的直接方式。 |

关键结论：在没有实例属性的情况下，所有实例都像“共享文件夹”一样共用类属性。一旦类属性改变，所有实例看到的值都会同步更新。
你想看看如何在这种结构下引入实例属性来遮蔽（Shadow）这些类属性吗？
"""

class CPeople:
    #定义基本属性
    name = ''
    age = 0
    #定义私有属性,私有属性在类外部无法直接进行访问
    __weight = "ddd"
    #定义构造方法
    def __init__(self,n,a,w):
        # self.name = n
        # self.age = a
        # self.weight = w

        # 类属性赋值
        self.__class__.__weight = "class weight"
        self.__class__.name = "class name"
        self.__class__.age = 100 

    def speak(self):
        # 类属性读取
        print("%s 说: 我 %d 岁。" %(self.name,self.age))
    
    @classmethod
    def changeClsVars(cls):
        # 类属性赋值
        cls.name = "class name33"
        cls.age = 300   
        cls.__weight = "class weight 33"
        print("changeClsVars")
 
# 实例化类
p1 = CPeople('runoob',10,30)
print( "CPeople.age=",CPeople.age,".....CPeople.name=",CPeople.name)
CPeople.changeClsVars()
p1.speak()
print( "CPeople.age=",CPeople.age,".....CPeople.name=",CPeople.name)
p1.speak()