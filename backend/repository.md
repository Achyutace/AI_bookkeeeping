## Entry
### write_entry_batch
向csv添加条目
param: 
- df: dataframe（必填）
return: 新增条目数
添加条目时自动顺延
兜底返回0
### delete_entry
param: 
- id: 条目的id
return: id
兜底返回0
### delete_entry_batch
param:
- id_list
return 删除的数量
兜底返0
### select_entry
根据条目筛选
param：
- category: 类别，空着默认all
- tag: {"类别": ["具体标签1", "具体标签2"]}
- reverse: True表示反选（除了这些标签都选）, False表示不反选正常选
return: 所有待选的id
兜底返回0
### change_entry
param:
id: 
add_tag: [""]
delete_tag: [""]
add_category: [""]
delete_category: [""]
return: 更改的东西的id
兜底返回0
### change_entry_batch
id: list
add_tag: [""]
delete_tag: [""]
add_category: [""]
delete_category: [""]
return: 更改的东西的数量
兜底返回0

## Category
### 新增category/tag
param: category（这玩意就是主key）
param: tag
逻辑：若有category_name就新增tag，没有就一起新增
return: category_name/ None, tag / None（兜底返回两个None）

### 删除category/tag
param: category
param: tag
逻辑：若没填tag则删除category，填了则严格只删除category

## user
### add_user：新建空白帐户
user_name
### delete
user_name