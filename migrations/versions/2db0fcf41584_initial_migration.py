"""Initial migration.

Revision ID: 2db0fcf41584
Revises: 
Create Date: 2025-03-08 10:49:19.773268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2db0fcf41584'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comparison_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('shop_x_cost', sa.Float(), nullable=False),
    sa.Column('shop_x_rating', sa.Float(), nullable=True),
    sa.Column('shop_x_delivery_cost', sa.Float(), nullable=False),
    sa.Column('shop_x_payment_mode', sa.String(), nullable=True),
    sa.Column('shop_y_cost', sa.Float(), nullable=False),
    sa.Column('shop_y_rating', sa.Float(), nullable=True),
    sa.Column('shop_y_delivery_cost', sa.Float(), nullable=False),
    sa.Column('shop_y_payment_mode', sa.String(), nullable=True),
    sa.Column('marginal_benefit', sa.Float(), nullable=True),
    sa.Column('cost_benefit', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phoneNumber', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('Role', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phoneNumber'),
    sa.UniqueConstraint('username')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=100), nullable=True),
    sa.Column('product_price', sa.Float(), nullable=True),
    sa.Column('product_rating', sa.Float(), nullable=True),
    sa.Column('product_url', sa.String(length=255), nullable=True),
    sa.Column('delivery_cost', sa.Float(), nullable=True),
    sa.Column('shop_name', sa.String(length=100), nullable=True),
    sa.Column('payment_mode', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('navigate_link', sa.String(length=255), nullable=True),
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], name='fk_product_shop'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('search_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('query', sa.String(), nullable=False),
    sa.Column('searched_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('payment_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    op.drop_table('orders')
    op.drop_table('search_history')
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('shops')
    op.drop_table('comparison_results')
    # ### end Alembic commands ###
