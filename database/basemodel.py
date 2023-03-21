import functools
from typing import Iterable
import sqlalchemy
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import scoped_session, sessionmaker
from pathlib import Path


base_path = Path().resolve()
database_name = 'lg_database.db'
sql_url = f'sqlite:///{base_path}/{database_name}'
engine = create_engine(f"{sql_url}?check_same_thread=False", echo=False)
Base = sqlalchemy.orm.declarative_base()   # type: ignore
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)


@contextmanager
def Db_session(commit=True):
    """db session封装.

    :params commit:进行数据库操作后是否进行commit操作的标志
                   True：commit, False:不commit
    """
    try:
        yield session
        if commit:
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        if session:
            session.close()


def class_dbsession(commit=True):
    """用于BaseModel中进行数据库操作前获取dbsession操作.

    :param commit:进行数据库操作后是否进行commit操作的标志，True：commit, False:不commit
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            # cls为对象或类
            cls = args[0]
            # 实际传入的参数
            new_args = args[1:]
            with Db_session(commit) as session:
                return func(cls, session, *new_args, **kwargs)
        return inner
    return wrapper


class BaseModel(object):
    u"""基础模型."""

    @class_dbsession(True)
    def add(self, session):
        u"""增.

        eg: a = MerchantBillDetail(id=1)
            a.add()
        """
        session.add(self)

    @classmethod
    @class_dbsession(True)
    def delete(cls, session, where_conds=[]):
        u"""删.

        eg: BaseModel.delete([BaseModel.a>1, BaseModel.b==2])
        """
        session.query(cls).filter(*where_conds).delete(
            synchronize_session='fetch')

    @classmethod
    @class_dbsession(True)
    def update(cls, session, update_dict, where_conds=[]):
        u"""更新.

        eg: BaseModel.update({'name': 'jack'}, [BaseModel.id>=1])
        """
        return session.query(cls).filter(*where_conds).update(
            update_dict,
            synchronize_session='fetch')

    @classmethod
    @class_dbsession(False)
    def query(cls, session, *args, **kwargs):
        u"""查询.

        eg: BaseModel.query([BaseModel.id, BaseModel.name],
                filter=[BaseModel.id>=1],
                group_by=[BaseModel.id, BaseModel.name]
                order_by=BaseModel.id.desc(), limit=10, offset=0)
        """
        if not kwargs:
            if not set(kwargs.keys()).issubset(
                    {'filter', 'group_by', 'order_by', 'limit', 'offset'}):
                raise Exception('input para error!')
        cfilter = kwargs.pop('filter', None)
        group_para = kwargs.pop('group_by', None)
        order_para = kwargs.pop('order_by', None)
        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', None)
        query_first = kwargs.get('query_first', False)
        join = kwargs.pop('join', None)

        if not isinstance(args[0], Iterable):
            args = [args[0]]
        squery = session.query(*args[0])
        if cfilter is not None:
            squery = squery.filter(*cfilter)
        if group_para is not None:
            squery = squery.group_by(*group_para)
        if order_para is not None:
            squery = squery.order_by(order_para)
        if limit is not None:
            squery = squery.limit(limit)
        if offset is not None:
            squery = squery.offset(offset)
        if join is not None:
            squery = squery.join(join[0], *join[1:])
        if query_first:
            return squery.first()
        return squery.all()

    @classmethod
    @class_dbsession(True)
    def batch_add(cls, session, *objs):
        """批量增加.

        eg: a = [MerchantBillDetail(id=1), MerchantBillDetail(id=2)]
            MerchantBillDetail.batch_add(a)
        """
        return session.add_all(objs[0])

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
