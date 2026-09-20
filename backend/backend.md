## route
### entry
#### 获取指定的条目
- Method: GET
- Path: /api/entries
- description: "get all entries"
- body: {
    "category": ["餐饮", "日常交通"],    // 空表示全部，不再区分收入/支出
    "tag": {"餐饮":["外卖", "水果"], "日常交通": []},// 空表示全部
    reverse: True
}

#### 修改指定的条目
- Method: PATCH
- Path: /api/entries/:id
- description: "修改单条的时候调用这个接口"
- body: {
    "category": [] // 空为归到未归类，category有什么就改为什么，交互逻辑写前端
    "tag": {"餐饮": ["外卖"], "日常交通": []} // 空列表是直接清空该分类的标签，有啥更新啥
}

#### 删除条目
- Method: DELETE
- Path: /api/entries/:id
- description： "删除条目"

#### 批量新增条目
- Method: POST
- Path: /api/entries/batch
- description: "对应 write_entry_batch，手动新增和 AI 导入后的落库都走这里，id 自动顺延"
- body: {
    "entries": [
        {
            "date": "2026-09-01",
            "time": "",             // 非必填
            "category": "餐饮",
            "tag": "外卖",          // 非必填
            "amount": 20.5,         // 正支出，负收入
            "account": "微信",
            "status": 0,            // 0正常，数字表示退款
            "note": ""              // 非必填
        }
    ]
}
- response: {
    "created": 2    // 实际新增条数
}

#### 批量修改条目
- Method: PATCH
- Path: /api/entries/batch
- description: "对应 change_entry_batch，批量加/删标签或改分类"
- body: {
    "ids": [1, 2, 3],
    "add_tag": ["外卖"],
    "delete_tag": [],
    "add_category": ["餐饮"],
    "delete_category": []    // 空数组表示不动
}
- response: {
    "changed": 3    // 实际改动条数
}

#### 批量删除条目
- Method: DELETE
- Path: /api/entries/batch
- description: "根据idx批量删除"
- body: {
    "ids": [1, 2, 3]
}
- response: {
    "deleted": 2    // 实际删除条数
}

### category
#### 增加分类
- Method: PUT
- Path: /api/category
- description: "add category and tag"
- body: {
    "category":  // 空表示增加tag
    "tag": ["",""] // 都空表示兜底
}
// 不可能category为空但tag不为空

#### 查看有什么分类
- Method: GET
- Path: /api/category
- description: "show category and tags"
- response: {
    "收入": {
        "家长给钱": [],
        ...
    },
    "支出": {
        ...
    },
    "general_tag": ["大钱"]
}

#### 删除分类
- Method: DELETE
- Path: /api/category
- description: "delete category and tag"
- body: {
    "category": [], // 有啥删啥
    "tag": {

    }
}
// 如果删tag，就删除entries的所有tag; 如果删


### user
#### 新建账目（对应 add_user）
- Method: PUT
- Path: /api/user
- description: "新建一个空白账目"
- body: {
    "user_name": "齐乐辰"
}
- response: {
    "user_name": "齐乐辰"
}

#### 删除账目（对应 delete）
- Method: DELETE
- Path: /api/user
- description: "删除账目"
- body: {
    "user_name": "齐乐辰"
}
- response: {
    "user_name": "齐乐辰"
}

// TODO：查（列出所有 user，供前端切换账目）和改（重命名 user）暂时没写，
// 因为 repository.md 里 user 只有 add_user / delete，等补上 select_user / rename 再补这两个 route。
