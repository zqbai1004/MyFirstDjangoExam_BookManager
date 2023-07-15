# Django Book Management System

## Description

This is a book management system based on the Django framework. This is my first small project touching upon both frontend and backend development, with many requirements fulfilled through interactions with ChatGPT. Although I'm satisfied with my work, there are undoubtedly many areas in the project that could be optimized from an objective standpoint, such as the implementation of the book cover functionality.

## Project Environment

- Python 3.9.16
- Django 4.1
- MySQL

## Installation & Usage

In your local environment, ensure that you have Python and Django installed first. Then, you can clone this repository into your local Django project and configure settings.

Here are the specific steps:

1. Create a Django project locally.
2. Clone this repository into your Django project.
3. Add "books" to the INSTALLED_APPS configuration in setting.py:

    ```python
    INSTALLED_APPS = [
        ...
        'books.apps.BooksConfig',
    ]
    ```

4. Add "books" URL reference in the project's URLconf file, i.e., urls.py:

    ```python
    path('books/',include('books.urls')),
    ```

5. Configure the database connection in setting.py.

## Reference Documents

- [Django Official Documentation](https://docs.djangoproject.com/zh-hans/4.1)
- [ChatGPT](https://chat.openai.com/?model=gpt-4)

## Developer Information

- Name: Z.Q. Bai
- Email: zqbai1004@qq.com

## Feedback

If you have any questions or suggestions, please feel free to send me an email or leave your comments in the GitHub issues.

Thank you!


# Django图书管理系统

## 描述

这是一个基于Django框架的图书管理系统。这是我个人接触前后端开发的第一个小项目，很多需求都是通过与ChatGPT的互动完成的。尽管我对自己的工作感到满意，但从客观的角度来看，项目中肯定还存在许多可以优化的地方，例如，实现的图书封面功能。

## 项目环境

- Python 3.9.16
- Django 4.1
- MySQL

## 安装与使用

在你的本地环境中，首先确保你已经安装了Python、Django。然后，你可以克隆这个仓库到本地的Django项目中，并进行setting的配置

以下是具体步骤：

1. 本地创建Django项目
2. 在你的Django中克隆这个仓库
3. 增加“books”到setting.py中INSTALLED_APPS的配置
```python
    INSTALLED_APPS = [
        ...
        'books.apps.BooksConfig',
    ]
```
4.增加“books”的url引用在项目的URLconf文件即urls.py中
```python
    path('books/',include('books.urls')),
```

5、在setting.py中配置数据库连接。

## 参考文档

- [Django官方文档](https://docs.djangoproject.com/zh-hans/4.1)
- [ChatGPT](https://chat.openai.com/?model=gpt-4)

## 开发者信息

- 姓名：Z.Q. Bai
- 邮箱：zqbai1004@qq.com

## 反馈

如果你有任何问题或建议，欢迎通过邮件或GitHub的issues向我反馈。

谢谢！
