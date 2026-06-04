# Flask-SQLAlchemy 常用方法速查

## 查询

```python
# 查所有
User.query.all()

# 查第一个
User.query.first()

# 按主键查
User.query.get(1)
User.query.get_or_404(1)          # 不存在自动返回 404

# 条件查询
User.query.filter(User.id == 1).first()
User.query.filter(User.name == 'admin').all()
User.query.filter(User.age >= 18).all()

# 多条件
User.query.filter(User.age >= 18, User.status == 1).all()
User.query.filter(db.and_(User.age >= 18, User.status == 1)).all()
User.query.filter(db.or_(User.name == 'a', User.name == 'b')).all()

# 模糊搜索
User.query.filter(User.name.like('%张%')).all()
User.query.filter(User.name.ilike('%zhang%')).all()  # 不区分大小写

# IN 查询
User.query.filter(User.id.in_([1, 2, 3])).all()

# BETWEEN
User.query.filter(User.age.between(18, 30)).all()

# 非空
User.query.filter(User.email.isnot(None)).all()

# 排序
User.query.order_by(User.id.desc()).all()
User.query.order_by(User.created_at.desc(), User.id.asc()).all()

# 限制条数
User.query.limit(10).all()

# 偏移
User.query.offset(10).limit(10).all()  # 跳过10条，取10条
```

## 分页

```python
pagination = User.query.paginate(page=1, per_page=10, error_out=False)

pagination.items      # 当前页数据列表
pagination.page       # 当前页码
pagination.pages      # 总页数
pagination.total      # 总条数
pagination.per_page   # 每页条数
pagination.has_next   # 是否有下一页
pagination.has_prev   # 是否有上一页
pagination.next_num   # 下一页页码
pagination.prev_num   # 上一页页码
```

## 新增

```python
user = User(name='张三', age=20)
db.session.add(user)
db.session.commit()

# 批量
db.session.add_all([user1, user2])
db.session.commit()
```

## 修改

```python
# 查出来改
user = User.query.get(1)
user.name = '李四'
db.session.commit()

# 批量更新
User.query.filter(User.status == 0).update({User.status: 1})
db.session.commit()
```

## 删除

```python
# 删一条
user = User.query.get(1)
db.session.delete(user)
db.session.commit()

# 批量删
User.query.filter(User.status == 0).delete()
db.session.commit()
```

## 聚合

```python
from sqlalchemy import func

User.query.count()                              # 计数
User.query.filter(User.age >= 18).count()       # 条件计数
db.session.query(func.max(User.age)).scalar()   # 最大值
db.session.query(func.min(User.age)).scalar()   # 最小值
db.session.query(func.avg(User.age)).scalar()   # 平均值
db.session.query(func.sum(User.age)).scalar()   # 求和
```

## 事务

```python
try:
    db.session.add(user)
    db.session.commit()
except:
    db.session.rollback()
    raise
```

## 只取部分字段

```python
# 只取某些列
users = db.session.query(User.id, User.name).all()

# 取单个值
name = db.session.query(User.name).filter(User.id == 1).scalar()
```
