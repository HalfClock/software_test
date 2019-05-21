# 第一节 简介

#### 知识收获
1. 前导性知识
2. TDD的概念，即测试驱动编程（先写测试然后编程）
3. 如何使用selenium对WEB应用进行初步的测试

#### 需要记住的命令

1. django开启一个project

```
django-admin.py startproject superlists
```
2. django开启对应的项目服务

```
python manage.py runserver
```

# 第二节 TDD流程概述及功能测试
#### 知识性收获

1. 功能测试(Functional Test) == 验收测试(Acceptance Test) == 端到端测试(End-to-End Test)==黑盒测试(Black Box Test)
2. **功能测试**：**面向用户的、从外部测试应用程序**，在创建功能测试时应该先编写User Story，然后按照User Story进行开发。
    * Functional tests should help you build an application with the right functionality, and guarantee you never accidentally break it.
3. **单元测试**：**面向编程者、从内部测试应用程序。**
    * Unit tests should help you to write code that’s clean and bug free.
4. TDD测试的工作流程：
 
![TDD测试的工作流程](https://raw.githubusercontent.com/HalfClock/software_test/master/images/TDD1.png)

6. python unittest标准库
    * setUp()
        * 测试之前运行
    * tearDown()
        * 测试之后运行(**即使出现错误**)
    * test_...()
        * 任何以test开头的方法都是测试方法，将由测试器运行
    * assertIn|assertEqual|assertTrue|assertFalse
        * 代替原生的assert语句

6. Django的模式
    1. Django是按照经典的MVC模式构建的、但是它的视图更像是一个控制器
    2. Django的主要工作与别的Web服务器一样，响应用户对网站特定URL的访问
    3. Django工作流程：
        
![Django的模式](https://raw.githubusercontent.com/HalfClock/software_test/master/images/django1.png)

#### 需要记住的代码
   

* Django开始一个app
    * `python manage.py startapp lists`
* unittest类如何使用

```python
from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do',self.browser.title)
        self.fail("Finish the test!")

if __name__ == '__main__':
    unittest.main(warnings='ignore')
```

# 第三节 单元测试
    本节举例如何在Django app中做单元测试，以及用大量例子说明了TDD测试的流程（单元测与功能测之间的关系）、以及单元测试的“满工出细活”本性。
#### 知识性收获

1. 在Django 的app中有一个tests.py，可在其中编写自己的单元测试代码，需要编写继承自django.test包中的TestCase类的自定义类

2. django.urls 包中的 resolve(‘urlname’)用于解析url参数、并返回Django用于解析此url的view对象，view对象在app中的views下定义。

3. resolve('urlname')方法需要URL mapping才能起作用、Django将之放在了project目录下的urls.py中
    1. 当调用resolve('urlname')方法时，系统会自动从mapping中查找。
    2. 需要注意的是，当用户正常访问url的时候，Django也会从mapping中查找对应的view，然后让对应的view去处理请求。
    3. url条目以正则表达式开头，该表达式定义它应用于哪些URL，然后继续说明它应该将这些请求发送到哪里 - 要么是导入的视图**函数**(可调用的python对象)，要么是其他地方的另一个urls.py文件。
        1. 如：`url(r'^$', views.home_page, name='home')`

4. 对比上一小节中的Django工作流程：
    1. HttpRequest()可以返回一个模拟的请求对象。
    2. HttpResponse()可以返回一个响应对象，可以使用该对象定义返回的元素。
    3. Request对象一般会被交给对应的view处理，并返回对应的Response对象。
 

#### 需要记住的

1. git commit -am is the quickest formulation, but also gives you the **least feedback** about what’s being committed, so make sure you’ve done a git status and a git diff beforehand, and are clear on what changes are about to go in.

2. TDD琐碎而繁琐的步骤可以根据情况简化

3. 为什么需要如此琐碎的测试？
    1. Having a test there for a simple function means it’s that much less of a psychological barrier to overcome when the simple function gets a tiny bit more complex—perhaps it grows an if. Then a few weeks later it grows a for loop. Before you know it, it’s a recursive metaclass-based polymorphic tree parser factory. But because it’s had tests from the very beginning, adding a new test each time has felt quite natural, and it’s well tested.
    
    2. 大意：现在做的微小的测试工作能够很好的为将来复杂的函数打好基础，当复杂函数出现问题时，经过如此多的测试，问题可以很快的被解决。

 

# 第四节 完整的TDD流程
    本节在引入了代码重构的基础上，用例子演示了一遍一整个TDD的流程(包括之前没有的代码重构)
#### 知识性收获

1. 单元测试应该是是关于**代码逻辑，数据流控制和配置相关**的测试。不应该用于测试数据内容（NB:HTML便签中的内容）是否正确。

2. **Refactoring(重构)**:当我们尝试去改进代码，而有不改变功能的时候就叫代码重构。
    1. 因为重构不改变代码的功能，所以重构最好是**基于严格测试的**

3. **Django的render函数**
    1. django.shortcut 包中的render(request,'home.html')
    
    2. 参数：请求对象，**要呈现的模板的名称**
    
    3. Django将在您的任何应用程序目录中自动搜索名为templates的文件夹。然后，它会**根据模板的内容** **为您构建一个HttpResponse。**
    
    4. templates是Django的一个非常强大的功能，它们的主要优势在于将Python变量替换为HTML文本

4. 新建了一个app需要在Django中**注册**，否则Django会找不到此APP，包括其中的templates
    1. 在app属于的projects目录的settings.py中的INSTALLED_APPS列表中注册此APP，添加APP的名称。
    2. 代码：`INSTALLED_APPS = [ ... , ... ,'lists']`

5. django.template.loader包中的**render_to_string('home.html')**
    1.此函数将特定的templates直接转化成html内容字符串

6. Django工具包——Django Test Client： 

```python
def test_home_page_return_correct_html(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response,'home.html')
```
```python
def test_home_page_return_correct_html(self):
    request = HttpRequest()
    response = home_page(request)   
    html = response.content.decode('utf8')
    self.assertTrue(html.startswith('<html>'))
    self.assertIn('<title>To-Do lists</title>', html)
    self.assertTrue(html.endswith('</html>'))
```
>**上面的两段代码功能一致**
>assertTemplateUsed直接把模板进行内容上的对比，省去了很多html的内容测试断言
>这符合单元测试的规矩——单元测试应该是是关于**代码逻辑，数据流控制和配置相关**的测试。
>功能一致，但是代码improve了，这就是代码重构

7.增加了代码重构的TDD流程：
![Aaron Swartz](https://raw.githubusercontent.com/HalfClock/software_test/master/images/TDD2.png)

# 第五节 数据库测试前导

#### 知识性收获

1. 当功能测试遇到不可预料的失败时，我们有几种调试方法
    * 添加打印语句，以显示当前页面文本的内容。
    * 改进错误消息以显示有关当前状态的更多信息。
    * 手动访问该网站。
    * **使用time.sleep在执行期间暂停测试。**
    
2. Cross-Site Request Forgery exploit(CSRF) 跨站点请求伪造攻击
    * Django的CSRF保护涉及将一些自动生成的令牌放入每个生成的表单中，以便能够将POST请求识别为来自原始网站。
    * **Django的CSRF令牌设置，在表单标签内部插入** ` {% csrf_token %} `
    * Django在渲染页面时，会使用隐藏的input域来代替CSRF令牌、该隐藏域带有CSRF令牌的信息
    
3. render函数将第三个参数作为一个字典，它将模板中嵌入的变量名称映射到它们的值（自己给的值）：
    * 使用 `使用{{ 变量名 }}` 可以在模板文件中嵌入python变量 `<tr><td>1: {{ new_item_text }}</td></tr>`
    * 示例：
        
        ```python
           render(request, 'home.html', {'new_item_text': request.POST.get('item_text','')})
        ```
4. python 的"f-string"句法
    * 只要在字符串前加f，就可以在字符串中间以{局部变量名}的形式插入局部变量
    * `f"New to-do item did not appear in table. Contents were:\n{table.text}"`
    
5. 红/绿/重构
    * 单元测试的流程有时可以是这样的——红色、绿色、重构
        * 首先编写一个会测试失败的单元测试（红色）。
        * 编写最简单的代码以使其通过（绿色），即使这意味着作弊 "cheat code"。
        * 重构以获得更有意义的更好的代码。
    * 重构即需要将"欺骗测试"的代码转变成令我们真正满意的代码
        * 消除重复（测试代码与程序代码都使用了常量）
        * 进行三角测试(triangulation)，用一般情况来代替特殊情况
        
6. 重构的准则 —— "三振出局"
    * 一旦代码中存在着三次重复、那么重构它
    * 最好的解决方法是、找到一个统一的函数来代替重复代码
    
7. Django ORM

    >对象关系映射器（ORM）是存储在具有表，行和列的数据库中的数据的抽象层。它允许我们使用熟悉的面向对象的隐喻来处理数据库，这些隐喻可以很好地处理代码。

    * 类映射到数据库表
    * 属性映射到列
    * 类的单个实例表示数据库中的一行数据。

8. Django 的 model
    * Django项目需要在models.py 中定义模式用于存储ORM数据库对象。
    * models.py中的model需要继承库中的models.Model，或者类似的类
    * 当修改了model后需要进行**数据库迁移**、以便使得现实的代码改动能够真正的在数据库中进行更改、使用 `python manage.py makemigrations`命令进行数据库迁移。
    * 需要注意的是，一旦继承model，那么就不能通过实例.attrname = value随意给实例创造属性了。因为model类的内部有限制
    
    > 在Django中，ORM的工作是为数据库建模，但是有第二个系统负责实际构建称为迁移的数据库。它的工作是根据对models.py文件所做的更改，使程序员能够添加和删除表和列。
    
9. 数据库测试
    * “真正的”单元测试永远不应该触及数据库
    * 若涉及到数据库测试的单元测应该更恰当地称为集成测试，因为它还依赖于外部系统 - 即数据库。


#### 需要记住的代码

1. 单元测试中，可以使用 `client.post('/', data={'item_text': 'A new list item'})` 来模拟客户端请求，data属性储存的是请求的参数

2. `request.POST`返回的是一个字典对象、该对象可以使用get方法

3. Django的model可以使用save()、count()方法来查询对象的信息，与保存对象(修改)、示例：
   
   ```python
       second_item = Item()
       second_item.text = 'Item the second'
       second_item.save()

       saved_items = Item.objects.all()
       self.assertEqual(saved_items.count(), 2)
    ```

# 第六节 数据库测试

#### 知识性收获
1. 对于任何的request，不要将空的item存储至model中。
    * 所以这样的代码是不应该在view中被发现的：`item.text = request.POST.get('item_text', '')`
2. **最好让单元测试每一次测试一件事情**，所以当一个单元测试过长时，就要考虑将他拆分成多个单元测试了。
3. **俗话说的好，在服务器在响应了POST请求后，最好重定向**。
    * 视图函数有两个工作要完成：*处理用户输入*和*返回适当的响应*。
    * 用户提交post请求大部分都是要将数据存进数据库中。
    * 有了更新后的数据库，我们就可以使用get去刷新有着新数据的新页面了。
    * 所以我们应该从定向去执行get请求而不是将处理后的数据返回(如果get请求无法呈现数据库中的数据，而是必须用请求返回的数据渲染页面，那么这个应用就太笨拙了)。
4. **Setup，Exercise，Assert是单元测试的典型结构。**
    * 经典的单元测试由三部分构成
    * Setup：设置数据项、或者建立要测试的数据
    * Exercise：处理这些数据
    * Assert：**判断处理结果是否符合预期**
    * 例子：

```python
    def test_displays_all_list_items(self):

        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())
```
5. 通过migrate创建我们的生产数据库。
    *  **单元测试的数据库会在测试过后删除**、与实际应用、功能测试中不同。
    *  单元测试中每一个以“test_”开头的函数都会**清空数据库、从新开始。**
    *  **单元测试用的迁移数据库命令和功能测试与实际生产中数据库迁移命令不同**：
        *  单元测试：`python manage.py makemigrations`
        *  功能测试：`python manage.py migrate`
    * **与单元测试不同的是，功能测试不会在每一次的测试后清空数据库。**
6. 实际的数据库在工程目录下的db.sqlite3文件中，在settings.py中有如下配置:

```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
    

#### 需要记住的代码
1. Django在view中重定向的代码：`redirect('/')`
2. 重定向时，response返回的code是302，location属性是重定向的url

```python
self.assertEqual(response.status_code, 302) 

self.assertEqual(response['location'], '/')
```

3. 生产数据库的迁移命令：`python manage.py migrate`
4. 删除数据库、重新迁移的命令：
    * `rm db.sqlite3` 注：windows可能需要停止服务器
    * `python manage.py migrate --noinput`
5. git tag命令可以标记一些信息
6. Django模板标签：
    1. {% csrf_token %}，详情见第五节的第二个知识点
    2. {% for ... endfor %}，可以在模板的html中动态渲染数据，如后面的代码：
    3. {{ forloop.counter }}可以记录循环的次数

```html
{% for item in items %}
    <tr><td>{{ forloop.counter }}: {{ item.text }}</td></tr>
{% endfor %}
```

# 第七节 改进功能测试
### 知识性收获
#### 确保测试的稳定性和可靠性
1. 功能测试应该具有很好的“**确定性(deterministic)**”和“**可靠性(reliable)**”。
2. 单元测试在数据库方面**具有稳定性**。
    *  当我们运行单元测试时，Django 会自动创建个全新的测试数据库（不同于真实数据库），这个数据库可以**安全的重置而不干扰真实数据库（db.sqlite3）**。
3. 当测试类继承自 unittest 包的 TestCase 时（整个项目的功能测试），每一次测试将**不再建立临时数据库** ——————> 这样的测试稳定性极差
    * 解决办法：
        * 手动修改功能测试 ———— 修改 setUp 和 tearDown 方法让其具有稳定性
        * 继承Django 1.4 后出现的新类 LiveServerTestCase
4. **子类化 LiveServerTestCase 能让功能测试有一个稳定的行为**
    * 其会像单元测试一样自动创建一个测试数据库
    * 其会为每一次功能测试部署一个独立的开发服务器
        * 因为每次都会部署、所以get方法的url需要使用动态url`self.browser.get(self.live_server_url)`
    * 其一般使用 manage.py 运行
5. Django 1.6 以后**项目的测试运行器**（命令：python manage.py test）会自动搜索**本项目中**所有带 test 开头的代码，然后运行它。
    * 所以**继承 LiveServerTestCase 的名为 test 的文件**可以将代码中的 main 方法删除 ~~`if __name__ == '__main__'`~~

> **为了代码的整洁**，最好将项目的各个功能测试单独放在一个文件夹（functional_test）中。  
> 继承了 LiveServerTestCase 后，且以单独的文件夹（functional_test）放置功能测试以后，单独运行功能测试需要运行这个代码 :  
> `python manage.py test functional_tests`

#### 减少或是调整必要的等待时间，使它更加合适
1. **显式等待（explicit wait）与隐式等待（implicit waits）**
    1. 显式等待 -> 单独的一句sleep代码 `time.sleep(1)`
    2. Selenium 提供了隐式等待 `implicitly_wait()`，但是其在 Selenium 3 后的行为变得很不稳定
2. **自己编写合适的隐式等待代码**:
```python
    def wait_for_row_in_list_table(self, row_text):

    start_time = time.time()
    while True:
        try:
            table = self.browser.find_element_by_id('id_list_table')
            rows = table.find_elements_by_tag_name('tr')
            self.assertIn(row_text, [row.text for row in rows])
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e

            time.sleep(0.5)
```

> 此代码很 ugly ，因为其没有将 timing 和 re-raising logic 分开。后期需要 refactoring.

### 需要记住的代码
1. 使用 LiveServerTestCase 后
    1. 获取动态url的方法 `self.browser.get(self.live_server_url)`
    2. 单独运行功能测试的指令 `python manage.py test functional_tests`
    3. 单独运行单元测试的指令 `python manage.py test APPNAME`
2. **自己编写合适的隐式等待代码**:
```python
    def wait_for_row_in_list_table(self, row_text):

    start_time = time.time()
    while True:
        try:
            table = self.browser.find_element_by_id('id_list_table')
            rows = table.find_elements_by_tag_name('tr')
            self.assertIn(row_text, [row.text for row in rows])
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e

            time.sleep(0.5)
```

# 第八节 增量开发（上）
### 知识性收获
1. **增量开发**会使你的代码**一步一步**的从**一个可运行的状态**转变成**另一个可运行的状态**
2. **YAGNI！** ———— 是我们用来抵制我们过度热情的创造性冲动的口头禅
    * 只设计和编写自己需要的功能
    * 不要编写不需要的功能而增加代码的复杂性
3. **REST**   
     Representational State Transfer（REST）是一种** Web 设计方法**，通常用于指导基于 Web 的 API 的设计。
4. **##号的注释**
    * 单 # 号的注释，是为了解释代码
    * 双 # 号是为了提醒当初的自己为什么这么做
5. **在编写新功能前，确保我们有一个回归测试（Regression Test）**
    * 当你**需要添加新功能时**，首先应该编写的是功能测试，但是此时**应该要有一个回归测试来保证你之前的功能不会在增加功能时被破坏**
    * 如果在**添加新功能时**，你已经有了一个测试函数/类、那么**在保留它的前提下，引入新的测试类/测试函数。**
    * 当你在修改代码时，发现你的回归测试出了差错，你**必须回去保证回归测试正常。** ——> 编写新的单元测试、进入新的 TDD 循环。
6. 当**所有的单元测试都通过了、而功能测试依旧没有通过**，通过研究测试的代码后，发现：
    *  确信单元测试代码的确覆盖了功能测试的问题，那么**通常指向了单元测试未涵盖的问题**
    *  如果发现单元测试代码没有覆盖功能测试的问题，那么重新编写单元测。
7. 默认情况下，浏览器将POST数据发送回其**当前所在的URL**(*进入这个页面的 URL*)
    * 当你想要更改此 POST 的 url 时，去修改 from 表单的 action 属性如：`<form method="POST" action="/lists/new">`
8. 我们约定**当 URL 的结尾没有 “/” 时**，代表着我们**要使用这个 URL 去修改数据库中的数据**了。
9. 目前理解中增量开发是：
    * 每一次去尝试开发一个很小的改变、比如，我们将一个需要的功能分解成了四个小部分、先针对这个功能编写功能测试、然后再分别对这四个小部分编写单元测试，以编写代码和进行重构。

### 需要记住的代码
1. 利用**正则表达式**的断言语句`self.assertRegex(需要判断的字符串, '正则式')`。
2. 使用 assertContains 代替 assertIn/ response.content.decode()。
    * `self.assertContains(response, 需要查找的字符串)`
3. 测试 response 是否**重定向**到某一个 url 的断言。
    * `self.assertRedirects(response, '重定向的 url')`

# 第九节 增量开发（下）
### 知识性收获
1. `A = models.TextField(default='')`这个类型只能保存字符串类型、若是把自定义对象赋给 A ，那么会保存着这个对象的字符串表示。
2. 若想要在数据库 Model 中保存另一个对象，则需要使用 `models.ForeignKey(ForeignClass, default=None)`
3. 删除迁移很危险。我们确实需要一次又一次地做，因为我们并不总是在第一时间获得我们的模型代码。但是如果删除已经应用于某个数据库的迁移，Django将会对它所处的状态以及如何应用未来的迁移感到困惑。只有在确定未使用迁移时才应该这样做。一个好的经验法则是，您永远不应删除或修改已提交给VCS的迁移。
4. 格式化字符串常量
    1. **是 Python3.6 新引入的一种字符串格式化方法**，主要目的是使格式化字符串的操作更加简便。
    2. f-string在形式上是以 f 或 F 修饰符引领的字符串（f'xxx' 或 F'xxx'），以大括号 {} 标明被替换的字段；f-string在本质上并不是字符串常量，而是一个在运行时运算求值的表达式,例：
        1. `comedian = {'name': 'Eric Idle', 'age': 74}`
        2. `f"The comedian is {comedian['name']}, aged {comedian['age']}."`
5. 在 url.py 中 urlpatterns 列表里的 url 对象的第一个参数往往是正则表达式，其中**每使用一次 “group” —— () ，就会传递 group 里正则识别出的字符串**给第二个参数（可调用对象，一般是 view 中的函数）
6. Model 中的每一类都可以使用 `ClassName.objects.get(id=object_id)` 函数进行查找并拿到指定 id 的对象。
7. Model 中的每一类都可以使用 `ClassName.objects.filter(AttributeName = attr)`函数进行筛查查出数据库里该类的所有对象中**某属性 == attr 的所有对象**，并**返回集合**
8. **.item_set称为反向查找**：它是Django令人难以置信的ORM之一，可让您从不同的表中查找对象的相关项目，例如：`for item in list.item_set.all`，这个循环每一次都能拿到一个 item ，**这些 item 是根据 list 对象反向查找的所有 item（item 里包含了list 对象）**
9. project/urls.py 实际上适用于适用于整个站点的 URL。
    1. 对于仅适用于列表应用程序的 URL，Django鼓励我们使用单独的 application/ urls.py，以使应用程序更加自包含。
    2. project/urls.py 的 urlpatterns 可以添加 `url(r'^lists/', include(list_urls))`include 是包含。请注意，它可以将URL正则表达式的一部分作为前缀，这将应用于所有包含的URL（这是我们减少重复的位，以及为我们的代码提供更好的结构）。
    3. application/ urls.py 里的 `urlpatterns = [ url(r'^new$', views.new_list, name='new_list')]`
    4. 若将 2 中的 urlpatterns 展开会是这样：`url(r'^lists/new$', views.new_list, name='new_list')`
10. 增量开发：
    1. 工作状态到工作状态（又名测试山羊与重构猫）
        * 增量开发鼓励我们一步一步，慢慢的从工作状态到工作状态。
        * 这里的工作状态是指之前的测试用例通过、也就是增加新功能时，回归测试通过。
    2. 将工作分成小的，可实现的任务。
    3. 遵循 YAGNI 法则，不开发没有必要的功能使代码变得臃肿。

### 需要记住的代码
1. 数据库 Model 中的外键代码:`models.ForeignKey(ForeignClass, default=None)`
2. Model 中的每一类都可以使用 `ClassName.objects.get(id=object_id)` 函数进行查找并拿到指定 id 的对象。
3. Model 中的每一类都可以使用 `ClassName.objects.get(id=object_id)` 函数进行查找并拿到指定 id 的对象。
4. Model 中的每一类都可以使用 `ClassName.objects.filter(AttributeName = attr)`函数进行筛查查出数据库里该类的所有对象中**某属性 == attr 的所有对象**，并**返回集合**
5. **.item_set称为反向查找**：它是Django令人难以置信的ORM之一，可让您从不同的表中查找对象的相关项目，例如：`for item in list.item_set.all`

## 第十节 布局和样式测试
### 知识性收获
1. **TDD 不应该测试美学(玄学）、但是我们可以测试我们美学的实施**（让我们自己确信代码是有效的），例如：我们可以快速检查主输入框是否按照我们在每个页面上的方式对齐，这将使我们相信该页面的其余样式也可能已加载。

2. **Django 模板继承**
    1. **Django模板语言使模板继承变得容易。**
    2. **目的：**减少重复代码
    3. 使用模板继承：
        1. 在**模板“父类”里使用**`{% block 变量名%}{% endblock %}`代表字符串、变量等 python 变量的**占位符。**
        2. 在**模板的子类中**使用`{% extends '父类模板名称.html' %}`**加载“父类”模板**
        3. 使用 `{% block 变量名%} 实际的变量/代码段 {% endblock %}` **代替模板“父类”中的变量占位符。**

### 需要记住的代码
