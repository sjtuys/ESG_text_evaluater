# ESG_text_evaluater
*ESG (Environmental, Social, Governance) Measurement and Evaluation*
### 爬取股票代码
*请在登录雪球官网后，在开发者工具的Requests Headers中获取Cookie，在`--init--` 函数中将cookie键值对的value改为自己的cookie*

在start_url中随时更新page与real_time，获得雪球的5000余个股票代码，在parse函数中将获得的股票代码存在res_list中返回

在parse和下面的parse_all_url、parse_comment_url中的User Agent是使用fake_useragent获的随机UA，设置爬取delay为随机数，避免无时间间隔被封IP

### 爬取关键词搜索得到的评论
parse_all_url函数通过调用parse_comment_url获得评论的json文件，以股票代码+ID+评论代码命名，并将该评论详情页网址以"url":https://xueqiu.com/user_id/comment_id 的键值对形式存入该字典

同时将总评论个数，股票代码，关键词，评论ID，评论题目，查询网址以字典加入sum.json，方便后续统计评论总数、不同关键词、不同股票数据量

### Demo
在该Demo中，仅选取第一页的90个股票代码进行爬取
