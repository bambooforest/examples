# sqla.py - insert into a parent and child table

import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.ext.declarative

engine = sa.create_engine('sqlite://', echo=True)


Base = sa.ext.declarative.declarative_base()


class Parent(Base):

     __tablename__ = 'parent'

     id = sa.Column(sa.Integer, primary_key=True)

     name = sa.Column(sa.Text, unique=True, nullable=False)


class Child(Base):

     __tablename__ = 'child'

     id = sa.Column(sa.Integer, primary_key=True)

     parent_id = sa.Column(sa.ForeignKey('parent.id'), nullable=False)
     name = sa.Column(sa.Text, nullable=False)

     __table_args__ = (sa.UniqueConstraint(parent_id, name),)


Base.metadata.create_all(engine)


items = [('spam', ('eggs', 'bacon')), ('ham', ('spam', 'eggs'))]

with engine.begin() as conn:
     insert_parent = sa.insert(Parent, bind=conn).execute
     insert_child = sa.insert(Child, bind=conn).execute
     for parent, children in items:
         p_id, = insert_parent(name=parent).inserted_primary_key
         params = [{'name': c, 'parent_id': p_id} for c in children]
         insert_child(params)
