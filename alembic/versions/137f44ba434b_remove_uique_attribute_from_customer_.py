"""remove uique  attribute from customer user_id

Revision ID: 137f44ba434b
Revises: ae46eccc56b3
Create Date: 2026-08-31 18:02:10.587884

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "137f44ba434b"
down_revision: Union[str, Sequence[str], None] = "ae46eccc56b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None





def upgrade() -> None:
    op.drop_constraint(
        "customers_ibfk_1",
        "customers",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_customers_user_id",
        table_name="customers",
    )

    op.create_index(
        "ix_customers_user_id",
        "customers",
        ["user_id"],
        unique=False,
    )

    op.create_foreign_key(
        "customers_ibfk_1",
        "customers",
        "users",
        ["user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "customers_ibfk_1",
        "customers",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_customers_user_id",
        table_name="customers",
    )

    op.create_index(
        "ix_customers_user_id",
        "customers",
        ["user_id"],
        unique=True,
    )

    op.create_foreign_key(
        "customers_ibfk_1",
        "customers",
        "users",
        ["user_id"],
        ["id"],
    )
