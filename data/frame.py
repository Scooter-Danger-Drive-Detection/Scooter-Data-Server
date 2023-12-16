import datetime
import sqlalchemy
from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired
from .db_session import SqlAlchemyBase
from .session import SessionTable


class FrameTable(SqlAlchemyBase):
    __tablename__ = 'frame'

    frame_id = sqlalchemy.Column(sqlalchemy.BigInteger,
                                 primary_key=True, autoincrement=True)
    session_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey(SessionTable.id))
    session = orm.relationship(SessionTable)
    last_frame_id = sqlalchemy.Column(sqlalchemy.Integer)

    speed = sqlalchemy.Column(sqlalchemy.Float)
    longitude = sqlalchemy.Column(SqlAlchemyBase.Double)
    latitude = sqlalchemy.Column(SqlAlchemyBase.Double)

    acceleration_x = sqlalchemy.Column(sqlalchemy.Double)
    acceleration_y = sqlalchemy.Column(sqlalchemy.Double)
    acceleration_z = sqlalchemy.Column(sqlalchemy.Double)

    gravity_x = sqlalchemy.Column(sqlalchemy.Double)
    gravity_y = sqlalchemy.Column(sqlalchemy.Double)
    gravity_z = sqlalchemy.Column(sqlalchemy.Double)

    rotation_delta_x = sqlalchemy.Column(sqlalchemy.Double)
    rotation_delta_y = sqlalchemy.Column(sqlalchemy.Double)
    rotation_delta_z = sqlalchemy.Column(sqlalchemy.Double)
