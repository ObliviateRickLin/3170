[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9434978&assignment_repo_type=AssignmentRepo)
# CSC3170 Course Project

## Project Overall Description

This is our implementation for the course project of CSC3170, 2022 Fall, CUHK(SZ). For details of the project, you can refer to [project-description.md](project-description.md). In this project, we will utilize what we learned in the lectures and tutorials in the course, and implement either one of the following major jobs:

<!-- Please fill in "x" to replace the blank space between "[]" to tick the todo item; it's ticked on the first one by default. -->

- [x] **Application with Database System(s)**
- [ ] **Implementation of a Database System**

## Team Members

Our team consists of the following members, listed in the table below (the team leader is shown in the first row, and is marked with 🚩 behind his/her name):

<!-- change the info below to be the real case -->

| Student ID | Student Name | GitHub Account (in Email) | GitHub User Name |
| ---------- | ------------ | ------------------------- | ---------------- |
| 119010351  | 谢昊轩 Haoxuan Xie 🚩      | 119010351@link.cuhk.edu.cn        |@[ForwardStar](https://github.com/ForwardStar) |
| 119010020  | 陈梦洁 Mengjie Chen        | 119010020@link.cuhk.edu.cn        |@[wuli-mA](https://github.com/wuli-mA) |
| 121090434  | 潘婕 Jie Pan          | 121090434@link.cuhk.edu.cn        | @[121090434](https://github.com/121090434)|
| 120090302  | 苏梦琦 Mengqi Su        | 120090302@link.cuhk.edu.cn        | @[Su-823](http://github.com/Su-823) |
| 120090005  | 钟文柯 Wenke Zhong        | 120090005@link.cuhk.edu.cn        | @[120090005](https://github.com/120090005)|
| 120090527  | 林锦睿 Jinrui Lin        | 120090527@link.cuhk.edu.cn        | @[RickLin616](https://github.com/RickLin616)|
| 119010224  | 罗杨知心 Yangzhixin Luo      | rep_laureline@hotmail.com        | @[lyzx2001](https://github.com/lyzx2001) |
| 119020226  | 蒋舒亭 Shuting Jiang        | 119020226@link.cuhk.edu.cn        | @[zxcg770](https://github.com/zxcg770)|
| 120090466  | 何兴杰 Xingjie He        | 120090466@link.cuhk.edu.cn        | @[JAck-Yolo](https://github.com/JAck-Yolo)|
| 120090454  | 仝研 Yan Tong          | yantong1775@gmail.com       | @[yantong1775](https://github.com/yantong1775) |

## Project Specification

<!-- You should remove the terms/sentence that is not necessary considering your option/branch/difficulty choice -->

After thorough discussion, our team made the choice and the specification information is listed below:

- Our option choice is: **Option 1**
- Our branch choice is: **Branch 1, 2**
- The difficulty level is: **Enhanced**

## Project Abstract
In this project, we intend to build a web-based database for a chip-manufacture company that synthesizes various functions of an online order management platform. The platform allows the registration from both customers and employees, where customers can release order and the employees are able to manage the order under the assistance of the information gathered by the database. Payments can also be finished on the platform as it allows **high concurrency payment** and clash recovery. All transaction records will be stored in the online database for analytical needs.

To simulate a real company and satisfy its possible business needs, we will create **data visualization dashboard** that enables the operational analysis such as customer profile, order completion rate, and geometrical distribution of deliveries. Moreover, the platform automatically allocates the production tasks to various plants belonging to the company under certain geometric constraints and the **cost-minimization purpose**. According to the real-time data of each machine's availability, orders will be assigned to the nearest plant to the customer that is available to finish the task. The operation costs of each machines will also be taken into consideration when designing the production chain. The system will reinforce its production strategy based on past data and try to provide its users with clear decision supports.

## Database Creation and Data Generation
To create database schemas, run the sql file [``source/db.sql``](https://github.com/CSC3170-2022Fall/project-wiskey-drunkards/blob/main/source/db.sql).

To generate random data in .csv format, run the .ipynb codes in [``source/data_generation``](https://github.com/CSC3170-2022Fall/project-wiskey-drunkards/tree/main/source/data_generation).

The detailed information of database schemas is included in [``Database.md``](https://github.com/CSC3170-2022Fall/project-wiskey-drunkards/blob/main/Database.md).