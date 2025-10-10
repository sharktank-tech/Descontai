"""update models structure"""

from alembic import op
import sqlalchemy as sa


# Revisão e dependências
revision = 'xxxx_update_models'
down_revision = None  # troque pelo último revision_id da sua base
branch_labels = None
depends_on = None


def upgrade():
    # ---- Users ----
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column("password_hash",
                              type_=sa.String(length=255),
                              existing_type=sa.String(length=500),
                              existing_nullable=False)

        batch_op.create_unique_constraint("uq_users_username", ["username"])
        batch_op.add_column(sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()))

    # ---- Produtos ----
    with op.batch_alter_table("produtos", schema=None) as batch_op:
        batch_op.alter_column("originalprice",
                              type_=sa.Numeric(10, 2),
                              existing_type=sa.Float(),
                              existing_nullable=False)

        batch_op.alter_column("saleprice",
                              type_=sa.Numeric(10, 2),
                              existing_type=sa.Float(),
                              existing_nullable=False)

        batch_op.alter_column("discount",
                              type_=sa.Integer(),
                              existing_type=sa.Float(),
                              existing_nullable=False)

        batch_op.alter_column("vendidos",
                              type_=sa.Integer(),
                              existing_type=sa.String(length=20),
                              existing_nullable=True,
                              server_default="0")


def downgrade():
    # ---- Produtos ----
    with op.batch_alter_table("produtos", schema=None) as batch_op:
        batch_op.alter_column("vendidos",
                              type_=sa.String(length=20),
                              existing_type=sa.Integer(),
                              existing_nullable=True)

        batch_op.alter_column("discount",
                              type_=sa.Float(),
                              existing_type=sa.Integer(),
                              existing_nullable=False)

        batch_op.alter_column("saleprice",
                              type_=sa.Float(),
                              existing_type=sa.Numeric(10, 2),
                              existing_nullable=False)

        batch_op.alter_column("originalprice",
                              type_=sa.Float(),
                              existing_type=sa.Numeric(10, 2),
                              existing_nullable=False)

    # ---- Users ----
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("uq_users_username", type_="unique")
        batch_op.alter_column("password_hash",
                              type_=sa.String(length=500),
                              existing_type=sa.String(length=255),
                              existing_nullable=False)
        batch_op.drop_column("created_at")
        batch_op.drop_column("updated_at")
