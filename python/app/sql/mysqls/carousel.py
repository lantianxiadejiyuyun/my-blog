from app.models import Carousel
from app.utils.validators import check_or_raise
from app.extensions import db
from app.utils.errors import AppError
from app.utils.format_datetime import format_datetime

# 查询 获取首页轮播图列表 有限数据
def get_carousels_list():

    query = Carousel.query
    query = query.filter(Carousel.status == 1)
    query = query.order_by(Carousel.sort_order.asc())

    data = query.all()


    result = [{
            'id':item.id,
            'title':item.title,
            'image_url':item.image_url,
            'link_url':item.link_url,
            'description':item.description,
            } for item in data]

    return result


# 查询 获取首页轮播图列表 完整数据
def get_carousels_list_all(page, page_size):
    page = check_or_raise(page, type=int,min_len=1,name='page')
    page_size = check_or_raise(page_size, type=int,min_len=1,name='page_size')

    query = Carousel.query
    query = query.filter(Carousel.status == 1)
    query = query.order_by(Carousel.sort_order.asc())

    data = query.paginate(page=page, per_page=page_size, error_out=False)


    result = [{
            'id':item.id,
            'title':item.title,
            'image_url':item.image_url,
            'link_url':item.link_url,
            'description':item.description,
            'sort_order':item.sort_order,
            'status': item.status,
            'created_at':format_datetime(item.created_at),
            'updated_at':format_datetime(item.updated_at),
            } for item in data]

    return {
        'list':result,
        'page': data.page,
        'pages': data.pages,
        'total': data.total,
        'page_size': data.per_page,
    }
