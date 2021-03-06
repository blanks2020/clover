#coding=utf-8

import datetime

from clover.exts import db

from clover.models import query_to_dict
from clover.dashboard.models import InterfaceDashboardModel


class DashboardService(object):

    def create(self, data):
        """
        # 将页面数据保存到数据库。
        :param data:
        :return:
        """
        try:
            model = DashboardModel(**data)
            db.session.add(model)
            db.session.commit()

            return model.id
        except:
            db.rollback()

    def update(self, data):
        """
        # Use ID as a condition to update the database's duplicate data records.
        # If no data can be found through ID, it will be added as a new record.
        :param data:
        :return:
        """
        try:
            old_model = InterfaceDashboardModel.query.get(data['id'])
            if old_model is None:
                model = InterfaceDashboardModel(**data)
                db.session.add(model)
                db.session.commit()
                return model.id
            else:
                {setattr(old_model, k, v) for k, v in data.items()}
                old_model.updated = datetime.datetime.now()
                db.session.commit()

                return old_model.id
        except:
            db.rollback()

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {'enable': 0, **data}

        try:
            offset = int(data.get('offset', 0))
        except TypeError:
            offset = 0

        try:
            limit = int(data.get('limit', 10))
        except TypeError:
            limit = 10

        results = InterfaceDashboardModel.query.filter_by(
            **filter
        ).order_by(
            InterfaceDashboardModel.created.desc()
        ).offset(offset).limit(limit)
        results = query_to_dict(results)
        count = InterfaceDashboardModel.query.filter_by(**filter).count()
        return count, results
