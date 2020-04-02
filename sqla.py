import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.ext.declarative

engine = sa.create_engine('sqlite:///example.sqlite3')

Base = sa.ext.declarative.declarative_base()

class Parent(Base):

     __tablename__ = 'parent'

     id = sa.Column(sa.Integer, primary_key=True)
     name = sa.Column(sa.Text, nullable=False)

class Child(Base):

     __tablename__ = 'child'

     id = sa.Column(sa.Integer, primary_key=True)
     name = sa.Column(sa.Text, nullable=False)
     parent_id = sa.Column(sa.ForeignKey('parent.id'), nullable=False)


Base.metadata.create_all(engine)

items = [('spam', ('eggs', 'bacon'))]

with engine.begin() as conn:
     for parent, children in items:
         p_id, = sa.insert(Parent,
bind=conn).execute(name=parent).inserted_primary_key
         params = [{'name': c, 'parent_id': p_id} for c in children]
         sa.insert(Child, bind=conn).execute(params)